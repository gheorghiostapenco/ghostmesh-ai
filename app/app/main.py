from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import chromadb
import uuid

app = FastAPI()

# --- CONFIGURATION ---
OLLAMA_URL = "http://ollama:11434/api/generate"
# Connect to the ChromaDB container defined in docker-compose
chroma_client = chromadb.HttpClient(host='chromadb', port=8000)
# Create/Get a collection to store our knowledge
collection = chroma_client.get_or_create_collection(name="my_knowledge")

class PromptRequest(BaseModel):
    prompt: str
    model: str = "llama3.1"

class LearnRequest(BaseModel):
    text: str
    source: str = "unknown"

@app.get("/")
def read_root():
    return {"status": "GhostMesh AI (RAG Enabled) is Online"}

@app.post("/learn")
def learn_text(request: LearnRequest):
    """
    Teaches the AI new information by storing it in the Vector DB.
    """
    try:
        # ChromaDB automatically handles Embedding (converting text to numbers)
        # utilizing the default 'all-MiniLM-L6-v2' model.
        collection.add(
            documents=[request.text],
            metadatas=[{"source": request.source}],
            ids=[str(uuid.uuid4())]
        )
        return {"status": "success", "message": "I have learned this information."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask")
def ask_ai(request: PromptRequest):
    """
    Retrieves relevant context from memory before answering.
    """
    try:
        # 1. SEARCH MEMORY (RAG)
        # Query the database for the 2 most relevant chunks of text
        results = collection.query(
            query_texts=[request.prompt],
            n_results=2
        )
        
        # Extract the found text
        context = ""
        if results['documents']:
            context = "\n".join(results['documents'][0])
            
        # 2. CONSTRUCT THE PROMPT
        # We tell the AI: "Use this context to answer the user."
        final_prompt = f"""
        You are an intelligent assistant. Use the following context to answer the question.
        If the answer is not in the context, say "I don't know based on my memory."
        
        CONTEXT:
        {context}
        
        QUESTION:
        {request.prompt}
        """
        
        # 3. CALL OLLAMA
        payload = {
            "model": request.model,
            "prompt": final_prompt,
            "stream": False
        }
        
        response = requests.post(OLLAMA_URL, json=payload)
        return {
            "answer": response.json().get("response"),
            "context_used": context  # Returning this helps debugging!
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
