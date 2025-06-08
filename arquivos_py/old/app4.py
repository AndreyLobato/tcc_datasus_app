import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Catálogo de Arquivos", layout="wide")
st.title("📁 Navegador de Arquivos")

# Estado inicial da pasta
if "caminho_atual" not in st.session_state:
    st.session_state["caminho_atual"] = "/"

# Conexão com SQLite
@st.cache_resource
def conectar():
    return sqlite3.connect("catalogo_arquivos.db", check_same_thread=False)

conn = conectar()

# Função para listar arquivos da pasta atual
def listar_conteudo(pasta_atual):
    query = """
        SELECT * FROM arquivos
        WHERE parent_path = ?
        ORDER BY is_dir DESC, nome
    """
    return pd.read_sql_query(query, conn, params=(pasta_atual,))

# Função para listar subpastas
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

# Navegação
caminho_atual = st.session_state["caminho_atual"]
st.markdown(f"📂 **Caminho atual:** `{caminho_atual}`")

# Botão voltar
if caminho_atual != "/":
    if st.button("🔙 Voltar"):
        novo = "/".join(caminho_atual.rstrip("/").split("/")[:-1])
        st.session_state["caminho_atual"] = novo if novo else "/"
        st.rerun()

# Mostrar subpastas
subpastas = listar_subpastas(caminho_atual)
for sub in subpastas:
    if st.button(f"📁 {sub}"):
        novo_caminho = f"{caminho_atual.rstrip('/')}/{sub}"
        st.session_state["caminho_atual"] = novo_caminho
        st.rerun()

# Mostrar arquivos da pasta atual
df = listar_conteudo(caminho_atual)
arquivos = df[df["is_dir"] == 0]

for _, arq in arquivos.iterrows():
    nome = arq["nome"]
    tamanho_kb = arq["tamanho"] / 1024 if pd.notnull(arq["tamanho"]) else 0
    st.markdown(f"📄 **{nome}** — `{tamanho_kb:.1f} KB`")
    st.download_button(
        label="⬇️ Simular Download",
        data="Conteúdo simulado",
        file_name=nome,
        key=arq["path"]
    )
