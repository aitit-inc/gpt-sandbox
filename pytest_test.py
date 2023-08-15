from libs.agent import *
import os
import json
from dotenv import load_dotenv
import libs.log as libLog
import logging
from libs.googlesearch import *

# .envファイルからAPIキーを読み込む
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 定数定義
AI_NAME = "問題集を作成する教師"
AI_ROLE = "学習に適した問題集をユーザの要望に合わせて作成する"
AI_GOALS = "問題集の作成,問題集を目次を作成する,問題集の各章と各節を作成する,各章の問題数を決定する,各章のキーワードを決定する,問題を作成する"
TITLE = "Pythonではじめる機械学習入門"


#########################  単体テスト  #########################
def test_class():
    # 章の構成を作成するクラスのテスト
    substitution = {
        "AI_NAME": AI_NAME,
        "AI_ROLE": AI_ROLE,
        "AI_GOALS": AI_GOALS
    }
    config = "config.ini"
    creator = ChapterCreator(OPENAI_API_KEY, substitution, config, TITLE)
    chapters = creator.create_chapters()
    print(chapters)
    creator.create_markdown_file(chapters)


#########################  結合テスト  #########################
def main():
    substitution = {
        "AI_NAME": AI_NAME,
        "AI_ROLE": AI_ROLE,
        "AI_GOALS": AI_GOALS
    }
    config = "config.ini"
    chapter_creator = ChapterCreator(OPENAI_API_KEY, substitution, config, TITLE)
    chapters = chapter_creator.create_chapters()
    substitution = {}
    quiz_creator = DecideNumQuiz(OPENAI_API_KEY, substitution, config, chapter_creator.messages, chapters)
    num_quiz = quiz_creator.num_of_quiz()
    print(num_quiz)

def keyword_test():
    substitution = {
        "AI_NAME": AI_NAME,
        "AI_ROLE": AI_ROLE,
        "AI_GOALS": AI_GOALS
    }
    config = "config.ini"
    chapter_creator = ChapterCreator(OPENAI_API_KEY, substitution, config, TITLE)
    chapters = chapter_creator.create_chapters()
    chapter = chapter_creator.get_chapter(0)
    num_of_keywords = 10
    substitution = {}
    keyword_creator = KeywordCreator(substitution, config, OPENAI_API_KEY, chapters)
    result_path = keyword_creator.get_keywords(num_of_keywords, chapter=chapter)
    # result_path = keyword_creator.add_keywords_from_web_search(TITLE, 0)
    keywords = get_keywords_from_md(result_path)
    print(keywords)


def websearch_test():
    substitution = {
        "AI_NAME": AI_NAME,
        "AI_ROLE": AI_ROLE,
        "AI_GOALS": AI_GOALS
    }
    config = "config.ini"
    chapter_creator = ChapterCreator(OPENAI_API_KEY, substitution, config, TITLE)
    chapters = chapter_creator.create_chapters()
    chapter = chapter_creator.get_chapter(0)
    url_response = get_useful_urls(chapters, chapter)
    data = json.loads(url_response)
    print(data)
    print(type(data))

    return data['urls']


def quiz():
    config = 'config.ini'
    substitution = {
        "AI_NAME": AI_NAME,
        "AI_ROLE": AI_ROLE,
        "AI_GOALS": AI_GOALS
    }
    config = "config.ini"
    chapter_creator = ChapterCreator(OPENAI_API_KEY, substitution, config, TITLE)
    chapters_msg = chapter_creator.create_chapters()
    chapter_creator.create_markdown_file(chapters_msg)
    idx = 0
    chapter = chapter_creator.get_chapter(idx)
    substitution = {}
    keyword_creator = KeywordCreator(substitution, config, OPENAI_API_KEY, chapters_msg)
    keyword = keyword_creator.get_keywords(10)
    path = 'outputs/markdown/keyword.md'
    keywords = get_keywords_from_md(path)
    quiz_creator = QuizCreator(substitution, config, OPENAI_API_KEY, chapters_msg)
    quiz = quiz_creator.gen_quiz(idx, chapter, keywords)
    print(quiz)


def start():
    # log_level = "libs.agent.KeywordCreator"

    try:
        # ログインスタンス呼び出し
        # logging.basicConfig()
        # logging.getLogger(log_level)

        # テスト実行
        keyword_test()
        
    except Exception:
        raise


if __name__ == "__main__":
    start()