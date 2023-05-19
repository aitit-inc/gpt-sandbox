from .error_message import *
from .prompt import *
import openai


# 定数定義
SYSTEM_ROLE = "system"
ASSISTANT_ROLE = "assistant"
USER_ROLE = "user"

def create_chat_message(role: str, content: str):
    """
    説明：メッセージを生成
    入力：role（system, user, assistant）content（内容）
    """
    return {"role": role, "content": content}


# メインでGPTに入力を渡す関数
def create_chat_completion(
        messages: list,
        temperature: float,
        api_key: str,
        max_tokens=2500, 
        model="gpt-3.5-turbo", # デフォルトはChatGPT
) -> str:
    """
    説明：OpenAIのChat Completion APIによってAIからの回答を生成
    """
    response = None
    openai.api_key = api_key
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
    except Exception:
        raise Exception(ERROR_MSG04)

    return response.choices[0].message["content"]


# 現時点では未使用
# コンテクスト生成
def generate_context(assistant_reply, message_history, relevant_memory):
    assistant_prompt = create_chat_message(ASSISTANT_ROLE, assistant_reply)
    triggering_prompt = TRIGGERING_PROMPT.format(relevant_memory)
    current_context = (
        message_history + assistant_prompt + triggering_prompt
    )
    return current_context