import streamlit as st
from libs.agent import *
from dotenv import load_dotenv
import os


# .envファイルからAPIキーを読み込む
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# 定数定義
AI_NAME = "問題集を作成する教師"
AI_ROLE = "学習に適した問題集をユーザの要望に合わせて作成する"
AI_GOALS = "問題集の作成,問題集を目次を作成する,問題集の各章と各節を作成する,各章の問題数を決定する,各章のキーワードを決定する,問題を作成する"
CONFIG = "config.ini"


# タイトルの入力
def get_title():
    title = st.text_input("タイトルを入力してください", placeholder="Pythonではじめる機械学習入門")
    return title

# 章の構成を表示
def show_markdown(result_path: str):
    with open(result_path, "r") as f:
        markdown_text = f.read()
    st.markdown(markdown_text, unsafe_allow_html=True)


# Streamlit
def main():
    if "start" not in st.session_state:
        st.session_state.start = False

    st.title("問題集自動生成アプリ")
    st.subheader("AIアシスタントによる問題集自動生成アプリです。")

    title = get_title()

    # start_button = st.button("問題集の目次を作成する", key=0)

    if st.button("問題集の目次を作成する", key=0):
        substitution = {
        "AI_NAME": AI_NAME,
        "AI_ROLE": AI_ROLE,
        "AI_GOALS": AI_GOALS
        }
        chapter_creator = ChapterCreator(OPENAI_API_KEY, substitution, CONFIG, title)
        chapters = chapter_creator.create_chapters()
        chapter_creator.create_markdown_file(chapters)
        result_path = chapter_creator.config.markdown_file_prefix() + os.path.basename(chapter_creator.config.markdown_filename())
        show_markdown(result_path)
        st.session_state.start = True
    
    while st.session_state.start:
        if st.button("キーワードを生成する", key=1):
            st.session_state.start = False
        num_of_keywords = st.number_input("キーワードの数を入力してください", min_value=1, max_value=10, value=1)
        chapter_idx = st.number_input("章番号を入力してください", value=0)
        keyword_creator = KeywordCreator({}, CONFIG, OPENAI_API_KEY, chapters)
        chapter = chapter_creator.get_chapter(chapter_idx)
        result_path = keyword_creator.get_keywords(num_of_keywords, chapter=chapter)
        show_markdown(result_path)


if __name__ == "__main__":
    main()