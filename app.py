import streamlit as st
from libs.file import *


def print_chapters(markdown_file):
    num_chapters, chapters = get_chapters(markdown_file)
    st.subheader("章の構成")
    for chapter in chapters:
        st.write("- " + str(chapter))

def main():
    st.title("Quiz GPT")
    title = st.text_input(
        "問題集のタイトルを入力してください",
    )

    if title and st.button("実行"):
        with st.spinner("実行中..."):
            markdown_file = "outputs/markdown/assistant_reply.md"
            print_chapters(markdown_file)


if __name__ == "__main__":
    main()