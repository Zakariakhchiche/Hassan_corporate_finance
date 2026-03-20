import streamlit as st
import os
import glob
from openai import OpenAI

# Configuration
DATA_DIRS = ["scraped_annuaire", "scraped_fusacq", "scraped_fusacq_regions"]

st.set_page_config(page_title="Hassan Corporate RAG", page_icon="🦍")

# Sidebar - API Settings
st.sidebar.title("⚙️ Configuration")
api_key = st.sidebar.text_input("Clé API DeepSeek :", type="password")
model_name = st.sidebar.selectbox("Modèle :", ["deepseek-chat", "deepseek-coder"])

st.title("🦍 Hassan Corporate RAG")
st.subheader("Base de données Intelligence Corporate & M&A")

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

# Search & Chat
query = st.text_input("Posez votre question en langage naturel (RAG) :", "")

if query:
    st.write(f"### Analyse pour : *{query}*")
    
    # 1. Retrieval (Simple Keyword Scoring)
    results = []
    for name, text in data.items():
        score = sum(1 for word in query.lower().split() if word in text.lower())
        if score > 0:
            results.append((score, name))
    
    results = sorted(results, key=lambda x: x[0], reverse=True)[:5] # Top 5
    
    if results:
        context = "\n\n".join([f"--- {name} ---\n{data[name][:2000]}" for score, name in results])
        
        if api_key:
            try:
                client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
                
                with st.spinner("🧠 DeepSeek est en train de rédiger la synthèse..."):
                    response = client.chat.completions.create(
                        model=model_name,
                        messages=[
                            {"role": "system", "content": "Tu es Hassan, un assistant expert en Corporate Finance. Réponds à la question en utilisant uniquement le contexte fourni. Sois précis et professionnel."},
                            {"role": "user", "content": f"CONTEXTE:\n{context}\n\nQUESTION: {query}"}
                        ],
                        stream=False
                    )
                    st.markdown("#### 🤖 Réponse de Hassan :")
                    st.write(response.choices[0].message.content)
            except Exception as e:
                st.error(f"Erreur API DeepSeek : {e}")
        else:
            st.info("💡 Clé API manquante dans la barre latérale. Voici les sources pertinentes trouvées :")
        
        for score, m in results:
            with st.expander(f"📍 Source : {m.upper()}"):
                st.markdown(data[m])
    else:
        st.warning("Aucun résultat pertinent trouvé dans la base de données.")

# Sidebar info
st.sidebar.markdown("---")
st.sidebar.info(f"📊 **Statistiques**\n- Fiches indexées : {len(data)}")
st.sidebar.write("Développé par Hassan 🦍")
