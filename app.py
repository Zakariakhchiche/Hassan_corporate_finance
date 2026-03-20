import streamlit as st
import os
import glob
from openai import OpenAI
import collections
import math

# Configuration
DATA_DIRS = ["scraped_annuaire", "scraped_fusacq", "scraped_fusacq_regions"]

st.set_page_config(page_title="Hassan Corporate RAG", page_icon="🦍", layout="wide")

# Sidebar - API Settings
st.sidebar.title("⚙️ Configuration")
default_key = st.secrets.get("DEEPSEEK_API_KEY", "")
api_key = st.sidebar.text_input("Clé API DeepSeek :", value=default_key, type="password")
model_name = st.sidebar.selectbox("Modèle :", ["deepseek-chat", "deepseek-coder"])
top_k = st.sidebar.slider("Nombre de sources à analyser :", 5, 30, 15)

st.title("🦍 Hassan Corporate RAG v2")
st.subheader("Intelligence de Marché - Analyse de 217 sources")

# Load data
@st.cache_data
def load_data():
    files = []
    for d in DATA_DIRS:
        if os.path.exists(d):
            files.extend(glob.glob(os.path.join(d, "*.md")))
    
    content = {}
    for f in files:
        try:
            with open(f, "r", encoding="utf-8") as file:
                name = os.path.basename(f).replace(".md", "")
                content[name] = file.read()
        except: pass
    return content

data = load_data()

# Simple TF-IDF like scoring
def get_scores(query, data):
    words = query.lower().split()
    scores = collections.defaultdict(float)
    
    # Calculate global word frequency to identify "rare" words (more important)
    all_text = " ".join(data.values()).lower()
    total_words = len(all_text.split())
    
    for word in words:
        if len(word) < 3: continue
        word_count = all_text.count(word)
        # Weight = log(Total / (1 + Count))
        weight = math.log(total_words / (1 + word_count))
        
        for name, text in data.items():
            if word in text.lower():
                # Count occurrences in this document
                occ = text.lower().count(word)
                scores[name] += occ * weight
                
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)

# Search & Chat
query = st.text_input("Posez votre question (Hassan analysera les meilleures sources correspondantes) :", "")

if query:
    st.write(f"🔍 **Hassan scanne la base de données...**")
    
    # 1. Retrieval
    results = get_scores(query, data)[:top_k]
    
    if results:
        # 2. Context Building (Increased to 3000 chars per source)
        context_parts = []
        for name, score in results:
            context_parts.append(f"SOURCE: {name.upper()}\nCONTENT: {data[name][:3000]}")
        
        context = "\n\n---\n\n".join(context_parts)
        
        if api_key:
            try:
                client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
                
                with st.spinner(f"🧠 Analyse de {len(results)} sources par DeepSeek..."):
                    response = client.chat.completions.create(
                        model=model_name,
                        messages=[
                            {"role": "system", "content": "Tu es Hassan, un assistant expert en Corporate Finance. Réponds de manière exhaustive en utilisant le contexte fourni. Si une information n'est pas dans le contexte, dis-le. Structure ta réponse avec des puces."},
                            {"role": "user", "content": f"Voici les fiches extraites pour répondre à la question.\n\n{context}\n\nQUESTION: {query}"}
                        ],
                        stream=False
                    )
                    st.markdown("### 🦍 Réponse de Hassan :")
                    st.write(response.choices[0].message.content)
            except Exception as e:
                st.error(f"Erreur API DeepSeek : {e}")
        
        st.markdown("---")
        st.write("📂 **Sources analysées pour cette réponse :**")
        cols = st.columns(3)
        for idx, (name, score) in enumerate(results):
            with cols[idx % 3]:
                with st.expander(f"📄 {name.upper()}"):
                    st.markdown(data[name])
    else:
        st.warning("Aucun résultat pertinent trouvé.")

# Sidebar info
st.sidebar.markdown("---")
st.sidebar.info(f"📊 **Statistiques**\n- Fiches indexées : {len(data)}")
st.sidebar.write("Hassan v2.0 🦍")
