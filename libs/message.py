from .prompt import *
from .chat import *
from .counter import token_counter


# 定数定義
SYSTEM_ROLE = "system"
ASSISTANT_ROLE = "assistant"
USER_ROLE = "user"

class ChapterMessages:
    def __init__(self, config, title):
        initial_prompt = config.construct_prompt()
        self.initial_prompt = create_chat_message(SYSTEM_ROLE, initial_prompt)
        self.system_prompt = create_chat_message(SYSTEM_ROLE, SYSTEM_PROMPT)
        self.start_prompt = create_chat_message(SYSTEM_ROLE, START_PROMPT.format(title))
        self.chapter_prompt = create_chat_message(USER_ROLE, CHAPTER_PROMPT)
        self.markdown_prompt = create_chat_message(USER_ROLE, MARKDOWN_PROMPT)

    def create_messages(self):
        # 最初のメッセージリストを生成
        messages = [
            self.initial_prompt,
            self.system_prompt,
            self.start_prompt,
            self.chapter_prompt,
            self.markdown_prompt
        ]
        return messages
    
class GenKeywordMessages:
    def __init__(self, num_of_keywords, chapter_messages, chapter=None):
        triggering_prompt = TRIGGERING_PROMPT.format(chapter_messages)
        self.initial_prompt = create_chat_message(SYSTEM_ROLE, triggering_prompt)
        if chapter is not None:
            self.system_prompt = create_chat_message(SYSTEM_ROLE, KEYWORD_SYSTEM_PROMPT)
            keyword_prompt = KEYWORD_PROMPT.format(chapter, num_of_keywords)
            self.input_prompt = create_chat_message(USER_ROLE, keyword_prompt)
        else:
            self.system_prompt = create_chat_message(SYSTEM_ROLE, KEYWORD_SYSTEM_PROMPT)
            keyword_prompt = KEYWORD_PROMPT_2.format(num_of_keywords)
            self.input_prompt= create_chat_message(USER_ROLE, keyword_prompt)
            

    def create_messages(self):
        messages = [
            self.initial_prompt,
            self.input_prompt,
            self.system_prompt
        ]
        return messages
    
class QuizMessages:
    def __init__(self, memory, idx, keyword_list, web_search_text=None):
        triggering_prompt = TRIGGERING_PROMPT.format(memory)
        self.initial_prompt = create_chat_message(SYSTEM_ROLE, triggering_prompt)
        # self.system_prompt = create_chat_message(SYSTEM_ROLE, QUIZ_SYSTEM_PROMPT)
        self.system_prompt = create_chat_message(SYSTEM_ROLE, QUIZ_SYSTEM_PROMPT_WEB)
        quiz_prompt = QUIZ_PROMPT.format(idx+1)
        for keyword in keyword_list:
            quiz_prompt += f"{keyword}\n"
        self.quiz_prompt = create_chat_message(USER_ROLE, quiz_prompt)
        self.system_prompt_2 = create_chat_message(SYSTEM_ROLE, QUIZ_FORMAT_PROMPT)
        # TODO 検索結果を１件しか参照していないので、改善の余地あり
        search_result  = WEB_SEARCH_PROMPT.format(web_search_text) if web_search_text is not None else None
        self.search_prompt = create_chat_message(SYSTEM_ROLE, search_result)

    def create_messages(self):
        messages = [
            self.initial_prompt,
            self.system_prompt,
            self.quiz_prompt,
            self.system_prompt_2
        ]
        return messages
    
    def create_messages_include_search(self):
        messages = [
            self.initial_prompt,
            self.search_prompt,
            self.system_prompt,
            self.quiz_prompt,
            self.system_prompt_2
        ]
        current_token_used = token_counter(messages)
        # 出力確認
        print(f"現在使用中のトークン数：{current_token_used}")
        return messages, current_token_used