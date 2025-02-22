import streamlit as st
import requests

# Set up the Streamlit page
st.set_page_config(page_title="Beauty Chatbot", layout="wide")

st.title("Beauty & Makeup Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input field
user_query = st.chat_input("Ask me anything about beauty & makeup...")

if user_query:
    # Display user query
    st.session_state["messages"].append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    # Send query to backend (agent.py)
    response = requests.post("http://localhost:8000/query", json={"input": user_query})

    if response.status_code == 200:
        bot_reply = response.json().get("output", "Sorry, I didn't understand that.")
    else:
        bot_reply = "Error connecting to the AI model."

    # Display bot response
    with st.chat_message("assistant"):
        st.markdown(bot_reply)

    # Add bot reply to chat history
    st.session_state["messages"].append({"role": "assistant", "content": bot_reply})
