# pages/1_processamento.py

import streamlit as st
import os
import pandas as pd
from database.db import conectar
from database.queries import buscar_tamanhos_por_path 
from services.file_service import formatar_tamanho
from services.conversion_service import baixar_arquivo_ftp, converter_para_parquet, converter_para_csv, converter_para_orc
from ftplib import FTP

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

    if not df.empty:
            with FTP('ftp.datasus.gov.br') as ftp:
                ftp.login()

                with col1:
                    if st.button("📄 CSV"):
                        with st.spinner("Convertendo para CSV..."):
                            for _, row in df.iterrows():
                                local_temp = os.path.join("temp", "arquivos_baixados", row['nome'])
                                baixar_arquivo_ftp(ftp, row['path'], local_temp)
                                converter_para_csv(local_temp, row['nome'], "convertidos/csv")
                            st.success("Conversão para CSV concluída!")

                with col2:
                    if st.button("🧪 Parquet"):
                        with st.spinner("Convertendo para Parquet..."):
                            for _, row in df.iterrows():
                                local_temp = os.path.join("temp", "arquivos_baixados", row['nome'])
                                baixar_arquivo_ftp(ftp, row['path'], local_temp)
                                converter_para_parquet(local_temp, row['nome'], "convertidos/parquet")
                            st.success("Conversão para Parquet concluída!")

                with col3:
                    if st.button("📦 ORC"):
                        with st.spinner("Convertendo para ORC..."):
                            for _, row in df.iterrows():
                                local_temp = os.path.join("temp", "arquivos_baixados", row['nome'])
                                baixar_arquivo_ftp(ftp, row['path'], local_temp)
                                converter_para_orc(local_temp, row['nome'], "convertidos/orc")
                            st.success("Conversão para ORC concluída!")


    if st.button("🗑️ Limpar Seleção"):
        st.session_state["selecionados"] = set()
        st.rerun()

def baixar_arquivos(): 
    pass


def main():

    conn = conectar()
    mostrar_arquivos_selecionados(conn)

if __name__ == "__main__":
    main()