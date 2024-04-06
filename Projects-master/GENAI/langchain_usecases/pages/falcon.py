import streamlit as st


from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from decouple import config
from langchain.memory import ConversationBufferWindowMemory
from langchain_community.llms import HuggingFaceHub




prompt = PromptTemplate(
    input_variables=["question"],
    template= """Question: {question}

Answer: Let's think step by step."""
)
# ,
# llm=HuggingFaceHub(repo_id='tiiuae/falcon-7b-instruct',huggingfacehub_api_token="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")
llm=HuggingFaceHub(repo_id="huggingfaceh4/zephyr-7b-alpha",huggingfacehub_api_token="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")

# memory = ConversationBufferWindowMemory(memory_key="chat_history", k=4)
llm_chain = LLMChain(
    llm=llm,
    # memory=memory,
    prompt=prompt
)

st.set_page_config(
    page_title="ChatGPT Clone",
    page_icon="🤖",
    layout="wide"
)

st.set_page_config(
    page_title="ChatGPT Clone",
    page_icon="🤖",
    layout="wide"
)
st.title("ChatGPT Clone")

# check for messages in session and create if not exists
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello there, am ChatGPT clone"}
    ]

# Display all messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_prompt = st.chat_input()

if user_prompt is not None:
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.write(user_prompt)

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Loading..."):
            ai_response = llm_chain.run(question=user_prompt)
            st.write(ai_response)
    new_ai_message = {"role": "assistant", "content": ai_response}
    st.session_state.messages.append(new_ai_message)