# TubeChat 🤖: RAG-Powered YouTube Assistant

**TubeChat** is a full-stack Generative AI application that transforms how users interact with video content. It integrates a **Chrome Extension** frontend with a **Python/LangChain** backend to provide real-time, context-aware Q&A for any YouTube video.

---

## 🚀 Project Overview

This project bridges the gap between static video content and interactive AI. Instead of manually copying transcripts into an LLM, TubeChat automatically injects a sidebar into the YouTube interface, ingests the video transcript, generates vector embeddings, and allows the user to chat with the video content using **Retrieval Augmented Generation (RAG)**.

### Key Features
- **⚡ Automatic Injection:** Detects YouTube video URLs and injects a chat interface directly into the DOM.
- **🧠 RAG Engine:** Uses LangChain and FAISS to create a searchable vector index of the video transcript.
- **🕰️ Temporal Context:** Preserves timestamp metadata, allowing the AI to cite specific moments in the video (e.g., *"At 120s, the speaker mentions..."*).
- **🔌 Microservices Architecture:** Decoupled Client-Server architecture using FastAPI and Vanilla JavaScript.

---

## 🛠️ Tech Stack

### Backend (AI Logic)
- **Framework:** FastAPI (Async Python Server)
- **Orchestration:** LangChain (LCEL)
- **Vector Store:** FAISS (Facebook AI Similarity Search)
- **LLM:** OpenAI GPT-3.5 Turbo
- **Data Ingestion:** `youtube-transcript-api`

### Frontend (User Interface)
- **Platform:** Chrome Extension Manifest V3
- **Logic:** Vanilla JavaScript (DOM Manipulation, Fetch API)
- **Styling:** CSS3 (Dark Mode optimized)

---

## 📂 Project Structure

```text
TubeChat/
├── backend/
│   ├── main.py            # FastAPI entry point & CORS configuration
│   ├── rag_engine.py      # Core RAG logic (Ingestion, Splitting, Embedding, Retrieval)
│   ├── requirements.txt   # Python dependencies
│   └── .env               # Environment variables (OpenAI Key)
└── extension/
    ├── manifest.json      # Chrome Extension configuration
    ├── content.js         # Content script for DOM injection & API communication
    └── styles.css         # Sidebar UI styling
---

## ⚙️ Installation & Setup

### 1. Backend Setup
The backend handles the heavy lifting: fetching transcripts and running the LLM chain.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/TubeChat.git
    cd TubeChat/backend
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up Environment Variables:**
    Create a `.env` file in the `backend/` folder and add your OpenAI API key:
    ```text
    OPENAI_API_KEY=sk-your-api-key-here
    ```

5.  **Run the Server:**
    ```bash
    python main.py
    ```
    *The server will start at `http://0.0.0.0:8000`.*

### 2. Frontend Setup (Chrome Extension)
1.  Open Google Chrome and navigate to `chrome://extensions/`.
2.  Toggle **Developer mode** in the top right corner.
3.  Click **Load unpacked**.
4.  Select the **`extension`** folder inside the `TubeChat` directory (do not select the root folder).
5.  The extension is now installed!

---

## 📖 Usage Guide

1.  Ensure the backend server is running (`python main.py`).
2.  Open any YouTube video (e.g., a podcast or tutorial).
3.  A dark sidebar will appear on the right side of the screen.
4.  The bot will automatically initialize:
    *   *Status: "Processing transcript..."*
    *   *Status: "Ready! Ask me anything."*
5.  Type a question (e.g., *"What is the main conclusion?"*) and hit Enter.

---

## 🧠 Architecture Flow

1.  **Trigger:** `content.js` detects a YouTube URL and extracts the `video_id`.
2.  **Request:** The extension sends a POST request to the FastAPI endpoint `/process`.
3.  **Ingestion:** `rag_engine.py` fetches the transcript using `YouTubeTranscriptApi`.
4.  **Indexing:** Text is split into chunks and embedded using `OpenAIEmbeddings`, then stored in a local `FAISS` index.
5.  **Query:** When the user asks a question, the system performs a similarity search on the vector store.
6.  **Generation:** Relevant chunks + the user question are sent to GPT-3.5 via a LangChain pipeline to generate an answer.

---

## 🚀 Future Improvements
- [ ] **Chat History:** Add memory to the LangChain pipeline for multi-turn conversations.
- [ ] **Timestamp Linking:** Make timestamps in the chat clickable to jump the video player to that time.
- [ ] **Cloud Deployment:** Dockerize the backend and deploy to Render/AWS.
- [ ] **Model Selection:** Allow users to switch between GPT-3.5 and GPT-4.

---

## 🤝 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License
[MIT](https://choosealicense.com/licenses/mit/)
```