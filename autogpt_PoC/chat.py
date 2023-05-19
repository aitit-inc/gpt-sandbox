def create_chat_message(role: str, content: str):
    """
    role: "system", "user", "assistant" から選択
    content: 
    """
    return {"role": role, "content": content}

#def generate_context(prompt)


# 実装途中
def chat_with_ai(
        prompt, user_input, full_message_history, memory, token_limit
):
    """
    prompt: AIに対する説明
    user_input: ユーザからの入力
    full_message_history: AIとユーザの対話履歴
    token_limit:
    """
    model = "gpt-3.5-turbo"
    send_token_limit = token_limit - 1000

    relevant_memory = (
        ""
        if len(full_message_history) == 0
        else memory.get_relevant()
    )


def generate_context(prompt, relevant_memory, full_message_history=None, model=None):
    # LLMに対するコンテクストを生成（最初のシステムプロンプトと最も関連のある過去のプロンプトを渡す）
    """
    prompt: システムプロンプト
    last_memory: 直前の対話履歴を渡す
    """
    current_context = [
        create_chat_message("system", prompt),
        create_chat_message(
        "system",
        f"This reminds you of these events from your past:\n{relevant_memory}\n\n"
        ),
    ]

    return current_context