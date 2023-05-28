from bs4 import BeautifulSoup
from duckduckgo_search import ddg
import openai
import pycreds
import logging
import threading
import queue
from readability import Document
import scrapy
from scrapy.crawler import CrawlerProcess
import os
from dotenv import load_dotenv
load_dotenv()


def extract_useful_information_from_single_chunk(url, title, text, idx, q=None):
    """
    説明：OpenAIのLLMによって有益なテキストデータのみを取り出す
    引数：url, title, ウェブサイトのテキスト
    戻り値：抽出されたテキストデータ
    """
    logger = logging.getLogger('ddgsearch')
    logger.info(f"extracting useful information from chunk {idx}, title: {title}")

    # 英語プロンプト（最初に使用）
    # prompt = f"""
    # Here is a url: {url}\n
    # Here is its title: {title}\n
    # Here is some text extracted from the webpage by bs4:\n
    # ----------\n
    # {text}\n
    # ----------\n
    # \n
    # Web pages can have a lot of useless junk in them. For example, there might be a lot of ads, or a lot of navigation links,
    # or a lot of text that is not relevant to the topic of the page. We want to extract only the useful information from the text.\n
    # \n
    # You can use the url and title to help you understand the context of the text.
    # Please extract only the useful information from the text. Try not to rewrite the text, but instead extract only the useful information from the text.
    # """
    prompt = f"""
    これはURL: {url}\n
    これはタイトル: {title}\n
    これはbs4.BeautifulSoupによって抽出されたウェブページの一部のテキストデータです。\n
    ----------\n
    {text}\n
    ----------\n
    \n
    ウェブページには多くの無駄なゴミが含まれています。例えば、多くの広告、多くのリンク集や
    そのウェブページのトピックには関係のないテキストなどがあります。私達はもとのテキストデータから
    有益な情報のみを抽出したいのです。\n
    \n
    あなたはURLやタイトルをテキストデータのコンテクストを理解するために使うことができます。
    テキストデータから有益な情報のみを抽出してください。しかし、もとのテキストデータの内容を書き換えることなく、有益な情報のみを抽出してください。
    """

    openai.api_key = os.getenv('OPENAI_API_KEY')

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=1000,
        temperature=0.2,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    if q:
        q.put((idx, response['choices'][0]['text']))
    logger.info(f"Done extracting useful information from chunk {idx}, title: {title}")

    text = response['choices'][0]['text']

    lines = text.splitlines()
    if "useful information" in lines[0].lower():
        text = "\n".join(lines[1:])

    return (idx, text)


def extract_useful_information(url, title, text, max_chunks):
    """
    説明：長いテキストをチャンクに分割して処理
    """
    chunks = [text[i*1000: i*1000+1100] for i in range(len(text)//1000)]
    chunks = chunks[:max_chunks]

    threads = []

    q = queue.Queue()

    for idx, chunk in enumerate(chunks):
        # 並列処理化
        t = threading.Thread(target=extract_useful_information_from_single_chunk, args=(url, title, chunk, idx, q))
        threads.append(t)
        t.start()

    # すべての処理が終了
    for t in threads:
        t.join()

    results = []
    while not q.empty():
        results.append(q.get())

    logger = logging.getLogger('ddgsearch')
    logger.info(f"Got {len(results)} results from the queue")

    # ソート処理
    results.sort(key=lambda x: x[0])
    
    # 分割されたテキストを結合
    text = ''.join([x[1] for x in results])

    return text


def readability(input_text):
    doc = Document(input_text)

    summary = doc.summary()

    soup = BeautifulSoup(summary, 'html.parser')
    summary_text = soup.get_text()

    return summary_text


def remove_duplicate_empty_lines(input_text):
    """
    説明：不要な重複の空白行を削除
    """
    lines = input_text.splitlines()

    fixed_lines = []
    for index, line in enumerate(lines):
        if line.strip() == '':
            if index != 0 and lines[index-1].strip() != '':
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)

    return '\n'.join(fixed_lines)

class MySpider(scrapy.Spider):
    """
    説明：crawler用のspiderクラス
    """
    name = 'myspider'
    start_urls = None
    clean_with_llm = False
    results = []

    def __init__(self, start_urls, clean_with_llm, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.start_urls = start_urls
        self.clean_with_llm = clean_with_llm

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        logger = logging.getLogger('ddgsearch')
        logger.info(f"***Parsing {response.url}...")

        body_html = response.body.decode('utf-8')

        url = response.url

        soup = BeautifulSoup(body_html, 'html.parser')
        title = soup.title.string
        text = soup.get_text()
        text = remove_duplicate_empty_lines(text)

        if self.clean_with_llm:
            useful_text = extract_useful_information(url, title, text, 50)
        else:
            useful_text = readability(body_html)
        useful_text = remove_duplicate_empty_lines(useful_text)

        self.results.append({
            'url': url,
            'title': title,
            'text': text,
            'useful_text': useful_text
        })


def ddgsearch(query, num_results=10, clean_with_llm=False):
    """
    説明：duckduckgoによってウェブサーチを行う
    引数：検索用のクエリ（必須）
    戻り値：検索結果
    """
    results = ddg(query, max_results=num_results)

    # ログの出力
    logger = logging.getLogger('ddgsearch')
    logger.info(f"Got {len(results)} results from the search.")
    logger.debug(f"Results: {results}")

    # urlの抽出
    urls = [result['href'] for result in results]
    urls = urls[:num_results]

    process = CrawlerProcess()
    process.crawl(MySpider, urls, clean_with_llm)
    process.start()

    return MySpider.results
