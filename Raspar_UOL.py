import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import boto3
import os

# Inicializando o Cliente s3
s3 = boto3.client('s3')
bucket_name = 'FALTA CRIAR BUCKET'

# Cria ou atualiza um arquivo CSV no S3
def cria_arquivo(titulo_texto, data_coleta):
    # Verifica se o arquivo já existe
    try:
       # Busca o arquivo para inserir novos dados
        response = s3.get_object(Bucket = bucket_name, key ='titulos.csv')
        df = pd.read_csv(response['body'])
    except s3.exceptions.NoSuchKey:
        #Caso não exista o arquivo, cria.
        df = pd.DataFrame(columns=['titulo', 'data_coleta'])

    # Adiciona uma nova linha com os dados coletados
    nova_linha = pd.DataFrame([[titulo_texto, data_coleta]], columns=['titulo', 'data_coleta'])
    df = pd.concat([df, nova_linha], ignore_index=True)

    # Salva o DataFrame como um arquivo CSV localmente
    df.to_csv('/tmp/titulos.csv', index=False)

    # Faz upload do arquivo CSV para o S3
    s3.upload_file('/tmp/titulos.csv', bucket_name, 'titulos.csv')



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

        # insere os dados no arquivo CSV no S3
        cria_arquivo(titulo_texto, data_coleta)


def lambda_handler(event, context):
    coleta_titulo()