from dotenv import load_dotenv
import os
from TutorGPT.agents import TutorGPT
from TutorGPT.file import *


def main():
    tutor_agent = TutorGPT()

    title = input("Title: ")
    title = title.replace("Title: ", "")

    # 目次作成
    table_of_contents = tutor_agent.create_table_of_contents(title=title)
    print(table_of_contents)

    # キーワード作成
    keywords = tutor_agent.create_keywords(table_of_contents=table_of_contents)
    print(keywords)

    # 問題文作成
    chapters = get_chapters(table_of_contents)
    chapter_idx = 0
    chapter = chapters[chapter_idx]

    questions = tutor_agent.create_questions(chapter=chapter)
    print(questions)


if __name__ == "__main__":
    main()