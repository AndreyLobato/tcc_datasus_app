import streamlit as st
import sqlite3
import pandas as pd
import math

st.set_page_config(page_title="Catálogo com Busca e Paginação", layout="wide")
st.title("📁 Navegador de Arquivos com Busca")

# Estados iniciais
if "caminho_atual" not in st.session_state:
    st.session_state["caminho_atual"] = "/"

if "pagina_atual" not in st.session_state:
    st.session_state["pagina_atual"] = 1

if "busca" not in st.session_state:
    st.session_state["busca"] = ""

# Conexão com SQLite
@st.cache_resource
def conectar():
    return sqlite3.connect("catalogo_arquivos.db", check_same_thread=False)

conn = conectar()

# Função: listar subpastas
def listar_subpastas(pasta_atual):
    query = """
        SELECT DISTINCT parent_path
        FROM arquivos
        WHERE parent_path LIKE ? AND parent_path != ?
    """
    like_expr = pasta_atual.rstrip("/") + "/%"
    subpastas = pd.read_sql_query(query, conn, params=(like_expr, pasta_atual))

    resultado = set()
    for p in subpastas["parent_path"]:
        rel_path = p[len(pasta_atual):].strip("/")
        if "/" in rel_path:
            resultado.add(rel_path.split("/")[0])
        elif rel_path:
            resultado.add(rel_path)
    return sorted(resultado)

# Função: listar arquivos com paginação e busca
def listar_arquivos(pasta_atual, termo_busca, offset, limite):
    busca_sql = f"%{termo_busca.lower()}%" if termo_busca else "%"
    query = """
        SELECT * FROM arquivos
        WHERE parent_path = ?
          AND LOWER(nome) LIKE ?
          AND is_dir = 0
        ORDER BY nome
        LIMIT ? OFFSET ?
    """
    return pd.read_sql_query(query, conn, params=(pasta_atual, busca_sql, limite, offset))

def contar_arquivos(pasta_atual, termo_busca):
    busca_sql = f"%{termo_busca.lower()}%" if termo_busca else "%"
    query = """
        SELECT COUNT(*) as total
        FROM arquivos
        WHERE parent_path = ?
          AND LOWER(nome) LIKE ?
          AND is_dir = 0
    """
    resultado = pd.read_sql_query(query, conn, params=(pasta_atual, busca_sql))
    return resultado["total"].iloc[0]

# Interface
caminho_atual = st.session_state["caminho_atual"]
st.markdown(f"📂 **Caminho atual:** `{caminho_atual}`")

# Botão voltar
if caminho_atual != "/":
    if st.button("🔙 Voltar"):
        novo = "/".join(caminho_atual.rstrip("/").split("/")[:-1])
        st.session_state["caminho_atual"] = novo if novo else "/"
        st.session_state["pagina_atual"] = 1
        st.rerun()

# Mostrar subpastas
subpastas = listar_subpastas(caminho_atual)
if subpastas:
    cols = st.columns(min(4, len(subpastas)))
    for i, sub in enumerate(subpastas):
        if cols[i % len(cols)].button(f"📁 {sub}"):
            novo_caminho = f"{caminho_atual.rstrip('/')}/{sub}"
            st.session_state["caminho_atual"] = novo_caminho
            st.session_state["pagina_atual"] = 1
            st.rerun()
else:
    st.info("📂 Nenhuma subpasta encontrada nesta pasta.")

# Busca
st.text_input("🔍 Buscar arquivos pelo nome", key="busca", on_change=lambda: st.session_state.update({"pagina_atual": 1}))

# Paginação
por_pagina = 10
total_arquivos = contar_arquivos(caminho_atual, st.session_state["busca"])
total_paginas = max(1, math.ceil(total_arquivos / por_pagina))
pagina = st.session_state["pagina_atual"]

offset = (pagina - 1) * por_pagina
df = listar_arquivos(caminho_atual, st.session_state["busca"], offset, por_pagina)

st.markdown(f"📄 **{total_arquivos} arquivo(s) encontrado(s)** — Página {pagina} de {total_paginas}")

# Listar arquivos
for _, arq in df.iterrows():
    nome = arq["nome"]
    tamanho_kb = arq["tamanho"] / 1024 if pd.notnull(arq["tamanho"]) else 0
    st.markdown(f"📄 **{nome}** — `{tamanho_kb:.1f} KB`")
    st.download_button(
        label="⬇️ Simular Download",
        data="Conteúdo simulado",
        file_name=nome,
        key=f"download_{arq['path']}"
    )

# Controles de página
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    if st.button("⬅️ Anterior") and pagina > 1:
        st.session_state["pagina_atual"] -= 1
        st.rerun()
with col3:
    if st.button("➡️ Próxima") and pagina < total_paginas:
        st.session_state["pagina_atual"] += 1
        st.rerun()
