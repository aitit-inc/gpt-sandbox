import os
import sys
from configparser import ConfigParser
from .error_message import *
from .prompt import *
import json

# 定数定義
OPEN_MODE_READ = 'r'

# TODO AutoGPTを参考にした環境設定クラスの構築

class ClsConfiger(object):
    """
    説明：環境設定ファイルの読み込み
    入力：config.ini, 設定値
    出力：環境変数
    """
    def __init__(self, substitution, config_file):
        # 設定変数
        self.substitution = substitution
        self.configparser = ConfigParser()
        try:
            # ファイル読み取り
            self.configparser.read(config_file)
        except Exception:
            # 読み取りエラー
            raise Exception(ERROR_MSG01.format(config_file))
        
    def get(self, *arg):
        try:
            return self.configparser.get(*arg).replace("\\", os.path.sep).replace("/", os.path.sep).format(**self.substitution)
        except Exception:
            # 設定値エラー
            raise Exception(ERROR_MSG02.format(arg[0], arg[1]))
        

# 章構成の設定クラス
class ChapterCreatorConfig(ClsConfiger):
    """
    説明：最初のセットアップ
    """
    def __init__(self, substitution, config_file):
        super().__init__(substitution, config_file)
        # AIの名前
        self.ai_name = super().get(self.__class__.__name__, 'ai_name')
        # AIの役割（詳細に）
        self.ai_role = super().get(self.__class__.__name__, 'ai_role')
        # AIの達成目標（リスト形式）
        str_ai_goals = super().get(self.__class__.__name__, 'ai_goals')
        self.ai_goals = str_ai_goals.split(',')

    def construct_prompt(self):
        full_prompt = (
            f"あなたは{self.ai_name}であり、役割は{self.ai_role}\n{SYSTEM_PROMPT}\n\n目標:\n\n"
        )
        for i, goal in enumerate(self.ai_goals):
            full_prompt += f"{i+1}. {goal}\n"

        # 手順を指定する（検証）
        full_prompt += (
            """
            下記は、あなたが目的を達成するために必要な手順です。\n
            1. 問題集の各章の構成を決定する\n
            2. 各章あたりに適切な問題数を決定する\n
            3. 各章に対して、キーワード群を生成する\n
            4. 各章に対して、問題を生成する\n
            """
        )

        return full_prompt
    
    def markdown_file_prefix(self):
        return super().get(self.__class__.__name__, sys._getframe().f_code.co_name)
    
    def markdown_filename(self):
        return super().get(self.__class__.__name__, sys._getframe().f_code.co_name)
    

# 問題文生成の設定クラス
class DecideNumQuizConfig(ClsConfiger):
    def __init__(self, substitution, config_file):
        super().__init__(substitution, config_file)

    def markdown_file_prefix(self):
        return super().get(self.__class__.__name__, sys._getframe().f_code.co_name)
    
    def markdown_filename(self):
        return super().get(self.__class__.__name__, sys._getframe().f_code.co_name)
    
# キーワード生成の設定クラス
class KeywordCreatorConfig(ClsConfiger):
    def __init__(self, substitution, config_file):
        super().__init__(substitution, config_file)

    def markdown_file_prefix(self):
        return super().get(self.__class__.__name__, sys._getframe().f_code.co_name)
    
    def markdown_filename(self):
        return super().get(self.__class__.__name__, sys._getframe().f_code.co_name)
    
    def json_file_prefix(self):
        return super().get(self.__class__.__name__, sys._getframe().f_code.co_name)
    
    def json_filename(self):
        return super().get(self.__class__.__name__, sys._getframe().f_code.co_name)
    
    def test_markdown_prefix(self):
        return super().get(self.__class__.__name__, sys._getframe().f_code.co_name)
    
    def test_markdown_filename(self):
        return super().get(self.__class__.__name__, sys._getframe().f_code.co_name)

# 問題生成の設定クラス
class QuizCreatorConfig(ClsConfiger):
    def __init__(self, substitution, config_file):
        super().__init__(substitution, config_file)

    def json_file_prefix(self):
        return super().get(self.__class__.__name__, sys._getframe().f_code.co_name)
    
    def json_filename(self):
        return super().get(self.__class__.__name__, sys._getframe().f_code.co_name)


# Chromadbの設定クラス
class ChromaConfig(ClsConfiger):
    def __init__(self, substitution, config_file):
        super().__init__(substitution, config_file)

    def collection_name(self):
        return super().get(self.__class__.__name__, sys._getframe().f_code.co_name)
    
    def persistant_directory(self):
        return super().get(self.__class__.__name__, sys._getframe().f_code.co_name)
    

# 現在は使用していない
class JsonReader(object):
    """
    説明：JSONファイルの読み取り
    入力：JSONファイル
    """
    def __init__(self, json_file):
        try:
            # JSON読み取り
            with open(json_file, OPEN_MODE_READ) as f:
                self.json = json.load(f)
        except Exception:
            # 読み取りエラー
            raise Exception(ERROR_MSG03.format(json_file))
        
    def get(self, key):
        return self.json[key]

class Prompt(JsonReader):
    def __init__(self, json_file):
        super().__init__(json_file)

    def system_prompt(self):
        return super().get("system_prompt")
    
    def input_prompt(self):
        return super().get("input_prompt")
    
    def final_prompt(self):
        return super().get("final_prompt")
    