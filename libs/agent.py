from .config import *
from .message import *
from .chat import *
from .file import *


# 定数定義
TEMPERATURE = 0

class BaseAgent(object):
    """
    説明：共通クラス（実装予定）
    """
    def __init__(self, api_key, messages):
        self.api_key = api_key
        self.messages = messages



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
        write_markdown(chapters,
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
    def __init__(self, api_key, substitution, config, message_history, chapters_reply):
        self.api_key = api_key
        self.config = QuizCreatorConfig(substitution, config)
        self.messages = [] if message_history is None else message_history
        self.messages.append(
            create_chat_message(ASSISTANT_ROLE, chapters_reply)
        )
        self.messages.append(
            create_chat_message(USER_ROLE, QUIZ_NUM_PROMPT)
        )
        self.messages.append(
            create_chat_message(SYSTEM_ROLE, QUIZ_NUM_MARKDOWN)
        )
        

    # 問題数を決定
    def num_of_quiz(self):
        self.messages.append(
            create_chat_message(USER_ROLE, QUIZ_NUM_PROMPT)
        )
        assistant_reply = create_chat_completion(
            self.messages,
            temperature=TEMPERATURE,
            api_key=self.api_key
        )
        
        # 出力を確認したいので、書き出しを実行（必須処理ではない）
        write_markdown(assistant_reply, self.config.markdown_file_prefix(), self.config.markdown_filename())
        result_path = os.path.join(self.config.markdown_file_prefix(), self.config.markdown_filename())

        self.num_quiz = get_num_of_quiz(result_path)

        return self.num_quiz
    
    def create_quiz(self, num_quiz, keywords=None):
        if keywords != None:

            return None
        else:
            return None
        
    
class KeywordCreator:
    """
    説明：各章ごとにキーワードを挙げる
    """
    def __init__(self, substitution, config, api_key, chapters):
        self.api_key = api_key
        self.config = KeywordCreatorConfig(substitution, config)
        self.chapters = chapters

    def get_keywords(self, num_of_keywords, chapter):
        gen_msg = GenKeywordMessages(num_of_keywords, self.chapters, chapter)
        messages = gen_msg.create_messages()
        keyword = create_chat_completion(
            messages,
            temperature=TEMPERATURE,
            api_key=self.api_key
        )

        write_markdown(keyword, self.config.markdown_file_prefix(), self.config.markdown_filename())
        
        return keyword