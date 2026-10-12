
import streamlit as st
from google import genai

st.set_page_config(page_title="AI Study Assistant", page_icon="📚")

st.title("📚 AI Study Assistant")
st.write("Ask your questions in simple English!")

api_key = st.text_input(
    "Enter your Gemini API key",
    type="password"
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

question = st.chat_input("Ask a study question...")

if question:
    if not api_key:
        st.warning("Please enter your Gemini API key.")
    else:
        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):
            try:
                client = genai.Client(api_key=api_key)

                with st.spinner("Finding an available AI model..."):
                    available = []

                    for model in client.models.list():
                        name = model.name.replace("models/", "")
                        actions = model.supported_actions or []

                        if "generateContent" in actions:
                            available.append(name)

                    preferred = [
                        "gemini-3.8-flash",
                        "gemini-3.7-flash",
                        "gemini-3.6-flash",
                        "gemini-3.5-flash-lite",
                    ]

                    models = [
                        m for m in preferred if m in available
                    ]

                    models += [
                        m for m in available if m not in models
                    ]

                answer = None

                for model in models:
                    try:
                        result = client.models.generate_content(
                            model=model,
                            contents=(
                                "You are a friendly study assistant. "
                                "Explain in simple English with examples.\n\n"
                                + question
                            )
                        )

                        if result.text:
                            answer = result.text
                            break

                    except Exception as error:
                        st.write(
                            f"Trying another model after an error "
                            f"with {model}."
                        )

                if answer:
                    st.write(answer)
                    st.session_state.messages.append(
                        {"role": "user", "content": question}
                    )
                    st.session_state.messages.append(
                        {"role": "assistant", "content": answer}
                    )
                else:
                    st.error(
                        "No available model answered. Please check "
                        "your Google AI Studio API key, model access, "
                        "and usage limits."
                    )

            except Exception as error:
                st.error(
                    "Could not connect to the AI service. "
                    "Please check your API key and try again."
                )
