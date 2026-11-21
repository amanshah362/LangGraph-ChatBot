# 🤖 Multi-Threaded AI Chatbot

A modern, production-ready full-stack AI chatbot built using **LangGraph**, **Google Gemini**, **SQLite**, and **Streamlit**. It features persistent multi-session chat history, real-time response streaming, and a clean UI inspired by ChatGPT.

---

## ✨ Features

- **🧠 State Orchestration:** Powered by `LangGraph` for robust graph-based state management.
- **⚡ Real-Time Streaming:** Uses LangChain's message chunk streaming (`st.write_stream`) for a fast, typewriter-like AI response experience.
- **💾 Persistent Storage:** Utilizes `SqliteSaver` and SQLite database to save all conversation checkpoints and threads permanently.
- **🗂️ Multi-Threaded Chat History:** 
  - Automatically generates unique thread IDs.
  - Dynamically extracts chat titles from the user's first prompt.
  - Sidebar support to switch, load, and delete past conversations effortlessly.
- **🎨 Modern UI:** Built entirely with `Streamlit` for a responsive and user-friendly interface.

---

## 🛠️ Tech Stack

- **Frontend & UI:** [Streamlit](https://streamlit.io/)
- **Orchestration:** [LangGraph](https://langchain-ai.github.io/langgraph/) / LangChain
- **LLM:** Google Gemini (`gemini-2.5-flash-lite` via `langchain-google-genai`)
- **Database / Checkpointer:** SQLite (`langgraph-checkpoint-sqlite`)
- **Environment Management:** Python-Dotenv

---

## 📂 Project Structure

```text
├── chatbot.db           # SQLite database for storing thread checkpoints (Auto-generated)
├── langgraph_backend.py # LangGraph graph setup, chat node, and SQLite checkpointer
├── frontend.py          # Streamlit UI, session state, and chat layout
├── requirements.txt     # Python dependencies
└── .env                 # Environment variables (API Keys)
