import streamlit as st
from pathlib import Path
import pandas as pd
from PIL import Image
from datetime import datetime
import os

st.set_page_config(page_title="Galeria de Arquivos", layout="wide")
st.title("🗂️ Galeria de Arquivos para Download")

# Define a pasta onde estão os arquivos
diretorio_arquivos = Path("old")
diretorio_arquivos.mkdir(exist_ok=True)

# Lista os arquivos disponíveis
arquivos = list(diretorio_arquivos.glob("*"))
if not arquivos:
    st.warning("Nenhum arquivo encontrado na pasta 'meus_arquivos'.")
    st.stop()


# Define número de colunas por linha
colunas = st.columns(3)

for idx, arquivo in enumerate(arquivos):
    col = colunas[idx % 3]  # distribui em 3 colunas

    with col:
        st.markdown("### 📄 " + arquivo.name)
        tamanho_kb = os.path.getsize(arquivo) / 1024
        data_modificacao = datetime.fromtimestamp(arquivo.stat().st_mtime).strftime('%d/%m/%Y %H:%M')

        st.write(f"📏 {tamanho_kb:.2f} KB")
        st.write(f"🕒 Modificado em: {data_modificacao}")

        with open(arquivo, "rb") as f:
            st.download_button(
                label="⬇️ Baixar",
                data=f,
                file_name=arquivo.name,
                use_container_width=True
            )
        st.markdown("---")