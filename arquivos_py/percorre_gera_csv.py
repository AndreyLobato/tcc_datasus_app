from ftplib import FTP, error_perm
import csv
import os
import pandas as pd

# Configurações do FTP
FTP_HOST = "ftp.datasus.gov.br"
FTP_USER = ""
FTP_PASS = ""
REMOTE_DIR = "/dissemin/publicos/"
#LOCAL_DIR = "/home/andrey/Projetos/TCC/arquivos_py"

def listar_ftp_recursivo(ftp, path='/', resultado=None):
    if resultado is None:
        resultado = []

    try:
        ftp.cwd(path)
    except error_perm:
        return resultado

    linhas = []
    ftp.retrlines('LIST', linhas.append)
    #print("linhas: " , linhas)

    for linha in linhas:
        #print("\nlinha", linha)
        partes = linha.split()
        if len(partes) < 4:
            continue

        # Nome do item é tudo a partir da 4ª posição em diante
        nome = ' '.join(partes[3:])
        caminho_completo = path.rstrip('/') + '/' + nome

        #print('\nnome:', nome, "caminho:", caminho_completo)

        if '<DIR>' in linha:
            print(linha)
            # É um diretório → chama recursivamente
            listar_ftp_recursivo(ftp, caminho_completo, resultado)
        else:
            # É um arquivo → tenta pegar o tamanho
            try:
                tamanho = ftp.size(caminho_completo)
            except:
                tamanho = 0  # Pode falhar por permissão

            resultado.append({
                'nome': nome,
                'tamanho': tamanho,
                'path': caminho_completo
            })           
            df = pd.DataFrame(resultado)
            df.to_csv('df_arquivos_sus.csv')

    return resultado

def gerar_csv(ftp, caminho_raiz='/', nome_arquivo_csv='arquivos_ftp.csv'):
    dados = listar_ftp_recursivo(ftp, caminho_raiz)

# Caminho para o diretório do script
    diretorio_script = os.path.dirname(os.path.abspath(__file__))
    caminho_csv = os.path.join(diretorio_script, nome_arquivo_csv)

    with open(caminho_csv, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['nome', 'tamanho', 'path'])
        writer.writeheader()
        for linha in dados:
            writer.writerow(linha)

    print(f"CSV gerado com sucesso: {nome_arquivo_csv}")


ftp = FTP(FTP_HOST)
ftp.login(FTP_USER, FTP_PASS)
ftp.encoding = 'latin-1'

gerar_csv(ftp, caminho_raiz=REMOTE_DIR,nome_arquivo_csv="df_arquivos_sus.csv")  # Gera o arquivo "arquivos_ftp.csv" no seu diretório local
