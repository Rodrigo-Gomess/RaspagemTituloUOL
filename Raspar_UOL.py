import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import sqlite3



def cria_tabela():
    # Conectar ao banco de dados (ou criar se não existir)
    conn = sqlite3.connect('titulos_uol.db')
    cursor = conn.cursor()

    # Criar tabela se não existir
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS titulos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        data_coleta TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()


def insere_titulo(titulo_texto, data_coleta):
    # Conectar ao banco de dados
    conn = sqlite3.connect('titulos_uol.db')
    cursor = conn.cursor()

    # Inserir o título e a data de coleta na tabela
    cursor.execute('''
    INSERT INTO titulos (titulo, data_coleta) VALUES (?, ?)
    ''', (titulo_texto, data_coleta))

    conn.commit()
    conn.close()


def coleta_titulo():
    url = 'https://uol.com.br'

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Armazena o primeiro título na variável titulos
    titulo = soup.find('h3', 'headlineMain__title')

    # Verifica se encontrou o título desejado
    if titulo:
        titulo_texto = titulo.get_text().strip()
        print(titulo_texto)

        #Data da coleta
        data_coleta = datetime.now().strftime('%Y-%m-%d %H:%M')  # Formato ano-mes-dia hora-minuto

        # insere os dados na tabela SQLite
        insere_titulo(titulo_texto, data_coleta)


cria_tabela()
coleta_titulo()