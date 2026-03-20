import streamlit as st
import os
import glob
from openai import OpenAI
import collections
import math
import re

# Configuration
DATA_DIRS = ["scraped_annuaire", "scraped_fusacq", "scraped_fusacq_regions", "scraped_cfnews"]

st.set_page_config(page_title="Hassan Corporate RAG", page_icon="🦍", layout="wide")

# Sidebar - API Settings
st.sidebar.title("⚙️ Configuration")
default_key = st.secrets.get("DEEPSEEK_API_KEY", "")
api_key = st.sidebar.text_input("Clé API DeepSeek :", value=default_key, type="password")
model_name = st.sidebar.selectbox("Modèle :", ["deepseek-chat", "deepseek-coder"])
top_k_chunks = st.sidebar.slider("Nombre de segments à analyser :", 10, 100, 40)

st.title("🦍 Hassan Corporate RAG v3")
st.subheader("Intelligence de Marché - Analyse de Précision")

# Load data and chunk it
@st.cache_data
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
                # Split by double newline to get "expert blocks" or paragraphs
                paragraphs = re.split(r'\n\s*\n', text)
                for p in paragraphs:
                    if len(p.strip()) > 50:
                        chunks.append({"source": name, "content": p.strip()})
        except: pass
    return chunks

all_chunks = load_and_chunk_data()

# Improved scoring on chunks
def get_best_chunks(query, chunks, k=40):
    words = [w.lower() for w in query.split() if len(w) > 3]
    scored_chunks = []
    
    for chunk in chunks:
        score = 0
        for word in words:
            if word in chunk['content'].lower():
                score += 1
            # Bonus for source name match
            if word in chunk['source'].lower():
                score += 2
        
        if score > 0:
            scored_chunks.append((score, chunk))
            
    return sorted(scored_chunks, key=lambda x: x[0], reverse=True)[:k]

# Search & Chat
query = st.text_input("Posez votre question (Hassan scannera chaque ligne des 217 sources) :", "")

if query:
    st.write(f"🔍 **Hassan analyse les segments les plus pertinents...**")
    
    # 1. Retrieval of chunks
    results = get_best_chunks(query, all_chunks, k=top_k_chunks)
    
    if results:
        # 2. Context Building
        context_parts = []
        sources_used = set()
        for score, chunk in results:
            context_parts.append(f"SOURCE: {chunk['source'].upper()}\n{chunk['content']}")
            sources_used.add(chunk['source'].upper())
        
        context = "\n\n---\n\n".join(context_parts)
        
        if api_key:
            try:
                client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
                
                with st.spinner(f"🧠 Synthèse Hassan en cours (Basée sur {len(results)} segments)..."):
                    response = client.chat.completions.create(
                        model=model_name,
                        messages=[
                            {"role": "system", "content": "Tu es Hassan, un gorille assistant métaphorique : solide, protecteur, calme et d'une efficacité redoutable. Ton approche est sérieuse et hautement professionnelle. Tu parles peu mais avec précision. Réponds à la question en utilisant le contexte fourni. Signe toujours avec 🦍."},
                            {"role": "user", "content": f"Voici les extraits de ma base de données :\n\n{context}\n\nQUESTION: {query}"}
                        ],
                        stream=False
                    )
                    st.markdown("### 🦍 Réponse de Hassan :")
                    st.write(response.choices[0].message.content)
            except Exception as e:
                st.error(f"Erreur API DeepSeek : {e}")
        
        st.markdown("---")
        st.write(f"📂 **Sources ayant contribué à cette réponse ({len(sources_used)}) :**")
        st.write(", ".join(list(sources_used)))
    else:
        st.warning("Aucun segment de données ne semble correspondre à votre recherche.")

# Sidebar info
st.sidebar.markdown("---")
st.sidebar.info(f"📊 **Statistiques**\n- Segments indexés : {len(all_chunks)}\n- Sources : 4 dossiers")
st.sidebar.write("Hassan v3.0 - Précision Chirurgicale 🦍")
