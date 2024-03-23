import streamlit as st
import transformers
from transformers import pipeline
# from streamlit import caching
from transformers import pipeline, Conversation

# Load the pre-trained model from Hugging Face
# chatbot_model = pipeline("conversational")  ##microsoft/DialoGPT-medium
chatbot_model = pipeline(model="facebook/blenderbot-400M-distill")  ##microsoft/DialoGPT-medium

# Define the Streamlit app state using SessionState
class SessionState:
    def __init__(self):
        self.conversation = []

# Function to generate bot response
def respond_to_user_input(user_input, session_state):
    conversation_history = [{"role": "system", "content": "You are a helpful assistant."}]
    for message in session_state.conversation:
        conversation_history.append({"role": "user", "content": message})

    bot_response = chatbot_model(
        user_input,
        conversation_history=conversation_history
    )

    session_state.conversation.append(user_input)
    session_state.conversation.append(bot_response['choices'][0]['message']['content'])

    return bot_response['choices'][0]['message']['content']

# Streamlit UI
def main():
    st.title("Chatbot with Hugging Face Model")

    # Create a unique key for caching based on user input
    # cache_key = "chatbot_cache_key" + st.text_input("Key")

    # Initialize or get the SessionState
    session_state = SessionState()

    # Conversation history
    st.write("Conversation History:")
    for i in range(0, len(session_state.conversation), 2):
        st.write(f"User: {session_state.conversation[i]}")
        st.write(f"Bot: {session_state.conversation[i + 1]}")
        st.write("------")

    # User input
    user_input = st.text_input("You:")
    if st.button("Send"):
        if user_input:
            response = respond_to_user_input(user_input, session_state)
            st.text_area("Bot:", response)

    # Clear conversation button
    if st.button("Clear Conversation"):
        session_state.conversation = []
        # caching.clear_cache()

if __name__ == "__main__":
    main()
