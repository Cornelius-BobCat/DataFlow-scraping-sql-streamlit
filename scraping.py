import pandas as pd
import requests
from bs4 import BeautifulSoup
import sqlite3

conn = sqlite3.connect('bdd.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS informations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url_img TEXT,
        nom TEXT,
        url_wiki TEXT
    )
''')

url = "https://fr.wikipedia.org/wiki/Galerie_des_drapeaux_des_pays_du_monde"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    td_elements = soup.select('.toccolours td')

    c=0
    for td in td_elements:
        img_tag = td.find('img') 
        a_tag = td.findAll('a') 

        if img_tag and a_tag:
            img_html = img_tag.prettify() 
            img_src = 'https:'+img_tag['src'] 
            last_a_tag = a_tag[-1]
            last_a_href = 'https://fr.wikipedia.org' + last_a_tag['href']
            last_a_text = last_a_tag.get_text() 

            cursor.execute('INSERT INTO informations (url_img, nom, url_wiki) VALUES (?, ?, ?)', (img_src,last_a_text,last_a_href))
            conn.commit() 

            c+=1
    print(c)
    conn.close() 
else:
    print("La requête a échoué avec le code :", response.status_code)