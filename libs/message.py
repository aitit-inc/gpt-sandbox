from .prompt import *
from .chat import *


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
            self.system_prompt = create_chat_message(SYSTEM_ROLE, KEYWORD_SYSTEM_PROMPT_2)
            keyword_prompt = KEYWORD_PROMPT_2.format(num_of_keywords)
            self.input_prompt= create_chat_message(USER_ROLE, keyword_prompt)
            

    def create_messages(self):
        messages = [
            self.initial_prompt,
            self.system_prompt,
            self.input_prompt
        ]
        return messages