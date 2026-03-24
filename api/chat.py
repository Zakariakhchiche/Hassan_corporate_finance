from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os
import glob
import re

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIRS = ["scraped_annuaire", "scraped_fusacq", "scraped_fusacq_regions", "scraped_cfnews", "scraped_rag_pdfs"]

class ChatRequest(BaseModel):
    message: str

def load_and_chunk_data():
    files = []
    for d in DATA_DIRS:
        if os.path.exists(d):
            files.extend(glob.glob(os.path.join(d, "*.md")))
    
    chunks = []
    for f in files:
        try:
            with open(f, "r", encoding="utf-8") as file:
                name = os.path.basename(f).replace(".md", "")
                text = file.read()
                paragraphs = re.split(r'\n\s*\n', text)
                for p in paragraphs:
                    stripped = p.strip()
                    if len(stripped) > 50:
                        chunks.append({"source": name, "content": stripped[:2000]})
        except: pass
    return chunks

def get_best_chunks(query, chunks, k=40):
    words = [w.lower() for w in query.split() if len(w) > 3]
    scored_chunks = []
    for chunk in chunks:
        score = 0
        for word in words:
            if word in chunk['content'].lower(): score += 1
            if word in chunk['source'].lower(): score += 2
        if score > 0:
            scored_chunks.append((score, chunk))
    
    seen = set()
    unique_results = []
    for s, c in sorted(scored_chunks, key=lambda x: x[0], reverse=True):
        if c['content'] not in seen:
            unique_results.append((s, c))
            seen.add(c['content'])
            if len(unique_results) >= k: break
    return unique_results

@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        chunks = load_and_chunk_data()
        results = get_best_chunks(request.message, chunks, k=40)
        
        if not results:
            return {"response": "Désolé, je ne trouve pas d'informations pertinentes dans ma base de données. 🦍", "sources": []}
        
        context_parts = []
        sources_used = set()
        for score, chunk in results:
            context_parts.append(f"SOURCE: {chunk['source'].upper()}\n{chunk['content']}")
            sources_used.add(chunk['source'].upper())
        
        context = "\n\n---\n\n".join(context_parts)
        
        api_key = os.environ.get("DEEPSEEK_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="DEEPSEEK_API_KEY not set")
        
        client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        
        completion = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "Tu es Hassan, un gorille assistant expert en Corporate Finance. Réponds de manière exhaustive et professionnelle en utilisant le contexte fourni. Signe toujours avec 🦍."},
                {"role": "user", "content": f"CONTEXTE:\n{context}\n\nQUESTION: {request.message}"}
            ]
        )
        
        response = completion.choices[0].message.content
        
        return {"response": response, "sources": list(sources_used)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Hassan Corporate RAG API"}
