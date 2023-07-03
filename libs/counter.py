import tiktoken


# 定数定義
MODEL = "cl100k_base"

def token_counter(messages: list) -> int:
    num_tokens = 0
    encoder = tiktoken.get_encoding(MODEL)
    # gpt-3.5-turboの場合
    # TODO gpt-4 を使う場合の分岐処理
    tokens_per_message = (
            4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        )
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoder.encode(value))
    num_tokens += 3
    return num_tokens