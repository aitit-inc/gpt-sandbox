from libs.agent import *
import os
from dotenv import load_dotenv
import libs.log as libLog
import logging

# .envファイルからAPIキーを読み込む
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 定数定義
AI_NAME = "策定者"
AI_ROLE = "学習に適した問題集をユーザの要望に合わせて作成する"
AI_GOALS = "問題集の作成,問題集をセクションに分割する,セクションごとに各章を作成する,各章の問題数を決定する"
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
    quiz_creator = QuizCreator(OPENAI_API_KEY, substitution, config, chapter_creator.messages, chapters)
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
    substitution = {}
    keyword_creator = KeywordCreator(substitution, config, OPENAI_API_KEY, chapters)
    keyword = keyword_creator.gen_keywords_json(10)
    print(keyword)


def start():
    global logger

    try:
        # ログインスタンス呼び出し
        logger = libLog.init(logging.INFO)
        # 開始
        logger.info(libLog.LOG_START)

        keyword_test()

        # 終了
        logger.info(libLog.LOG_COMPLETE)

    except Exception:
        raise


if __name__ == "__main__":
    start()