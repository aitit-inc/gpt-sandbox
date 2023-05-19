import os
import markdown2
from bs4 import BeautifulSoup

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


def write_chapter(chapters, file_prefix: str, file_name: str):
    """
    説明：作成された章の構成を書き込む（.md形式を想定）
    入力：章の構成（リスト型）、ファイルを保管する場所
    出力：markdownファイルの作成
    """
    # markdownに変換
    chapters = markdown2.markdown(chapters)
    new_file = file_prefix + os.path.basename(file_name)
    # フォルダ準備
    prepare_dir(new_file)
    with open(new_file, OPEN_MODE_WRITE) as f:
        f.write(chapters)

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