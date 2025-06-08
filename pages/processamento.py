# pages/1_processamento.py

import streamlit as st
import os
import zipfile
import io
import pandas as pd
from database.db import conectar
from database.queries import buscar_tamanhos_por_path 
from services.file_service import formatar_tamanho
from services.conversion_service import baixar_arquivo_ftp, converter_para_parquet, converter_para_csv, converter_para_orc, limpar_pasta
from ftplib import FTP


def mostrar_opcao_download():
    st.markdown("### 📥 Selecione os arquivos convertidos para download:")

    pasta_convertidos = "convertidos"
    arquivos_convertidos = os.listdir(pasta_convertidos)

    if "selecionados_download" not in st.session_state:
        st.session_state["selecionados_download"] = set()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Selecionar todos"):
            st.session_state["selecionados_download"] = set(arquivos_convertidos)
            st.rerun()

    with col2:
        if st.button("❌ Limpar seleção"):
            st.session_state["selecionados_download"] = set()
            st.rerun()

    # Checkboxes por arquivo
    for arquivo in arquivos_convertidos:
        checked = arquivo in st.session_state["selecionados_download"]
        if st.checkbox(arquivo, value=checked, key=f"chk_{arquivo}"):
            st.session_state["selecionados_download"].add(arquivo)
        else:
            st.session_state["selecionados_download"].discard(arquivo)

    selecionados = list(st.session_state["selecionados_download"])

    if selecionados:
        st.markdown("### 📦 Download dos Arquivos Selecionados")
        
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w") as zipf:
            for nome_arquivo in selecionados:
                caminho = os.path.join(pasta_convertidos, nome_arquivo)
                if os.path.exists(caminho):
                    zipf.write(caminho, arcname=nome_arquivo)

        buffer.seek(0)
        download = st.download_button(
            label="📥 Baixar selecionados em ZIP",
            data=buffer,
            file_name="arquivos_convertidos.zip",
            mime="application/zip"
        )

        if download:
            # Apagar os arquivos após o download
            for nome_arquivo in selecionados:
                caminho = os.path.join(pasta_convertidos, nome_arquivo)
                if os.path.exists(caminho):
                    os.remove(caminho)
            st.success("Download Feito com sucesso!")
            st.session_state["selecionados_download"] = set()


def mostrar_arquivos_selecionados(conn):

    st.title("📦 Arquivos Selecionados")

    selecionados = st.session_state.get("selecionados", [])

    df = buscar_tamanhos_por_path(conn, selecionados)

    # Exibir arquivos com tamanho individual
    for _, row in df.iterrows():
        tamanho_kb = row['tamanho'] / 1024
        st.markdown(f"- 📄 **{row['nome']}** — `{tamanho_kb:.1f} KB`")
    
    tamanho_total = df["tamanho"].sum()
    st.info(f"📦 **Tamanho total dos arquivos:** {formatar_tamanho(tamanho_total)}")

    st.markdown("### 🔄 Converter arquivos selecionados")
    
    col1, col2, col3 = st.columns(3)

    if st.button("🗑️ Limpar Selecionados Para Conversão"):
        st.session_state["selecionados"] = set()
        st.rerun()

    if not df.empty:
            with FTP('ftp.datasus.gov.br') as ftp:
                ftp.login()

                with col1:
                    if st.button("📄 CSV"):
                        with st.spinner("Convertendo para CSV..."):
                            for _, row in df.iterrows():
                                local_temp = os.path.join("temp", "arquivos_baixados", row['nome'])
                                baixar_arquivo_ftp(ftp, row['path'], local_temp)
                                converter_para_csv(local_temp, row['nome'], "convertidos")
                                limpar_pasta("temp/arquivos_baixados")
                            st.success("Conversão para CSV concluída!")

                with col2:
                    if st.button("🧪 Parquet"):
                        with st.spinner("Convertendo para Parquet..."):
                            for _, row in df.iterrows():
                                local_temp = os.path.join("temp", "arquivos_baixados", row['nome'])
                                baixar_arquivo_ftp(ftp, row['path'], local_temp)
                                converter_para_parquet(local_temp, row['nome'], "convertidos")
                                limpar_pasta("temp/arquivos_baixados")
                            st.success("Conversão para Parquet concluída!")

                with col3:
                    if st.button("📦 ORC"):
                        with st.spinner("Convertendo para ORC..."):
                            for _, row in df.iterrows():
                                local_temp = os.path.join("temp", "arquivos_baixados", row['nome'])
                                baixar_arquivo_ftp(ftp, row['path'], local_temp)
                                converter_para_orc(local_temp, row['nome'], "convertidos")
                                limpar_pasta("temp/arquivos_baixados")
                            st.success("Conversão para ORC concluída!")
    
            mostrar_opcao_download()



def main():

    conn = conectar()
    mostrar_arquivos_selecionados(conn)

if __name__ == "__main__":
    main()