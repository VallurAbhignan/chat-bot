import streamlit as st
from main import ask_bot, generate_questions, save_chat_history, load_chat_history

st.set_page_config("Interview Prep Bot", layout="wide")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

mode = st.sidebar.radio("Choose Mode", ["Practice", "Interview"])

st.sidebar.markdown("### Clear & View History")
if st.sidebar.button("🗑️ Clear History"):
    st.session_state.chat_history = []

if st.sidebar.button("📖 View Previous Q&A"):
    if st.session_state.chat_history:
        st.markdown("### Previous Questions:")
        for idx, qa in enumerate(st.session_state.chat_history):
            st.markdown(f"**{idx+1}. {qa['question']}**")
            st.markdown(f"- Answer: {qa['answer']}")
    else:
        st.info("No history yet.")

st.title("🤖 ChatGPT-Style Interview Preparation Bot")

if mode == "Interview":
    st.subheader("Ask anything, the bot will answer like in an interview.")

    user_input = st.text_input("Your question:")
    model = "llama3-70b-8192"

    if st.button("Ask"):
        if user_input:
            answer = ask_bot(user_input, model)
            st.markdown(f"🧑 **You**: {user_input}")
            st.markdown(f"🤖 **Bot**: {answer}")
            st.session_state.chat_history.append({"question": user_input, "answer": answer})

elif mode == "Practice":
    st.subheader("Practice Mode - Generate Questions")

    domain = st.text_input("Enter Domain (e.g., DBMS, Networking):")
    difficulty = st.selectbox("Select Difficulty", ["Easy", "Medium", "Hard"])
    num_questions = st.slider("Number of Questions", 1, 10, 5)

    if st.button("Generate"):
        if domain:
            questions = generate_questions(domain, difficulty, num_questions)
            if not questions:
                st.warning("No questions generated.")
            else:
                st.session_state.chat_history.extend(questions)
                for idx, qa in enumerate(questions, 1):
                    with st.expander(f"Q{idx}: {qa['question']}"):
                        st.markdown(qa['answer'])
        else:
            st.warning("Please enter a domain.")
