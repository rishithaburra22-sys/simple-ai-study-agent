import streamlit as st
from google import genai

st.set_page_config(page_title="AI Study Assistant", page_icon="📚")
st.title("📚 AI Study Assistant")
st.write("Ask your questions in simple English!")

api_key = st.text_input("Enter your Gemini API key", type="password")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

question = st.chat_input("Ask a question")

if question and api_key:
    client = genai.Client(api_key=api_key)

    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        try:
            prompt = (
                "You are a friendly study assistant. "
                "Explain in simple English with examples.\n\n"
            )

            for msg in st.session_state.messages:
                prompt += msg["role"] + ": " + msg["content"] + "\n"

            response = client.models.generate_content(
                model=st.session_state.get("working_model", "gemini-3.8-flash"),
                contents=prompt
            )

            answer = response.text or "Please try again."
            st.write(answer)

            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )

        except Exception as e:
            st.error(f"AI error: {e}")

elif question:
    st.warning("Please enter your API key first.")
