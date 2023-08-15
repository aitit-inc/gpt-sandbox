import os
import markdown2
from bs4 import BeautifulSoup


# 定数定義
OPEN_MODE_WRITE = 'w'
OPEN_MODE_READ = 'r'


def write_markdown(input: str, file_prefix: str) -> bool:
    """
    説明：マークダウンファイルを書き出す
    """
    input_md = markdown2.markdown(input)
    
    with open(file_prefix, OPEN_MODE_WRITE) as f:
        f.write(input_md)

    return True

def get_chapters(markdown_chapters: str):
    """
    説明：作成された目次から章を取得する
    """
    html = markdown2.markdown(markdown_chapters)

    soup = BeautifulSoup(html, 'html.parser')
    h1_all = soup.find_all('h1')
    chapters_count = 0
    h1_list = []
    for h1 in h1_all:
        h1_list.append(h1.text.strip())
        chapters_count += 1

    return chapters_count, h1_list