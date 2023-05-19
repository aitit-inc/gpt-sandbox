# OpenAIのトークナイザー
# 参考：https://note.com/npaka/n/ncb4864df31c9
import tiktoken

MODEL = "cl100k_base" # text-embedding-ada-002

def token_counter(messages: list) -> int:
    num_tokens = 0
    encoder = tiktoken.get_encoding(MODEL)
    # gpt-3.5-turboの場合
    tokens_per_message = (
            4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        )
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoder.encode(value))

    return num_tokens