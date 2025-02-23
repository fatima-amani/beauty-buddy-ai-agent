# AI Chatbot

## 📌 Overview

This project is an AI-powered chatbot built using **FastAPI** as the backend and **Streamlit** for the frontend. It leverages **LangChain**, **TogetherAPI**, **LLM**, **RAG** and **Web scraping** to provide responses and beauty product recommendations.

## 🚀 Features

- **FastAPI Backend**: Handles user queries via a `/query` endpoint
- **Streamlit Frontend**: Provides a chat-based UI for interaction
- **AI Agent with LangChain**: Uses an intelligent agent to classify queries
- **Knowledge Base Retrieval**: Retrieves relevant beauty-related information
- **Web Scraping**: Suggests beauty products based on user preferences

## 🏗️ Project Structure

```
📂 AI Chatbot
│── agent.py        # AI agent using LangChain
│── app.py         # FastAPI backend for chatbot
│── chatbot_ui.py  # Streamlit frontend for user interaction
│── injest.py   # FAISS-based PDF text embedding and indexing
│── llm.py         # LLM model (on local machine) integration
│── llm2.py         # LLM model (via together API) integration
│── retriever.py   # FAISS-based document retrieval using embeddings
│── scraper.py     # Scrapes beauty products and links
│── .gitignore     # Git ignore file
│── README.md      # Project documentation
```

## 🛠️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/fatima-amani/AI-Major-Assignment
cd AI-Major-Assignment
```

### 2️⃣ Create a Virtual Environment & Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
pip install -r requirements.txt
```

### 3️⃣ Set Up Environment Variables

Create a `.env` file and add your API keys:

```ini
TOGETHER_ACCESS_TOKEN=your_api_key
```

### 4️⃣ Run FastAPI Backend

```bash
python app.py
```

### 5️⃣ Run Streamlit Frontend

```bash
streamlit run chatbot_ui.py
```

## 🖥️ Usage

1. Open the Streamlit UI in your browser
2. Type a question related to beauty, skincare, or makeup
3. The chatbot will provide answers or product recommendations

## 💡 Author

Developed by Fatima Amani
