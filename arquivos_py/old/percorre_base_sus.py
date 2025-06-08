import ftplib
import pandas as pd
import pyarrow.parquet as pq
import os
from dbfread import DBF

# Configurações do FTP
FTP_HOST = "ftp.datasus.gov.br"
FTP_USER = ""
FTP_PASS = ""
REMOTE_DIR = "/dissemin/publicos/SIASUS/200801_/Dados/ "
LOCAL_DIR = "/home/andrey/Projetos/TCC/arquivos_py"


def listar_arquivos_ftp():
    """Conecta ao FTP e retorna a lista de arquivos no diretório remoto."""
    with ftplib.FTP(FTP_HOST) as ftp:
        ftp.login(FTP_USER, FTP_PASS)
        ftp.cwd(REMOTE_DIR)  # Muda para o diretório correto
        arquivos = ftp.nlst()  # Lista os arquivos disponíveis
    return arquivos

def obter_tamanho_arquivo(filename):
    """Obtém o tamanho do arquivo no FTP em GB."""
    with ftplib.FTP(FTP_HOST) as ftp:
        ftp.login(FTP_USER, FTP_PASS)
        ftp.cwd(REMOTE_DIR)
        tamanho_bytes = ftp.size(filename)  # Obtém o tamanho em bytes
        tamanho_gb = tamanho_bytes / (1024 ** 3)  # Converte para GB
    return tamanho_gb


def listar_arquivos_e_tamanhos():
    """Retorna duas listas: uma com os nomes dos arquivos e outra com seus tamanhos em GB."""
    nomes_arquivos = []
    tamanhos_arquivos = []
    
    with ftplib.FTP(FTP_HOST) as ftp:
        ftp.login(FTP_USER, FTP_PASS)
        ftp.cwd(REMOTE_DIR)  # Muda para o diretório correto
        arquivos = ftp.nlst()  # Lista os arquivos disponíveis

        for arquivo in arquivos:
            try:
                tamanho_bytes = ftp.size(arquivo)  # Obtém o tamanho em bytes
                #tamanho_gb = tamanho_bytes / (1024 ** 3)  # Converte para GB
                nomes_arquivos.append(arquivo)
                tamanhos_arquivos.append(tamanho_bytes)
            except Exception as e:
                print(f"Erro ao obter tamanho de {arquivo}: {e}")

    return nomes_arquivos, tamanhos_arquivos

#dbc_file = baixar_arquivo_ftp("ABDF1112.dbc")
#arquivos_disponiveis = listar_arquivos_ftp()

# Obtém os nomes e tamanhos dos arquivos
nomes, tamanhos = listar_arquivos_e_tamanhos()

print(len(nomes))
print(sum(tamanhos))

def converter_dbc_para_parquet(dbc_path):
    #Converte um arquivo DBC para Parquet comprimido.
    tabela = DBF(dbc_path, encoding="latin1")  # Converter DBC em DataFrame
    df = pd.DataFrame(iter(tabela))
    parquet_path = dbc_path.replace(".dbc", ".parquet")

    # Salvar em Parquet com compressão máxima
    df.to_parquet(parquet_path, compression="gzip", index=False)
    os.remove(dbc_path)  # Apagar o arquivo DBC para economizar espaço
    return parquet_path

def inserir_no_banco(parquet_path):
    #Exemplo de como inserir os dados no banco de dados PostgreSQL.
    from sqlalchemy import create_engine

    engine = create_engine("postgresql://usuario:senha@host:porta/banco")
    df = pd.read_parquet(parquet_path)
    
    # Inserir em lotes para melhor performance
    df.to_sql("tabela_destino", engine, if_exists="append", index=False, chunksize=10000)

    os.remove(parquet_path)  # Apagar o arquivo Parquet após inserção

    # Fluxo de trabalho
arquivos_ftp = ["arquivo1.dbc", "arquivo2.dbc"]  # Isso pode ser listado dinamicamente
for arquivo in arquivos_ftp:
    dbc_file = baixar_arquivo_ftp(arquivo)
    parquet_file = converter_dbc_para_parquet(dbc_file)
    inserir_no_banco(parquet_file)

