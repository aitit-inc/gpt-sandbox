from .config import *
from .message import *
from .chat import *
from .file import *


# 定数定義
TEMPERATURE = 0

class ChapterCreator:
    """
    説明：章の構成を作成する
    """
    def __init__(self, api_key, substitution, config_file, title):
        self.api_key = api_key
        self.config = ChapterCreatorConfig(substitution, config_file)
        ms_cl = ChapterMessages(self.config, title)
        self.messages = ms_cl.create_messages()

    def create_chapters(self):
        assistant_reply = create_chat_completion(
            self.messages,
            temperature=TEMPERATURE,
            api_key=self.api_key
        )
        return assistant_reply

    def create_markdown_file(self, chapters):
        # chaptersはマークダウンファイルのパス
        write_chapter(chapters,
                      self.config.markdown_file_prefix(),
                      self.config.markdown_filename())
        
    def get_chapter(self, idx):
        file_path = self.config.markdown_file_prefix() + self.config.markdown_filename()
        _, chapters = get_chapters(file_path)
        return chapters[idx]

class QuizCreator:
    """
    説明：問題を生成する
    """
    def __init__(self, api_key, message_history, chapters_reply):
        self.api_key = api_key
        self.messages = [] if message_history is None else message_history
        self.messages.append(
            create_chat_message(ASSISTANT_ROLE, chapters_reply)
        )
        self.messages.append(
            create_chat_message(USER_ROLE, QUIZ_NUM_PROMPT)
        )
        

    # 問題数を決定
    def num_of_quiz(self):
        self.messages.append(
            create_chat_message(USER_ROLE, QUIZ_NUM_PROMPT)
        )
        num_quiz = create_chat_completion(
            self.messages,
            temperature=TEMPERATURE,
            api_key=self.api_key
        )
        return num_quiz
    
class KeywordCreator:
    def __init__(self, api_key):
        self.api_key = api_key
