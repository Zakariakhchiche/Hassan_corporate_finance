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

# Search
query = st.text_input("Rechercher une entreprise, un expert ou un secteur :", "")

if query:
    st.write(f"Résultats pour : **{query}**")
    matches = []
    for name, text in data.items():
        if query.lower() in text.lower():
            matches.append(name)
    
    if matches:
        for m in matches:
            with st.expander(f"📄 {m.upper()}"):
                st.markdown(data[m])
    else:
        st.warning("Aucun résultat trouvé.")

# Sidebar info
st.sidebar.info(f"📊 **Statistiques du RAG**\n- Entreprises indexées : {len(data)}\n- Sources : CFNEWS, Fusacq, Annuaire CF")
st.sidebar.markdown("---")
st.sidebar.write("Développé par Hassan 🦍")

if st.sidebar.button("Actualiser les données"):
    st.cache_data.clear()
    st.rerun()
