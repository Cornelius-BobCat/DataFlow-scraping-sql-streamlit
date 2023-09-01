import streamlit as st
import sqlite3

conn = sqlite3.connect('bdd.db')
cursor = conn.cursor()

st.title('Application SQLite Flag')

cursor.execute('SELECT * FROM informations')
donnees = cursor.fetchall()

st.write('Liste des informations :')
for id, url_img, nom, url_wiki in donnees:
    st.image(url_img)
    st.write(f'Nom : {nom}')
    st.write(f'URL Wiki : {url_wiki}')
    st.write('----------------------')

conn.close()