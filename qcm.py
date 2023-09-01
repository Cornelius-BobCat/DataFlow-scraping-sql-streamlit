# importation des bibliotheque
import streamlit as st
import sqlite3
import pandas as pd
import random
import time

# fonction de mise en cache des données
@st.cache_data
def get_data():
    # connexion a la bdd
    conn = sqlite3.connect('bdd.db')
    cursor = conn.cursor()
    # recupération des données
    cursor.execute('SELECT * FROM informations')
    donnees = cursor.fetchall()

    conn.close()
    # création du df pour le time up
    columns = ['id', 'url_img', 'nom', 'url_wiki']
    return pd.DataFrame(donnees, columns=columns)

# fonction pour relancer app streamlit toutes les 10 secondes
def run_streamlit():
    with st.empty():
        for seconds in range(10):
            st.write(f"⏳ {seconds} seconds")
            time.sleep(1)
        st.write("✔️ Time over!")
        time.sleep(1)
        st.experimental_rerun()

# fonction pour gérer la bonne et la mauvaise réponse
def answer(a,b):
    if a == b:
        return st.success('VRAI', icon="✅")
    else:
        return st.warning('FAUX', icon="⚠️")
    
# titre de l'app
st.title('Time Up Flag')

# recupération des données
df = get_data()

# selection d'une ligne aléatoire
random_row = df.sample()

# recupération du bon pays pour le drapeau
good = str(random_row['nom'].values[0])
# creation d'une liste vide de choix possible
list_choix = []
# ajout de a bonne réponse
list_choix.append(good)

# génération de 1 choix supplémentaire
for i in range(1):
    x = df.sample()
    not_good = str(x['nom'].values[0])
    list_choix.append(not_good)

# brassage de la liste pour qu'elle devienne aléatoire
random.shuffle(list_choix)

# création de 3 colonnes dans le layout de streamlit
col1,col2,col3 = st.columns(3)

with col1:
    # choix option 1
    with st.expander(list_choix[0]):
        answer(list_choix[0],good)
with col2:
    # Drapeaux avec contour noir / option css
    style = "border: 1px solid black;"
    st.markdown(
        f'<img src="{random_row["url_img"].values[0]}" alt="Image" style="{style}" width="200">',
        unsafe_allow_html=True
    )
with col3:
    # choix option 2 
    with st.expander(list_choix[1]):
        answer(list_choix[1],good)

# Appel de la fonction pour le time out et le re run
run_streamlit()

