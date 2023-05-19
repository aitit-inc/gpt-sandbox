import streamlit as st
from config import AIConfig
from chat import create_chat_message
from utils import create_chat_completion

cfg = AIConfig("Python expert", "create great python program", ["creating python program", "improving python program", "analyzing python program"])
system_prompt = cfg.construct_full_prompt()

# 定数定義
SYSTEM_PROMPT = create_chat_message("system", system_prompt)

# 使用予定（未実装）
TRIGGERING_PROMPT = (
            "Determine which next command to use, and respond using the"
            " format specified above:"
        )

# 空のリストで対話履歴の初期化
full_messages_history = []

# セッション管理
if "generated" not in st.session_state:
    st.session_state["generated"] = []
if "past" not in st.session_state:
    st.session_state["past"] = []
if "input" not in st.session_state:
    st.session_state["input"] = ""
if "stored_session" not in st.session_state:
    st.session_state["stored_session"] = []

# サイドバー設定
with st.sidebar.expander("Config", expanded=False):
    MODEL = st.selectbox(label='Model', options=['gpt-3.5-turbo','text-davinci-003','text-davinci-002','code-davinci-002'])

# 入力関数
def user_input():
    input_text = st.text_input("You: ", st.session_state["input"], key="input",
                               placeholder="Your AI assistant here! Ask me anything about python code!",
                               label_visibility="hidden")
    return create_chat_message("user", input_text)

st.title("Python code Bot")
st.subheader("This is an experimental bot.")

st.subheader("Below is system prompt. (predetermined)")
st.info(SYSTEM_PROMPT["content"])

user_prompt = user_input()
messages = [SYSTEM_PROMPT, user_prompt]

#st.sidebar.button("New chat", on_click = create_chat_completion(messages, temperature=0), type="primary")
if st.button("generate"):
    assistant_reply = create_chat_completion(messages, temperature=0)
    st.info(assistant_reply)