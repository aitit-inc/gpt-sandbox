from libs.agent import *
from libs.googlesearch import *
from libs.vectorstore import VectorStore
from libs import log
import logging
import os
from dotenv import load_dotenv


# 定数定義
# AIのペルソナを設定（詳細にしたほうが良い）
AI_NAME = "策定者"
AI_ROLE = "学習に適した問題集をユーザの要望に合わせて作成する"
AI_GOALS = "問題集の作成,問題集をセクションに分割する,セクションごとに各章を作成する,各章の問題数を決定する"
# 
TITLE = "Pythonではじめる機械学習入門"
# コンフィグ
CONFIG = "config.ini"
# キーワードの数
NUM_KEYWORDS = 10
# .envファイルからAPIキーを読み込む
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# Embeddingモデル
EMBEDDING_MODEL = "text-embedding-ada-002"


def web_search(search_words, query, n_results=1):
    """
    説明：ウェブ検索を行い最も関連性の高い情報を抽出
    """
    texts = split_texts(get_urls(search_words))
    substitution = {}
    vector_store = VectorStore(OPENAI_API_KEY, substitution, CONFIG)
    # ベクトルDB作成
    vector_store.create_db(texts)

    # クエリをEmbedding化
    query_embed = openai.Embedding.create(
        input=query,
        model=EMBEDDING_MODEL
    )["data"][0]["embedding"]

    query_results = vector_store.collection.query(
        query_embeddings=query_embed,
        n_results=n_results,
        include=["documents"]
    )

    return query_results["documents"][0]


def main():
    # a. 章立てを決める
    # 章構成の設定値
    substitution = {
        "AI_NAME": AI_NAME,
        "AI_ROLE": AI_ROLE,
        "AI_GOALS": AI_GOALS
    }

    chapter_creator = ChapterCreator(OPENAI_API_KEY, substitution, CONFIG, TITLE)
    # 各章を作成
    chapters = chapter_creator.create_chapters()
    # 出力確認のために保存
    chapter_creator.create_markdown_file(chapters)


    # b. 各章の問題数を決める
    # 設定値
    substitution = {}

    quiz_num_creator = DecideNumQuiz(OPENAI_API_KEY, substitution, CONFIG, chapter_creator.messages, chapters)
    
    # 問題数を決定（出力はローカルに保存される）
    num_quiz = quiz_num_creator.num_of_quiz()

    # c. 章ごとに、キーワード群を決める
    # 設定値
    substitution = {}

    keyword_creator = KeywordCreator(substitution, CONFIG, OPENAI_API_KEY, chapters)
    # キーワード群を生成（引数で数は指定可能）
    # 出力はローカルに保存される
    result_path = keyword_creator.get_keywords(NUM_KEYWORDS)
    keywords = get_keywords_from_md(result_path)

    # d. 問題を生成する
    # 設定値
    substitution = {}

    quiz_creator = QuizCreator(substitution, CONFIG, OPENAI_API_KEY, chapters)
    idx = 0
    chapter = chapter_creator.get_chapter(idx)

    quiz = quiz_creator.gen_quiz(idx, chapter, keywords)

    # 出力の書き込み
    with open("output.txt", OPEN_MODE_WRITE, encoding="utf-8") as file:
        file.write(quiz)

    return quiz


def start():
    # ログインスタンス呼び出し
    logger = log.init(logging.DEBUG)
    try:
        # 開始
        logger.info(log.LOG_START)

        output = main()


        # 終了
        logger.info(log.LOG_COMPLETE)

    except Exception:
        raise


if __name__ == "__main__":
    start()