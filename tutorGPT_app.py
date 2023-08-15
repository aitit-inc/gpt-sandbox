import streamlit as st
from TutorGPT.agents import TutorGPT


# タイトルの入力
def get_title():
    title = st.text_input("タイトルを入力してください")
    return title


def main():
    tutor_agent = TutorGPT()

    st.title("TutorGPT 🤖")
    st.subheader("Creating a book of questions")

    title = st.text_input("問題集のタイトルを入力してください", st.session_state["input"],
                          key="input",
                          label_visibility="hidden")
    
    if title:
        output = tutor_agent.create_table_of_contents(title=title)
        st.session_state.past.append(title)
        st.session_state.generated.append(output)

    with st.expander("Steps", expanded=True):
        for i in range(len(st.session_state["generated"])-1, -1, -1):
            st.info(st.session_state["past"][i], icon="🧐")
            st.markdown(st.session_state["generated"][i], unsafe_allow_html=True)


if __name__ == "__main__":
    st.set_page_config(page_title="TutorGPT", layout="centered")

    if "generated" not in st.session_state:
        st.session_state["generated"] = []
    if "past" not in st.session_state:
        st.session_state["past"] = []
    if "input" not in st.session_state:
        st.session_state["input"] = ""

    main()