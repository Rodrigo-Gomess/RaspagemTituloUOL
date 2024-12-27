import requests
from bs4 import BeautifulSoup
from datetime import datetime
import boto3
import csv
import io

# Inicializando o Cliente s3
s3 = boto3.client('s3')
bucket_name = 'webscrappinuol'


# Cria ou atualiza um arquivo CSV no S3
def cria_arquivo(titulo_texto, data_coleta):
    file_key = 'titulos.csv'

    try:
        # Tenta buscar o arquivo CSV existente no S3
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        file_content = response['Body'].read().decode('utf-8')
        csv_reader = csv.reader(io.StringIO(file_content))
        rows = list(csv_reader)
    except s3.exceptions.NoSuchKey:
        # Caso o arquivo não exista, cria uma nova estrutura
        rows = [["titulo", "data_coleta"]]  # Cabeçalho do CSV

    # Adiciona a nova linha com os dados coletados
    rows.append([titulo_texto, data_coleta])

    # Salva o novo conteúdo em um arquivo CSV na memória
    csv_buffer = io.StringIO()
    csv_writer = csv.writer(csv_buffer)
    csv_writer.writerows(rows)

    # Faz upload do arquivo atualizado para o S3
    s3.put_object(Bucket=bucket_name, Key=file_key, Body=csv_buffer.getvalue())
    print("Arquivo CSV atualizado com sucesso no S3!")


def coleta_titulo():
    url = 'https://uol.com.br'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Armazena o primeiro título na variável título
    titulo = soup.find('h3', 'headlineMain__title')

    # Verifica se encontrou o título desejado
    if titulo:
        titulo_texto = titulo.get_text().strip()
        print(titulo_texto)

        # Data da coleta
        data_coleta = datetime.now().strftime('%Y-%m-%d %H:%M')  # Formato ano-mes-dia hora-minuto

        # Insere os dados no arquivo CSV no S3
        cria_arquivo(titulo_texto, data_coleta)


def lambda_handler(event, context):
    coleta_titulo()
