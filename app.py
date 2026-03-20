import streamlit as st
import os
import glob

# Configuration
DATA_DIRS = ["scraped_annuaire", "scraped_fusacq", "scraped_fusacq_regions"]

st.set_page_config(page_title="Hassan Corporate RAG", page_icon="🦍")

st.title("🦍 Hassan Corporate RAG")
st.subheader("Base de données Intelligence Corporate & M&A")

# Load data
@st.cache_data
def load_data():
    files = []
    for d in DATA_DIRS:
        files.extend(glob.glob(os.path.join(d, "*.md")))
    
    content = {}
    for f in files:
        with open(f, "r", encoding="utf-8") as file:
            name = os.path.basename(f).replace(".md", "")
            content[name] = file.read()
    return content

data = load_data()

# Search & Chat
query = st.text_input("Posez votre question en langage naturel (ex: 'Quels fonds investissent dans le BTP ?') :", "")

if query:
    st.write(f"### Analyse pour : *{query}*")
    
    # 1. Retrieval (Semantic search simulation via keyword scoring)
    results = []
    for name, text in data.items():
        score = sum(1 for word in query.lower().split() if word in text.lower())
        if score > 0:
            results.append((score, name))
    
    results = sorted(results, key=lambda x: x[0], reverse=True)[:5] # Top 5
    
    if results:
        # 2. Context Building
        context = "\n\n".join([f"--- {name} ---\n{data[name][:1000]}" for score, name in results])
        
        # 3. Simple Logic for Answer (Mocking LLM if key is missing)
        st.info("💡 Hassan est en train d'analyser les fiches correspondantes...")
        
        for score, m in results:
            with st.expander(f"📍 Source : {m.upper()}"):
                st.markdown(data[m])
                
        st.success("Analyse terminée. Vous pouvez consulter les fiches détaillées ci-dessus pour obtenir les réponses précises.")
    else:
        st.warning("Désolé, je n'ai pas trouvé d'informations pertinentes pour cette question dans la base actuelle.")

# Sidebar info
st.sidebar.info(f"📊 **Statistiques du RAG**\n- Entreprises indexées : {len(data)}\n- Sources : CFNEWS, Fusacq, Annuaire CF")
st.sidebar.markdown("---")
st.sidebar.write("Développé par Hassan 🦍")

if st.sidebar.button("Actualiser les données"):
    st.cache_data.clear()
    st.rerun()
