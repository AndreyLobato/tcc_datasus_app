import streamlit as st
from pathlib import Path
import pandas as pd
from PIL import Image

#st.set_page_config(page_title="Conversor de Arquivos", layout="centered")
#st.title("🗂️ Conversor de Arquivos com Download")

# Define a pasta onde estão os arquivos
diretorio_arquivos = Path("old")
diretorio_arquivos.mkdir(exist_ok=True)

# Lista os arquivos disponíveis
arquivos = list(diretorio_arquivos.glob("*"))
if not arquivos:
    st.warning("Nenhum arquivo encontrado na pasta 'meus_arquivos'.")
    st.stop()


# Seleção de arquivo
arquivo_selecionado = st.selectbox("Escolha um arquivo para conversão:", arquivos)

# Detecta o tipo de arquivo e mostra opções
opcoes = []

if arquivo_selecionado:
    if arquivo_selecionado.suffix == ".csv":
        opcoes = ["Excel (.xlsx)", "JSON (.json)"]
    elif arquivo_selecionado.suffix in [".jpg", ".jpeg", ".png"]:
        opcoes = ["PDF (.pdf)"]


if opcoes:
    conversao = st.selectbox("Escolha o formato de conversão:", opcoes)

    if st.button("Converter"):
        arquivo_convertido = None

        if conversao == "Excel (.xlsx)":
            df = pd.read_csv(arquivo_selecionado)
            destino = arquivo_selecionado.with_suffix(".xlsx")
            df.to_excel(destino, index=False)
            arquivo_convertido = destino

        elif conversao == "JSON (.json)":
            df = pd.read_csv(arquivo_selecionado)
            destino = arquivo_selecionado.with_suffix(".json")
            df.to_json(destino, orient="records", indent=2)
            arquivo_convertido = destino

        elif conversao == "PDF (.pdf)":
            imagem = Image.open(arquivo_selecionado).convert("RGB")
            destino = arquivo_selecionado.with_suffix(".pdf")
            imagem.save(destino)
            arquivo_convertido = destino

        if arquivo_convertido:
            st.success(f"Arquivo convertido: {arquivo_convertido.name}")
            with open(arquivo_convertido, "rb") as f:
                st.download_button(
                    label="📥 Baixar arquivo convertido",
                    data=f,
                    file_name=arquivo_convertido.name,
                    mime="application/octet-stream"
                )
else:
    st.info("Nenhuma conversão disponível para esse tipo de arquivo.")
