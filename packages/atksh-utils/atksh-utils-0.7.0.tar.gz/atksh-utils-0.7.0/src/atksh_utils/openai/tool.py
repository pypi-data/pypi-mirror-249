import io
import json
import os
import random
import re
import subprocess
import sys
import tempfile
import time
import tokenize
import traceback
import urllib.parse
from code import InteractiveConsole
from concurrent.futures import ThreadPoolExecutor as TPE
from contextlib import redirect_stderr, redirect_stdout
from functools import partial
from itertools import islice
from threading import Lock, Semaphore

import backoff
import pypdf
import requests
from bs4 import BeautifulSoup as bs4
from duckduckgo_search import DDGS
from urllib3.exceptions import ReadTimeoutError

from .prompt import SEARCH_RESULT_SUMMARIZE_PROMPT, VISIT_PAGE_SUMMARIZE_PROMPT
from .token import clean_text, count_token, sub_tokenize

# Create a temporary directory for storing files to $HOME/.cache/askgpt/
CACHE_DIR = os.path.join(os.path.expanduser("~"), ".cache", "askgpt")
os.makedirs(CACHE_DIR, exist_ok=True)
SESSION_PATH = os.path.join(CACHE_DIR, "session.pkl")

Print_LOCK = Lock()
DDGS_LOCK = Lock()
API_LOCK = Semaphore(16)
Python_LOCK = Lock()
Console_LOCK = Lock()
Shell_LOCK = Lock()
UserAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15"
PYTHON_PATH = sys.executable


CONSOLE = InteractiveConsole(locals=None)
MAX_ATTEMPTS = 5
MAX_SEARCH_RESULTS = 30
ANSI_ESCAPE = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
ARXIV_REGEX = re.compile(
    r"arxiv\.org\/(?:abs|pdf)\/((?:[0-9]+\.[0-9]+)|(?:old\.\d+)|(?:[a-z]+\/\\d+))(?:v\d+)?",
    re.UNICODE,
)


def make_chunk(text: str, max_length: int, overlap_ratio: float = 0.2) -> list[str]:
    text = clean_text(text)
    length = count_token(text)
    i = 0
    while True:
        try:
            (s, t), ret = sub_tokenize(text, i, i + max_length)
        except:
            break
        yield ret
        if t == length:
            break
        prev_i = i
        i += max_length
        diff = i - t
        i -= diff
        delta = prev_i - i
        i -= int(delta * overlap_ratio)
        i = min(i, length)
        if i == length:
            break


@backoff.on_exception(
    partial(backoff.expo, base=3, factor=2),
    (requests.exceptions.RequestException, ReadTimeoutError),
    max_tries=5,
    jitter=backoff.full_jitter,
)
def get_response(url: str) -> requests.Response:
    return requests.get(
        url,
        headers={"User-Agent": UserAgent, "Accept-Language": "ja,en-US;q=0.9,en;q=0.8"},
        timeout=15,
    )


def extract_output_if_possible(text: str) -> str:
    start_idx = text.find("<output>")
    if start_idx == -1:
        return text
    end_idx = text.find("</output>")
    if end_idx == -1:
        return text
    return text[start_idx + len("<output>") : end_idx]


def verbose():
    return os.getenv("ASKGPT_VERBOSE", "0") == "1"


def random_sleep():
    for _ in range(3):
        time.sleep(random.uniform(0.1, 1.0))


def parse_args(arguments: str) -> dict:
    try:
        return json.loads(arguments)
    except json.decoder.JSONDecodeError:
        try:
            return json.loads(arguments, strict=False)
        except:
            return arguments


def cb(chunk, _):
    with Print_LOCK:
        light_cyan = "\033[96m"
        reset = "\033[0m"
        if (finish_reason := chunk.choices[0].dict().get("finish_reason")) is not None:
            if finish_reason == "stop":
                print("\n")
        token = chunk.choices[0].delta.content
        if token:
            print(f"{light_cyan}{token}{reset}", end="")


def get_browser_functions(ai: "OpenAI"):
    visit_page_model_name = ai.model_name
    visit_page_max_context_length = (
        100000 if "gpt-4-1106-preview" in visit_page_model_name else 10000
    )
    visit_page_max_context_length -= count_token(VISIT_PAGE_SUMMARIZE_PROMPT)

    def _search_summarize(query_text: str, results: str) -> str:
        """Summarizes the query text and results."""
        search_result_child = ai.make_child(ai.model_name, temperature=0.2, top_p=0.8)
        search_result_child.set_system_prompt(SEARCH_RESULT_SUMMARIZE_PROMPT)
        error = "Unknown error."
        for i in range(MAX_ATTEMPTS):
            for _ in range(i + 1):
                random_sleep()
            try:
                with API_LOCK:
                    return extract_output_if_possible(
                        search_result_child(
                            f"Query: {query_text}\nResults: {results}\nSummary: ",
                            stream_callback=cb if verbose() else None,
                        )[1]
                    )
            except:
                error = traceback.format_exc()
                print(error)
                continue
        return f"Error: {error}.\nPlease try again or try another query."

    def _page_summarize(query_text: str, page: str) -> str:
        """Summarizes the query text and page."""
        visit_page_child = ai.make_child(visit_page_model_name, temperature=0.2, top_p=0.8)
        visit_page_child.set_system_prompt(VISIT_PAGE_SUMMARIZE_PROMPT)
        error = "Unknown error."
        for i in range(MAX_ATTEMPTS):
            for _ in range(i + 1):
                random_sleep()
            try:
                text = f"Query: {query_text}\nPage: {page}\nSummary: "
                with API_LOCK:
                    return extract_output_if_possible(
                        visit_page_child(
                            text,
                            stream_callback=cb if verbose() else None,
                        )[1]
                    )
            except:
                error = traceback.format_exc()
                print(error)
                continue
        return f"Error: {error}.\nPlease try again or try another url or wait_sec for a while."

    def search_on_web_by_duckduckgo(query_text: str, lang: None | str = None) -> str:
        """Searches the web for the query text. Returns the summarized search results. If you failed to get the results multiple times, please run `pip install -U duckduckgo-search` and try again.

        :param query_text: The keywords to query. For example, `今日の天気 東京`. This must be ensure_ascii=False.
        :type query_text: str
        :param lang: The language of the query text. `en` or `ja` is supported. If None, the language is wt-wt (worldwide).
        :type lang: str, optional
        :return: summarized search results.
        :rtype: str
        """
        your_query = repr(query_text)[1:-1]
        if len(query_text.split("\n")) > 1:
            ret = (
                "Error: Please use a single line query text.\n"
                f"Your query text:\n{your_query}\n"
                "Please try again or try another query like `今日の天気 東京の気温は？ yahoo天気`."
                "<instruction>Before retrying, clearly state your query and confirm that it is a single line query text.</instruction>"
            )
            print(ret)
            return ret
        attempts = 0
        search_results = []
        if lang is None:
            region = None
        elif lang == "en":
            region = "us-en"
        elif lang == "ja":
            region = "ja-ja"
        else:
            return "Error: lang must be either 'en' or 'ja'."
        while attempts < MAX_ATTEMPTS:
            with DDGS_LOCK:
                with DDGS() as ddgs:
                    search_results = ddgs.text(
                        query_text,
                        region=region,
                        safesearch="Off",
                        max_results=MAX_SEARCH_RESULTS,
                        backend="html",
                    )
                    search_results = list(search_results)
                    if search_results:
                        break
                    time.sleep(1.5 + attempts)
                    random_sleep()
                attempts += 1
                if verbose():
                    print(f"[search_on_web_by_duckduckgo] Retrying {attempts}...")

        results = json.dumps(search_results, ensure_ascii=False, indent=2)
        ret = "Error: No results found.\nPlease try again or try another query."
        if results:
            ret = f"Your query: {your_query}\n\nSummarized Search Results:\n"
            ret += _search_summarize(query_text, results).strip()
            ret += "\nPlease visit all the five pages so that you can get correct infomation to answer by `visit_page` tool."
        return ret

    def visit_page(query_text: str, url: str) -> str:
        """Visits the page at the url and summarizes the text with respect to the query text. Recommended to use after search_on_web_by_duckduckgo for each url.

        :param query_text: The topic for summarization. This must be ensure_ascii=False.
        :type query_text: str
        :param url: The url to visit (must be a valid url like `https://www.google.com`).
        :type url: str
        :return: The summarized text of the page.
        :rtype: str
        """
        your_query = repr(query_text)[1:-1]
        if len(query_text.split("\n")) > 1:
            ret = (
                "Error: Please use a single line query text.\n"
                f"Your query text:\n{your_query}\n"
                "Please try again or try another query like `東京 今日の天気`."
                "<instruction>Before retrying, clearly state your query and confirm that it is a single line query text.</instruction>"
            )
            print(ret)
            return ret
        if "arxiv.org" in url:
            paper_id = ARXIV_REGEX.search(url).group(1)
            url = f"https://www.arxiv-vanity.com/papers/{paper_id}/"
        try:
            random_sleep()
            response = get_response(url)
            content_type = response.headers.get("Content-Type", "")

            text: str = ""
            if "application/pdf" in content_type:
                # PDFファイルの処理
                pdf_content = response.content
                with tempfile.NamedTemporaryFile(suffix=".pdf") as temp_pdf:
                    temp_pdf.write(pdf_content)
                    temp_pdf.seek(0)
                    reader = pypdf.PdfReader(temp_pdf.name)
                    for page in reader.pages:
                        text += page.extract_text() + "\n"
            else:
                # 通常のHTMLページの処理
                soup = bs4(response.text, "html.parser")
                body = soup.find("body").text.strip()
                links = []
                for a in soup.find_all("a"):
                    href = a.get("href")
                    if href is None:
                        continue
                    n = a.text.strip()
                    if len(n) < 2:
                        continue
                    href = urllib.parse.urljoin(url, href)
                    links.append(f"{n}: `{href}`")
                links = " - " + "\n - ".join(links)
                text += body + "\n====LINKS====\n" + links

            while True:
                rets = []
                with TPE(max_workers=8) as executor:
                    futures = []
                    for chunk in make_chunk(text, visit_page_max_context_length):
                        future = executor.submit(_page_summarize, query_text, chunk)
                        futures.append(future)
                    for future in futures:
                        ret = future.result()
                        rets.append(ret)
                text = "\n".join(rets).strip()
                if len(text) < visit_page_max_context_length:
                    break
            ret = text
            ret = ret.strip()
            ret += '\nPlease visit "Related Links" if available so that you can get correct infomation to answer by `visit_page` tool.'
            ret = f"Your query: {your_query}\n\nSummarized Page:\n{ret}"
        except:
            e = traceback.format_exc()
            print(e)
            ret = f"Error: {e}.\nPlease try again or try another url."
        return ret

    return search_on_web_by_duckduckgo, visit_page


def run_pyhton_with_session(code: str) -> str:
    """This is a function that executes Python code and returns the stdout. Don't forget to print the result.

    :param code: Python code of multiple lines. You must print the result. For example, `value = 2 + 3; print(value)`.
    :type code: str
    :return: stdout of running the Python code.
    :rtype: str
    """
    lines = code.split("\n")
    lines = ["    " + line for line in lines]
    code = "\n".join(lines)
    result = ""
    with Python_LOCK, io.StringIO() as buf, redirect_stdout(buf), redirect_stderr(buf):
        out = None
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py") as f:
            try:
                f.write("import traceback\n")
                f.write("import dill\n")
                f.write(f"try:\n    dill.load_session('{SESSION_PATH}')\nexcept:\n    pass\n")
                f.write("\n\n\n")
                f.write("try:\n")
                f.write(code)
                f.write(
                    "\nexcept:\n    print(f'ERROR: {traceback.format_exc()}')\n    print('\\n\\n\\n')\n"
                )
                f.write("else:\n    print('\\n\\n\\nThe code is executed successfully.')\n")
                f.write("    print('The following is the system message about session.')\n")
                f.write(
                    f"\ntry:\n    dill.dump_session('{SESSION_PATH}')\nexcept:"
                    "\n    print('[SYSTEM INFO]: Failed to save this session:', traceback.format_exc())\n"
                    "else:\n    print('[SYSTEM INFO]: Saved this session.')\n"
                )
                f.flush()
                out = subprocess.check_output(f"{PYTHON_PATH} {f.name}", shell=True, text=True)
            except:
                e = traceback.format_exc()
                print(e)
                result += f"Error: {e}.\nPlease try again.\n"
            if out == "":
                result += "NotPrintedError('The result is not printed.')\nPlease print the result in your code."
            elif out is not None:
                result += out
            result += ANSI_ESCAPE.sub("", buf.getvalue())
            result = result.strip()
    if verbose():
        print("=== Run Python Code ===")
        print(result)
        print("=======================")
    return result


def bash(command: str) -> str:
    """Execute the given command and return the result.

    :param command: The command to execute. For example, `ls -l`.
    :type command: str
    :return: The result of the execution of the command.
    :rtype: str
    """
    with Shell_LOCK:
        try:
            ret = subprocess.check_output(command, shell=True)
        except subprocess.CalledProcessError as e:
            return_code = e.returncode
            output = e.output
            ret = f"Error: return_code={return_code}, output={output}"
        except:
            e = traceback.format_exc()
            print(e)
            ret = f"Error: {e}.\nPlease try again or try another command."
    ret = ANSI_ESCAPE.sub("", str(ret)).strip()
    if verbose():
        print("=== Bash ===")
        print(ret)
        print("============")
    return ret


def pip_install(command: str) -> str:
    """Install the given package with pip and return the result. Use this if and only if you encounter an error with `import`.

    :param command: The packages to install. For example, `numpy pandas`.
    :type command: str
    :return: The result of the installation of the package.
    :rtype: str
    """
    with Shell_LOCK:
        try:
            ret = subprocess.check_output(f"{PYTHON_PATH} -m pip install {command}", shell=True)
        except subprocess.CalledProcessError as e:
            return_code = e.returncode
            output = e.output
            ret = f"Error: return_code={return_code}, output={output}"
        except:
            e = traceback.format_exc()
            print(e)
            ret = f"Error: {e}.\nPlease try again or try another command."
    ret = ANSI_ESCAPE.sub("", str(ret)).strip()
    if verbose():
        print("=== Pip Install ===")
        print(ret)
        print("===================")
    return ret


def clear_all_python_session():
    """Clears the exec_python_code session.

    :return: True if the session is cleared successfully.
    :rtype: bool
    """
    try:
        if os.path.exists(SESSION_PATH):
            os.remove(SESSION_PATH)
        return True
    except:
        return False


def keep_writing_if_over_max_length():
    """To continue writing over the max_length, you can use this function to reset the output and continue writing but you cannot call this function twice.

    :return: message to continue writing.
    :rtype: str
    """
    return "Please continue writing. Do not call `keep_writing` again."


def wait_sec(seconds: int):
    """Wait for the given seconds.

    :param seconds: The seconds to wait.
    :type seconds: int
    :return: waited message.
    :rtype: str
    """
    time.sleep(seconds)
    return "Waited for {} seconds.".format(seconds)
