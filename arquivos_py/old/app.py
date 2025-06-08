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


# Dicionário para armazenar seleções
selecionados = {}

# Exibir arquivos em galeria com checkbox
colunas = st.columns(3)
for idx, arquivo in enumerate(arquivos):
    col = colunas[idx % 3]

    with col:
        st.markdown("### 📄 " + arquivo.name)
        tamanho_kb = os.path.getsize(arquivo) / 1024
        data_mod = datetime.fromtimestamp(arquivo.stat().st_mtime).strftime('%d/%m/%Y %H:%M')
        st.write(f"📏 {tamanho_kb:.2f} KB")
        st.write(f"🕒 {data_mod}")

        checkbox = st.checkbox("Selecionar", key=arquivo.name)
        selecionados[arquivo] = checkbox

        st.markdown("---")

# Filtra arquivos selecionados
arquivos_escolhidos = [arq for arq, marcado in selecionados.items() if marcado]

if arquivos_escolhidos:
    st.success(f"{len(arquivos_escolhidos)} arquivo(s) selecionado(s).")

    # Criar ZIP para download
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as zipf:
        for arquivo in arquivos_escolhidos:
            zipf.write(arquivo, arcname=arquivo.name)
    buffer.seek(0)

    st.download_button(
        label="📦 Baixar selecionados como ZIP",
        data=buffer,
        file_name="arquivos_selecionados.zip",
        mime="application/zip"
    )
else:
    st.info("Nenhum arquivo selecionado.")
    
"""Versão com multiselect"""
# # Seleção múltipla
# selecionados = st.multiselect("Selecione os arquivos para download:", arquivos)

# # Mostrar botões de download para cada selecionado
# for arquivo in selecionados:
#     with open(arquivo, "rb") as f:
#         st.download_button(
#             label=f"📥 Baixar: {arquivo.name}",
#             data=f,
#             file_name=arquivo.name
#         )

"""Versão com galeria"""
# # Define número de colunas por linha
# colunas = st.columns(3)

# for idx, arquivo in enumerate(arquivos):
#     col = colunas[idx % 3]  # distribui em 3 colunas

#     with col:
#         st.markdown("### 📄 " + arquivo.name)
#         tamanho_kb = os.path.getsize(arquivo) / 1024
#         data_modificacao = datetime.fromtimestamp(arquivo.stat().st_mtime).strftime('%d/%m/%Y %H:%M')

#         st.write(f"📏 {tamanho_kb:.2f} KB")
#         st.write(f"🕒 Modificado em: {data_modificacao}")

#         with open(arquivo, "rb") as f:
#             st.download_button(
#                 label="⬇️ Baixar",
#                 data=f,
#                 file_name=arquivo.name,
#                 use_container_width=True
#             )
#         st.markdown("---")