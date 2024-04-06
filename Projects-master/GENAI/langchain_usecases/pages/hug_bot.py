    # https://www.analyticsvidhya.com/blog/2023/12/implement-huggingface-models-using-langchain/
import streamlit as st
from langchain.llms import HuggingFaceHub
import os

from getpass import getpass


hg=st.secrets.huggingface_api.token
os.environ["HUGGINGFACEHUB_API_TOKEN"] = hg

if hg:

    llm = HuggingFaceHub(
        repo_id="huggingfaceh4/zephyr-7b-alpha",
        model_kwargs={"temperature": 0.5, "max_length": 64,"max_new_tokens":512}
    )


    query: str = st.chat_input()

    # response = llm.predict(prompt)
    # print(response)


    # Store LLM generated responses
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    if query:
        # prompt=f"""<|system|>
        #     You are an AI assistant that follows instruction extremely well.
        #     Please be truthful and give direct answers
        #     </s>
        #      <|user|>
        #      {query}
        #      </s>
        #      <|assistant|>
        # """

        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.write(query)

        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = llm.predict(query)
                    st.write(response)

                message = {"role": "assistant", "content": response}
                st.session_state.messages.append(message)