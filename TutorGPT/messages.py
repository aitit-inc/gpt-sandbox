from pydantic import BaseModel
from .prompts import *


# 定数定義
SYSTEM_ROLE = "system"
ASSISTANT_ROLE = "assistant"
USER_ROLE = "user"


class Messages(BaseModel):
    ai_name: str = "TutorGPT"
    ai_role: str = "tutor of creating a book of questions"


    def construct_start_messages(self, title: str) -> list:
        triggering_prompt = TRIGGERING_PROMPT.format(
            ai_name=self.ai_name,
            ai_role=self.ai_role,
            conversation_history="None"
        )
        start_prompt = START_PROMPT.format(
            title=title,
        )

        return [
            create_chat_message(role=SYSTEM_ROLE, content=triggering_prompt),
            create_chat_message(role=USER_ROLE, content=start_prompt)
        ]

    def keyword_messages(self, conversation_history: list) -> list:
        conversation_history = "\n".join(conversation_history)
        triggering_prompt = TRIGGERING_PROMPT.format(
            ai_name=self.ai_name,
            ai_role=self.ai_role,
            conversation_history=conversation_history
        )
        return [
            create_chat_message(role=SYSTEM_ROLE, content=triggering_prompt),
            create_chat_message(role=USER_ROLE, content=KEYWORD_PROMPT_BETA)
        ]
    
    def question_messages(self, conversation_history: list, chapter: str) -> list:
        conversation_history = "\n".join(conversation_history)
        triggering_prompt = TRIGGERING_PROMPT.format(
            ai_name=self.ai_name,
            ai_role=self.ai_role,
            conversation_history=conversation_history
        )
        question_prompt = QUESTION_PROMPT.format(chapter)
        return [
            create_chat_message(role=SYSTEM_ROLE, content=triggering_prompt),
            create_chat_message(role=USER_ROLE, content=question_prompt)
        ]


    @classmethod
    def setup(cls, cf):
        return cls(ai_name=cf.ai_name, ai_role=cf.ai_role)


def create_chat_message(role: str, content: str) -> dict:
    """
    チャットメッセージを作成する
    """
    return {"role": role, "content": content}