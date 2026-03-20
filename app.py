import streamlit as st
import os
import glob
from openai import OpenAI
import collections
import math
import re

# Configuration
DATA_DIRS = ["scraped_annuaire", "scraped_fusacq", "scraped_fusacq_regions", "scraped_cfnews"]

st.set_page_config(page_title="Hassan Chat - Corporate Finance", page_icon="🦍", layout="centered")

# Custom CSS for WhatsApp-like feel
st.markdown("""
    <style>
    .stChatMessage {
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar - API Settings
st.sidebar.title("⚙️ Configuration")
default_key = st.secrets.get("DEEPSEEK_API_KEY", "")
api_key = st.sidebar.text_input("Clé API DeepSeek :", value=default_key, type="password")
model_name = st.sidebar.selectbox("Modèle :", ["deepseek-chat", "deepseek-coder"])
top_k_chunks = st.sidebar.slider("Précision (nb segments) :", 10, 100, 40)

st.title("🦍 Hassan Chat")
st.caption("Votre expert en Corporate Finance & M&A")

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
                # Split by double newline or single newline if paragraphs are very long
                paragraphs = re.split(r'\n\s*\n', text)
                for p in paragraphs:
                    stripped = p.strip()
                    if len(stripped) > 50:
                        # Limit chunk size to avoid context overflow
                        chunks.append({"source": name, "content": stripped[:2000]})
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
            if word in chunk['content'].lower(): score += 1
            if word in chunk['source'].lower(): score += 2
        if score > 0:
            scored_chunks.append((score, chunk))
    # Filter unique contents to avoid duplicates
    seen = set()
    unique_results = []
    for s, c in sorted(scored_chunks, key=lambda x: x[1], reverse=True):
        if c['content'] not in seen:
            unique_results.append((s, c))
            seen.add(c['content'])
            if len(unique_results) >= k: break
    return unique_results

# Session State for Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🦍" if message["role"] == "assistant" else None):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Comment puis-je vous aider ?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    results = get_best_chunks(prompt, all_chunks, k=top_k_chunks)
    
    with st.chat_message("assistant", avatar="🦍"):
        if results:
            context_parts = []
            sources_used = set()
            for score, chunk in results:
                context_parts.append(f"SOURCE: {chunk['source'].upper()}\n{chunk['content']}")
                sources_used.add(chunk['source'].upper())
            
            context = "\n\n---\n\n".join(context_parts)
            
            if api_key:
                try:
                    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
                    
                    response_placeholder = st.empty()
                    full_response = ""
                    
                    completion = client.chat.completions.create(
                        model=model_name,
                        messages=[
                            {"role": "system", "content": "Tu es Hassan, un gorille assistant expert en Corporate Finance. Réponds de manière exhaustive et professionnelle en utilisant le contexte fourni. Signe toujours avec 🦍."},
                            {"role": "user", "content": f"CONTEXTE:\n{context}\n\nQUESTION: {prompt}"}
                        ],
                        stream=True
                    )
                    
                    for chunk in completion:
                        if len(chunk.choices) > 0 and chunk.choices[0].delta.content:
                            full_response += chunk.choices[0].delta.content
                            response_placeholder.markdown(full_response + "▌")
                    
                    response_placeholder.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                    
                    with st.expander("📚 Sources utilisées"):
                        st.write(", ".join(list(sources_used)))
                except Exception as e:
                    st.error(f"Erreur API : {e}")
            else:
                st.info("💡 Veuillez configurer votre clé API dans la barre latérale pour activer les réponses de Hassan.")
        else:
            st.write("Désolé, je ne trouve pas d'informations sur ce sujet dans ma base de données. 🦍")

# Sidebar stats
st.sidebar.markdown("---")
st.sidebar.info(f"📊 **Index** : {len(all_chunks)} segments")
