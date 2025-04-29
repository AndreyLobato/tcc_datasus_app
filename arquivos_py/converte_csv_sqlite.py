import pandas as pd
import sqlite3
from pathlib import PurePosixPath

# Carregar CSV
df = pd.read_csv("~/Projetos/tcc_app/tcc_datasus_app/arquivos_py/df_arquivos_sus.csv")  # substitua pelo caminho real

# Preprocessar
df["parent_path"] = df["path"].apply(lambda p: str(PurePosixPath(p).parent))
df["is_dir"] = False  # por enquanto tudo é arquivo

# Criar SQLite
conn = sqlite3.connect("catalogo_arquivos.db")
cursor = conn.cursor()

# Criar tabela
cursor.execute("""
CREATE TABLE IF NOT EXISTS arquivos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    tamanho INTEGER,
    path TEXT,
    parent_path TEXT,
    is_dir BOOLEAN
)
""")

# Limpar dados antigos (caso rode mais de uma vez)
cursor.execute("DELETE FROM arquivos")

# Inserir dados
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO arquivos (nome, tamanho, path, parent_path, is_dir)
        VALUES (?, ?, ?, ?, ?)
    """, (row["nome"], row["tamanho"], row["path"], row["parent_path"], row["is_dir"]))

conn.commit()
conn.close()

print("📦 Base SQLite criada com sucesso!")
