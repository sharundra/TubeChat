import os
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

class RAGChatbot:
    def __init__(self):
        self.vector_store = None
        self.retriever = None
        self.chain = None
        self.current_video_id = None

    def process_video(self, video_id):
        """Ingests video, creates chunks, and builds index."""
        print(f"Processing video ID: {video_id}")
        
        # Avoid reprocessing if it's the same video and chain is built
        if self.current_video_id == video_id and self.chain:
            return "Video already loaded."
        
        self.current_video_id = video_id
        
        # 1. Fetch Transcript (Updated for v1.2.3 API)
        try:
            # Instantiate the API object (New v1.2.3 way)
            yt_api = YouTubeTranscriptApi()
            
            # Use the instance method .fetch()
            transcript_list = yt_api.fetch(video_id)
            
            full_text = ""
            # Iterate over the FetchedTranscript object
            for chunk in transcript_list:
                # Access attributes via dot notation (.start, .text)
                start_time = int(chunk.start)
                text = chunk.text
                full_text += f"[Start: {start_time}s] {text}\n"

        except Exception as e:
            print(f"Error fetching transcript: {e}")
            # If direct fetch fails, try listing (also updated for v1.2.3)
            try:
                # In v1.2.3, .list() is likely the instance method replacement for list_transcripts
                transcript_list_obj = yt_api.list(video_id)
                # Find english or first available
                transcript = transcript_list_obj.find_transcript(['en', 'en-US'])
                fetched_transcript = transcript.fetch()
                
                full_text = ""
                for chunk in fetched_transcript:
                    start_time = int(chunk.start)
                    text = chunk.text
                    full_text += f"[Start: {start_time}s] {text}\n"
            except Exception as e2:
                raise Exception(f"Could not fetch transcript: {str(e)} | Fallback error: {str(e2)}")

        # 2. Split Text
        print("Splitting text...")
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.create_documents([full_text])

        # 3. Embed & Store
        print("Embedding and creating Vector Store...")
        embeddings = OpenAIEmbeddings()
        self.vector_store = FAISS.from_documents(chunks, embeddings)
        self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 4})
        
        # 4. Build Chain
        print("Building Chain...")
        self._build_chain()
        return "Index built successfully."

    def _build_chain(self):
        llm = ChatOpenAI(model="gpt-3.5-turbo")
        
        template = """
        You are a YouTube Assistant. Answer the question based ONLY on the context provided.
        The context includes timestamps like [Start: 120s]. 
        When answering, try to mention the timestamp if relevant (e.g., "At 2 minutes...").
        If the context is insufficient, just say you don't know.
        
        Context: {context}
        
        Question: {question}
        """
        
        prompt = PromptTemplate.from_template(template)
        
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        self.chain = (
            {"context": self.retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

    def answer_question(self, question):
        if not self.chain:
            return "Please process a video first."
        return self.chain.invoke(question)

# Create a singleton instance
chatbot = RAGChatbot()