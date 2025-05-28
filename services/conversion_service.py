import os
import pandas as pd
import pyreaddbc
import dbfread
from ftplib import FTP
import pyarrow as pa
import pyarrow.orc as orc


def converter_para_parquet(caminho_local, nome_arquivo, destino):
    
    extensao = os.path.splitext(nome_arquivo)[1].lower()

    if extensao == ".dbc":
        dbf_path = caminho_local.replace(".dbc", ".dbf")
        pyreaddbc.dbc2dbf(caminho_local, dbf_path)
        caminho_para_ler = dbf_path
    elif extensao == ".dbf":
        caminho_para_ler = caminho_local
    else:
        raise ValueError("Formato não suportado para conversão.")

    # Leitura do arquivo DBF
    df = pd.DataFrame(iter(dbfread.DBF(caminho_para_ler)))
    
    # Salva como parquet
    nome_sem_extensao = os.path.splitext(nome_arquivo)[0]
    parquet_path = os.path.join(destino, f"{nome_sem_extensao}.parquet")
    df.to_parquet(parquet_path)

    return parquet_path

def converter_para_csv(caminho_local, nome_arquivo, destino):
    
    extensao = os.path.splitext(nome_arquivo)[1].lower()

    if extensao == ".dbc":
        dbf_path = caminho_local.replace(".dbc", ".dbf")
        pyreaddbc.dbc2dbf(caminho_local, dbf_path)
        caminho_para_ler = dbf_path
    elif extensao == ".dbf":
        caminho_para_ler = caminho_local
    else:
        raise ValueError("Formato não suportado para conversão.")

    df = pd.DataFrame(iter(dbfread.DBF(caminho_para_ler)))

    nome_sem_extensao = os.path.splitext(nome_arquivo)[0]
    csv_path = os.path.join(destino, f"{nome_sem_extensao}.csv")
    df.to_csv(csv_path, index=False)

    return csv_path

def converter_para_orc(caminho_local, nome_arquivo, destino):
    
    extensao = os.path.splitext(nome_arquivo)[1].lower()

    if extensao == ".dbc":
        dbf_path = caminho_local.replace(".dbc", ".dbf")
        pyreaddbc.dbc2dbf(caminho_local, dbf_path)
        caminho_para_ler = dbf_path
    elif extensao == ".dbf":
        caminho_para_ler = caminho_local
    else:
        raise ValueError("Formato não suportado para conversão.")

    df = pd.DataFrame(iter(dbfread.DBF(caminho_para_ler)))
    
    nome_sem_extensao = os.path.splitext(nome_arquivo)[0]
    orc_path = os.path.join(destino, f"{nome_sem_extensao}.orc")

    table = pa.Table.from_pandas(df)
    with open(orc_path, "wb") as f:
        orc.write_table(table, f)

    return orc_path

def baixar_arquivo_ftp(ftp: FTP, remote_path: str, local_path: str):
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    with open(local_path, 'wb') as f:
        ftp.retrbinary(f"RETR {remote_path}", f.write)