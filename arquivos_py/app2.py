import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Navegador de Arquivos", layout="wide")
st.title("📁 Navegação de Pastas e Arquivos")

# Pasta raiz
PASTA_RAIZ = Path("old").resolve()
PASTA_RAIZ.mkdir(exist_ok=True)

# Pega caminho atual salvo na sessão
if "caminho_atual" not in st.session_state:
    st.session_state["caminho_atual"] = PASTA_RAIZ

caminho_atual = Path(st.session_state["caminho_atual"])

# Botão voltar
if caminho_atual != PASTA_RAIZ:
    if st.button("🔙 Voltar"):
        st.session_state["caminho_atual"] = caminho_atual.parent
        st.rerun()

# Lista conteúdo da pasta atual
itens = sorted(caminho_atual.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))

pastas = [item for item in itens if item.is_dir()]
arquivos = [item for item in itens if item.is_file()]

# Exibe pastas como botões
for pasta in pastas:
    if st.button(f"📁 {pasta.name}"):
        st.session_state["caminho_atual"] = pasta.resolve()
        st.rerun()

# Exibe arquivos com download
for arquivo in arquivos:
    st.markdown(f"📄 **{arquivo.name}**  —  `{arquivo.stat().st_size/1024:.1f} KB`")
    with open(arquivo, "rb") as f:
        st.download_button(
            label="⬇️ Baixar",
            data=f,
            file_name=arquivo.name,
            key=arquivo.name
        )
    st.markdown("---")
