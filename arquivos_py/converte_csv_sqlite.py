import pandas as pd
import sqlite3
from pathlib import PurePosixPath

# Carregar CSV
df = pd.read_csv("~/Projetos/tcc_app/tcc_datasus_app/arquivos_py/df_arquivos_sus.csv")  
df_catalogo = pd.read_csv("~/Projetos/tcc_app/tcc_datasus_app/data/de-para-catalogo-datasus.csv")

# Preprocessar
df["parent_path"] = df["path"].apply(lambda p: str(PurePosixPath(p).parent))
#df["is_dir"] = False  # por enquanto tudo é arquivo

def parse_nome_arquivo(nome, path, parent_path):
    sigla_sistema, tipo, uf, mes, ano, extensao, complemento = None, None, None, None,None ,None,None 
    if nome.split('.')[1] in ['dbc', 'dbf', 'DBC', 'DBF']:
        match path.split('/')[3].upper(): 

            case "SIASUS" | "CIH"|"CNES"|"SISCAN"|"SISPRENATAL"|"SIHSUS": 
                # tratamento dos casos em que apresenta complemento "_1 e _2"
                if ("BI" in nome[0:3]) and (len(nome) > 12): 
                    complemento = nome[8:10]
                    tipo = nome[0:2]
                    uf = nome[2:4].upper()
                    if int(nome[4:6]) > 50:
                        ano = 1900 + int(nome[4:6])
                    else:
                        ano = 2000 + int(nome[4:6])
                    mes = int(nome[6:8])
               
                elif ("PA" in nome[0:3]) and (len(nome) > 12):
                    complemento = nome[8:10]
                    tipo = nome[0:2]
                    uf = nome[2:4].upper()

                    # considera numeros baixos do sec 21 e numeros altos seculo 21
                    if int(nome[4:6]) > 50:
                        ano = 1900 + int(nome[4:6])
                    else:
                        ano = 2000 + int(nome[4:6])
                    
                    #separa a informação sobre o mes da base
                    mes = int(nome[6:8])
                
                elif (len(nome) > 12):
                    tipo = nome[0:3].upper()
                    uf = nome[3:5].upper()
                    try:
                        if int(nome[5:7]) > 50:
                            ano = 1900 + int(nome[5:7])
                        else:
                            ano = 2000 + int(nome[5:7])
                            mes = int(nome[7:9])
                    except:
                        pass

                else:
                    tipo = nome[0:2].upper()

                    #separa a informação sobre a unidade federativa - RJ, SP
                    uf = nome[2:4].upper()
                    
                    try:
                        # considera numeros baixos do sec 21 e numeros altos seculo 21
                        if int(nome[4:6]) > 50:
                            ano = 1900 + int(nome[4:6])
                        else:
                            ano = 2000 + int(nome[4:6])

                        #separa a informação sobre o mes da base
                        mes = int(nome[6:8])
                    except:
                        pass

                #separa a informação sobre a extensao do arquivo 
                extensao = nome.split('.')[1]
            
            case "CIHA":

                tipo = nome[0:4].upper()

                #separa a informação sobre a unidade federativa - RJ, SP
                uf = nome[4:6].upper()

                # considera numeros baixos do sec 21 e numeros altos seculo 21
                if int(nome[6:8]) > 50:
                    ano = 1900 + int(nome[6:8])
                else:
                    ano = 2000 + int(nome[6:8])

                #separa a informação sobre o mes da base
                mes = int(nome[8:10])

                #separa a informação sobre a extensao do arquivo 
                extensao = nome.split('.')[1]
            case "PCE":

                tipo = nome[0:3].upper()

                #separa a informação sobre a unidade federativa - RJ, SP
                uf = nome[3:5].upper()

                # considera numeros baixos do sec 21 e numeros altos seculo 21
                if int(nome[5:7]) > 50:
                    ano = 1900 + int(nome[5:7])
                else:
                    ano = 2000 + int(nome[5:7])

                #separa a informação sobre a extensao do arquivo 
                extensao = nome.split('.')[1]            
          
            case "PNI":
                tipo = nome[0:4].upper()

                #separa a informação sobre a unidade federativa - RJ, SP
                uf = nome[4:6].upper()

                # considera numeros baixos do sec 21 e numeros altos seculo 21
                # tem um caso com numero no lugar de letra por isso o try
                try: 
                    if int(nome[6:8]) > 50:
                        ano = 1900 + int(nome[6:8])
                    else:
                        ano = 2000 + int(nome[6:8])
                except:
                    ano = None
                #CPNI AC 14.dbf

                #separa a informação sobre a extensao do arquivo 
                extensao = nome.split('.')[1]
            case "PAINEL_ONCOLOGIA":
                #POBR2013.dbc
                tipo = nome[0:2].upper()

                #separa a informação sobre a unidade federativa - RJ, SP
                uf = nome[2:4].upper()

                # considera numeros baixos do sec 21 e numeros altos seculo 21
                ano = int(nome[4:8])

                #separa a informação sobre a extensao do arquivo 
                extensao = nome.split('.')[1]
            case "RESP":
                #RESPAC15.dbc

                tipo = nome[0:4].upper()

                #separa a informação sobre a unidade federativa - RJ, SP
                uf = nome[4:6].upper()

                try: 
                    if int(nome[6:8]) > 50:
                        ano = 1900 + int(nome[6:8])
                    else:
                        ano = 2000 + int(nome[6:8])
                except:
                    ano = None

                #separa a informação sobre a extensao do arquivo 
                extensao = nome.split('.')[1]
            case "SIM":
                extensao = nome.split('.')[1]
                if 'DORES' in parent_path:
                    if len(nome) >= 12: 
                        tipo = nome[0:2].upper()
                        uf = nome[2:4].upper()
                        ano = int(nome[4:8])
                    else:
                        tipo = nome[0:3].upper()
                        uf = nome[3:5].upper()
                        if int(nome[5:7]) > 50:
                            ano = 1900 + int(nome[5:7])
                        else:
                            ano = 2000 + int(nome[5:7])
                elif "TABELAS" not in parent_path:
                        nome_sem_extensao = nome.split(".")[0]
                        tipo = nome_sem_extensao[0:-2].upper()
                        try:
                            if int(nome_sem_extensao[-2:]) > 50:
                                ano = 1900 + int(nome_sem_extensao[-2:])
                            else:
                                ano = 2000 + int(nome_sem_extensao[-2:])
                        except:
                            pass
            case "SINAN":
                extensao = nome.split('.')[1]
                nome_sem_extensao = nome.split(".")[0]
                tipo = nome_sem_extensao[0:-4].upper()
                uf = nome_sem_extensao[-4:-2].upper()
                try:
                    if int(nome_sem_extensao[-2:]) > 50:
                        ano = 1900 + int(nome_sem_extensao[-2:])
                    else:
                        ano = 2000 + int(nome_sem_extensao[-2:])
                except:
                    pass
            case "SINASC":
                if "TABELAS" not in parent_path:
                    extensao = nome.split('.')[1]
                    if len(nome) == 13:
                        tipo = nome[0:3]
                        uf = nome[3:5]
                        try:
                            ano = int(nome[5:9])
                        except:
                            pass
                    else:
                        if nome[0:4] == "DNEX":
                            tipo = nome[0:4]
                            ano = nome[4:8]
                        else:
                            tipo = nome[0:2]
                            uf = nome[2:4]
                            try:
                                ano = int(nome[4:8]) 
                            except:
                                pass

    else:
        tipo, uf, mes, ano, extensao, complemento = None
    sigla_sistema = path.split('/')[3].upper()
    return sigla_sistema, tipo, uf, mes, ano, extensao, complemento

# Criar SQLite
conn = sqlite3.connect("catalogo_arquivos.db")
#conn = sqlite3.connect("teste_SIASUS.db")
cursor = conn.cursor()

# Limpar dados antigos (caso rode mais de uma vez)
#cursor.execute("DELETE FROM arquivos")
#cursor.execute("DELETE FROM de_para")

# Criar tabela arquivos
cursor.execute("""
CREATE TABLE IF NOT EXISTS arquivos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    tamanho INTEGER,
    path TEXT,
    parent_path TEXT,
    path_new TEXT,
    parent_path_new TEXT,
    sigla_sistema TEXT,
    sigla_subsistema TEXT,
    uf TEXT, 
    mes INTEGER, 
    ano INTEGER, 
    extensao TEXT, 
    complemento TEXT
)
""")
# Criar tabela de_para
cursor.execute("""CREATE TABLE IF NOT EXISTS de_para (
    id_de_para INTEGER PRIMARY KEY AUTOINCREMENT,
    sistema_traducao TEXT,
    sigla_sistema TEXT,
    sigla_subsistema TEXT,
    subsistema_traducao TEXT)
""") 

# Inserir dados df
for _, row in df.iterrows():
    
    sigla_sistema, sigla_subsistema, uf, mes, ano, extensao, complemento = None, None, None, None,None ,None,None 
    parent_path_new, path_new = None, None
    if row["nome"].split('.')[1] in ['dbc', 'dbf', 'DBC', 'DBF']:
        sigla_sistema, sigla_subsistema, uf, mes, ano, extensao, complemento = parse_nome_arquivo(row["nome"], row["path"], row["parent_path"])
        path_new = f"""/{sigla_sistema}/{row["nome"]}"""
        parent_path_new = f"/{sigla_sistema}"
    #print(_, row["nome"], row["path"], tipo, uf, mes, ano, extensao,"\n")
    cursor.execute("""
        INSERT INTO arquivos (
                            nome, 
                            tamanho, 
                            path, 
                            parent_path,
                            path_new,
                            parent_path_new, 
                            sigla_sistema,
                            sigla_subsistema, 
                            uf,
                            mes,
                            ano,
                            extensao,
                            complemento
                   )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?)
    """, (row["nome"], row["tamanho"], row["path"], row["parent_path"],path_new, parent_path_new, sigla_sistema, sigla_subsistema, uf, mes, ano, extensao, complemento)
    )

for _, row in df_catalogo.iterrows():
    
    cursor.execute("""
        INSERT INTO de_para ( 
                                sistema_traducao,
                                sigla_sistema,
                                sigla_subsistema,
                                subsistema_traducao
                   )
        VALUES (?, ?, ?, ?)
    """, (row["sistema_traducao"], row["sigla_sistema"], row["sigla_subsistema"], row["subsistema_traducao"])
    )

conn.commit()
conn.close()

print("📦 Base SQLite criada com sucesso!")
