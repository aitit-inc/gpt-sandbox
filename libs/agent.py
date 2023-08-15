from .config import *
from .message import *
from .chat import *
from .file import *
from .googlesearch import *
import random
import logging


# ログ設定
logger = logging.getLogger(__name__)


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
        # self.messages = ms_cl.create_messages()
        self.messages = ms_cl.create_messages_ver2()

    def create_chapters(self):
        assistant_reply = create_chat_completion(
            self.messages,
            temperature=TEMPERATURE,
            api_key=self.api_key,
            model="gpt-4"
        )
        return assistant_reply

    def create_markdown_file(self, chapters):
        # chaptersはマークダウンファイルのパス
        write_markdown(chapters,
                      self.config.markdown_file_prefix(),
                      self.config.markdown_filename())
        
    def get_chapter(self, idx):
        # markdown出力した場合のみ有効
        file_path = self.config.markdown_file_prefix() + self.config.markdown_filename()
        _, chapters = get_chapters(file_path)
        return chapters[idx]
    
# TODO 出力形式を選択（問題の形式）
class DecideNumQuiz:
    """
    説明：問題数を決定する
    """
    def __init__(self, api_key, substitution, config, message_history, chapters_reply):
        self.api_key = api_key
        self.config = DecideNumQuizConfig(substitution, config)
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
        

# TODO ウェブ検索からのキーワードの追加
class KeywordCreator:
    """
    説明：各章ごとにキーワードを挙げる
    """
    def __init__(self, substitution, config, api_key, chapters):
        self.api_key = api_key
        self.config = KeywordCreatorConfig(substitution, config)
        self.chapters = chapters

    def get_keywords(self, num_of_keywords, chapter=None):
        gen_msg = GenKeywordMessages(num_of_keywords, self.chapters, chapter)
        messages = gen_msg.create_messages()
        keyword = create_chat_completion(
            model="gpt-4",
            messages=messages,
            temperature=TEMPERATURE,
            api_key=self.api_key
        )

        write_markdown(keyword, self.config.markdown_file_prefix(), self.config.markdown_filename())
        result_path = self.config.markdown_file_prefix() + os.path.basename(self.config.markdown_filename())

        return result_path
    
    
    # json形式でキーワードの生成を行う（バグ解決中）
    # ステータス：未決
    def gen_keywords_json(self, num_of_keywords):
        gen_msg = GenKeywordMessages(num_of_keywords, self.chapters)
        messages = gen_msg.create_messages()
        keyword = create_chat_completion(
            messages,
            temperature=TEMPERATURE,
            api_key=self.api_key
        )
        json_file = os.path.join(self.config.json_file_prefix(), self.config.json_filename())
        write_json(keyword, json_file)

        return keyword
    
    # ウェブ検索からのキーワードを追加する
    # 各章のタイトルからキーワードを抽出する
    def add_keywords_from_web_search(self, title, chapter_idx, num_of_keywords=1):
        # 開始ログ
        logger.info("処理開始：ウェブ検索からのキーワード検出")
        messages = []
        chapter = self.chapters[chapter_idx]
        # 問題集のタイトルで検索を行い、各章のタイトルに関連の高い情報を抽出する
        search_result = web_search(title, chapter)
        # 試作段階なので、ハードコーディング
        prompt = f"""
        これは問題集のタイトル：{title}\n
        これは問題集の章：{chapter}\n
        下記の文章はウェブ検索によって抽出された文章です。\n
        --------------------------------------------------\n
        {search_result}\n
        --------------------------------------------------\n
        この文章から、問題集の章に関連すると思われるキーワードを抽出してください。\n
        """
        messages.append(create_chat_message(USER_ROLE, prompt))
        # 出力制御用のプロンプト
        system_prompt = (
            "各章と関連する語句の出力の形式は以下のmarkdown形式に合致させなさい。\n"
            "<h1>第n章</h1>\n"
            "<h2>word_1, word_2, ...word_n</h2>\n"
        )
        messages.append(create_chat_message(SYSTEM_ROLE, system_prompt))

        additional_keywords = create_chat_completion(
            messages,
            temperature=TEMPERATURE,
            api_key=self.api_key
        )

        # 結果確認ログ
        logger.info(f"ChatGPTの出力：{additional_keywords}")

        write_markdown(additional_keywords, self.config.test_markdown_prefix(), self.config.test_markdown_filename())
        result_path = self.config.test_markdown_prefix() + self.config.test_markdown_filename()

        logger.info("処理終了")
        
        return result_path


class QuizCreator:
    # TODO 問題数でループして各章の問題を生成
    # 現在は問題生成のみGPT-4を使用
    def __init__(self, substitution, config, api_key, model="gpt-3.5-turbo", message_history=None):
        self.api_key = api_key
        self.config = QuizCreatorConfig(substitution, config)
        self.memory = [] if message_history is None else message_history
        if model == "gpt-4":
            self.token_limit = 8000
        else:
            self.token_limit = 4000
        self.model = model
        
    # # ランダムな語句を抽出
    # def random_words(keywordlist):
    #     num_of_words = random.randint(1, len(keywordlist))
    #     return random.sample(keywordlist, num_of_words)

    def gen_quiz(self, idx, chapter, keywords):
        keyword_list = keywords[chapter]
        num_of_words = random.randint(1, len(keyword_list))
        keyword_list = random.sample(keyword_list, num_of_words)
        gen_msg = QuizMessages(self.memory, idx, keyword_list)
        msg = gen_msg.create_messages()
        # 未使用変数
        # num_quiz = num_quizes[chapter]
        assistant_reply = create_chat_completion(
            msg,
            temperature=TEMPERATURE,
            api_key=self.api_key,    
        )

        # json出力
        json_path = os.path.join(self.config.json_file_prefix(), self.config.json_filename())
        write_json(assistant_reply, json_path)

        return assistant_reply
    
    def gen_quiz_with_search(self, idx, chapter, keywords, search_result):
        keyword_list = keywords[chapter]
        num_of_words = random.randint(1, len(keyword_list))
        keyword_list = random.sample(keyword_list, num_of_words)
        gen_msg = QuizMessages(self.memory, idx, keyword_list, search_result)
        msg, current_token_used = gen_msg.create_messages_include_search()
        num_tokens = self.token_limit - current_token_used
        assistant_reply = create_chat_completion(
            msg,
            temperature=TEMPERATURE,
            api_key=self.api_key,
            max_tokens=num_tokens,
            model=self.model
        )

        return assistant_reply