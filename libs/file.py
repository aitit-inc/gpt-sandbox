import os
import re
import markdown2
import json
from bs4 import BeautifulSoup
from .error_message import *

# 定数定義
OPEN_MODE_WRITE = 'w'
OPEN_MODE_READ = 'r'


def prepare_dir(dest):
    """
    説明：フォルダ準備
    """
    dest_dir = os.path.dirname(dest)
    if len(dest_dir):
        # ルートがない場合
        if not os.path.exists(dest_dir):
            os.mkdir(dest_dir)


def write_markdown(input, file_prefix: str, file_name: str):
    """
    説明：作成された章の構成を書き込む（.md形式を想定）
    入力：章の構成（リスト型）、ファイルを保管する場所
    出力：markdownファイルの作成
    """
    # markdownに変換
    input_md = markdown2.markdown(input)
    new_file = file_prefix + os.path.basename(file_name)
    # フォルダ準備
    prepare_dir(new_file)
    with open(new_file, OPEN_MODE_WRITE) as f:
        f.write(input_md)

def write_json(json_string, json_file):
    """
    説明：json形式で出力されたファイルを書き出す
    引数：json形式のstring、jsonファイルのパス
    戻り値：
    """
    data = json.loads(json_string)
    try:
        with open(json_file, OPEN_MODE_WRITE) as file:
            json.dump(data, file)
    except:
        print("入力が正しいJSONフォーマットでありません")

def get_chapters(markedown_file):
    """
    説明：markdown形式で出力されたファイルから各章を取り出す
    引数：markdownファイルのパス
    戻り値：章の数、リスト形式の章
    """
    with open(markedown_file, OPEN_MODE_READ) as file:
        markdown = file.read()
    html = markdown2.markdown(markdown)

    soup = BeautifulSoup(html, 'html.parser')
    h1_all = soup.find_all('h1')
    chapters_count = 0
    h1_list = []
    for h1 in h1_all:
        h1_list.append(h1.text.strip())
        chapters_count += 1

    return chapters_count, h1_list

def get_num_of_quiz(markdown_file):
    """
    説明：markdown形式で出力されたファイルから問題数を取り出す
    引数：markdownファイルのパス
    戻り値：問題数、辞書型
    """
    def extract_num_of_quiz(num_str):
        return int(re.findall(r'\d+', num_str)[0])
    
    with open(markdown_file, OPEN_MODE_READ) as file:
        markdown = file.read()
    html = markdown2.markdown(markdown)

    soup = BeautifulSoup(html, 'html.parser')
    soup = BeautifulSoup(html, 'html.parser')
    h1_all = soup.find_all('h1')
    h2_all = soup.find_all('h2')
    result = {}
    if len(h1_all) == len(h2_all):
        for i in range(len(h1_all)):
            result[h1_all[i].text.strip()] = extract_num_of_quiz(h2_all[i].text.strip())
        return result
    else:
        return ERROR_MSG05