
code
Markdown
download
content_copy
expand_less
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
⚙️ Installation & Setup
1. Backend Setup

The backend handles the heavy lifting: fetching transcripts and running the LLM chain.

Clone the repository:

code
Bash
download
content_copy
expand_less
git clone https://github.com/yourusername/TubeChat.git
cd TubeChat/backend

Create a virtual environment:

code
Bash
download
content_copy
expand_less
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies:

code
Bash
download
content_copy
expand_less
pip install -r requirements.txt

Set up Environment Variables:
Create a .env file in the backend/ folder and add your OpenAI API key:

code
Text
download
content_copy
expand_less
OPENAI_API_KEY=sk-your-api-key-here

Run the Server:

code
Bash
download
content_copy
expand_less
python main.py

The server will start at http://0.0.0.0:8000.

2. Frontend Setup (Chrome Extension)

Open Google Chrome and navigate to chrome://extensions/.

Toggle Developer mode in the top right corner.

Click Load unpacked.

Select the extension folder inside the TubeChat directory (do not select the root folder).

The extension is now installed!

📖 Usage Guide

Ensure the backend server is running (python main.py).

Open any YouTube video (e.g., a podcast or tutorial).

A dark sidebar will appear on the right side of the screen.

The bot will automatically initialize:

Status: "Processing transcript..."

Status: "Ready! Ask me anything."

Type a question (e.g., "What is the main conclusion?") and hit Enter.

🧠 Architecture Flow

Trigger: content.js detects a YouTube URL and extracts the video_id.

Request: The extension sends a POST request to the FastAPI endpoint /process.

Ingestion: rag_engine.py fetches the transcript using YouTubeTranscriptApi.

Indexing: Text is split into chunks and embedded using OpenAIEmbeddings, then stored in a local FAISS index.

Query: When the user asks a question, the system performs a similarity search on the vector store.

Generation: Relevant chunks + the user question are sent to GPT-3.5 via a LangChain pipeline to generate an answer.

🚀 Future Improvements

Chat History: Add memory to the LangChain pipeline for multi-turn conversations.

Timestamp Linking: Make timestamps in the chat clickable to jump the video player to that time.

Cloud Deployment: Dockerize the backend and deploy to Render/AWS.

Model Selection: Allow users to switch between GPT-3.5 and GPT-4.

🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

📄 License

MIT

code
Code
download
content_copy
expand_less