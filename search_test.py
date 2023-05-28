from libs.googlesearch import *
import os
import re


# 必要な変数の宣言
# 検索用のテキスト
query = "python 機械学習"
# 検索するサイトの数
num_results = 1
# LLMによってテキストクレンジングを行うか
clean_with_llm = True
# 出力先のパス
output_file = "outputs/google_search/second_test.txt"


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

def main():
    shorten = False

    results = ddgsearch(query, num_results, clean_with_llm)

    with open(output_file, 'w', encoding='utf-8') as f:
        result_lines = get_results_lines(results, shorten)
        f.writelines([f"{result}\n" for result in result_lines])


if __name__ == "__main__":
    main()