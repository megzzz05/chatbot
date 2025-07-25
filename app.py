import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
base_url = os.getenv("GROQ_BASE_URL")

client = OpenAI(
    api_key=api_key,
    base_url=base_url,
)

st.set_page_config(page_title="Groq Chatbot", layout="centered")
st.title("🤖 Chat with Groq LLM")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Say something...")

if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=st.session_state.messages,
                temperature=0.7,
                stream=True,
            )

            placeholder = st.empty()
            full_response = ""

            for chunk in response:
                content = chunk.choices[0].delta.content or ""
                full_response += content
                placeholder.markdown(full_response + "▌")

            placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})