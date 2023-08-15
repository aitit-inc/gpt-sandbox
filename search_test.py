from libs.googlesearch import *
from libs.agent import *
import os
import re
from dotenv import load_dotenv


# .envファイルからAPIキーを読み込む
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# 必要な変数の宣言
# 検索用のテキスト
query = "python 機械学習"
# 検索するサイトの数
num_results = 1
# LLMによってテキストクレンジングを行うか
clean_with_llm = True
# 出力先のパス
output_file = "outputs/google_search/summary_test.txt"
AI_NAME = "策定者"
AI_ROLE = "学習に適した問題集をユーザの要望に合わせて作成する"
AI_GOALS = "問題集の作成,問題集をセクションに分割する,セクションごとに各章を作成する,各章の問題数を決定する"
TITLE = "Pythonではじめる機械学習入門"


def get_results_lines(results, shorten):
    result_lines = []
    for index, results in enumerate(results):
        result_lines.append("**************************************")
        result_lines.append(f"Result {index+1}")
        result_lines.append(f"URL: {results['url']}")
        result_lines.append(f"Title: {results['title']}")
        # 出力を短くするかどうか
        if shorten:
            result_lines.append("Cleaned Text (shortened):")
            useful_lines = results['useful_text'].splitlines()[:20]
            short_useful_text = '\n'.join(useful_lines)
            result_lines.append(short_useful_text)
        else:
            result_lines.append("Cleaned Text :")
            result_lines.append(results['useful_text'])
            result_lines.append("Full Text:")
            result_lines.append(results['text'])
        result_lines.append("**************************************")
        result_lines.append('')
    return result_lines

def summary():
    substitution = {
        "AI_NAME": AI_NAME,
        "AI_ROLE": AI_ROLE,
        "AI_GOALS": AI_GOALS
    }
    config = "config.ini"
    chapter_creator = ChapterCreator(OPENAI_API_KEY, substitution, config, TITLE)
    chapters = chapter_creator.create_chapters()
    chapter = chapter_creator.get_chapter(0)
    results = gpt_search(chapters, chapter, clean_with_llm)
    return results

def main():
    shorten = False

    # results = ddgsearch(query, num_results, clean_with_llm)
    results = summary()

    with open(output_file, 'w', encoding='utf-8') as f:
        result_lines = get_results_lines(results, shorten)
        f.writelines([f"{result}\n" for result in result_lines])


if __name__ == "__main__":
    main()