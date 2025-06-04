# pages/1_processamento.py

import streamlit as st
import os
import zipfile
import io
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
                            st.success("Conversão para CSV concluída!")

                with col2:
                    if st.button("🧪 Parquet"):
                        with st.spinner("Convertendo para Parquet..."):
                            for _, row in df.iterrows():
                                local_temp = os.path.join("temp", "arquivos_baixados", row['nome'])
                                baixar_arquivo_ftp(ftp, row['path'], local_temp)
                                converter_para_parquet(local_temp, row['nome'], "convertidos")
                            st.success("Conversão para Parquet concluída!")

                with col3:
                    if st.button("📦 ORC"):
                        with st.spinner("Convertendo para ORC..."):
                            for _, row in df.iterrows():
                                local_temp = os.path.join("temp", "arquivos_baixados", row['nome'])
                                baixar_arquivo_ftp(ftp, row['path'], local_temp)
                                converter_para_orc(local_temp, row['nome'], "convertidos")
                            st.success("Conversão para ORC concluída!")
    
            st.markdown("### ⬇️ Arquivos convertidos disponíveis para download")

            pasta_convertidos = "convertidos"
            arquivos_convertidos = os.listdir(pasta_convertidos)

            # Listar arquivos
            arquivos_convertidos = sorted(os.listdir(pasta_convertidos))

            # Botão para selecionar todos
            if "checklist_selecionados" not in st.session_state:
                st.session_state["checklist_selecionados"] = {nome: False for nome in arquivos_convertidos}

            if st.button("✅ Selecionar todos"):
                for nome in arquivos_convertidos:
                    st.session_state["checklist_selecionados"][nome] = True
                st.rerun()

            # Botão para limpar seleção
            if st.button("🗑️ Limpar selecionados para download"):
                for nome in arquivos_convertidos:
                    st.session_state["checklist_selecionados"][nome] = False
                st.rerun()

            # Checklist manual com checkboxes individuais
            selecionados = []
            for nome in arquivos_convertidos:
                marcado = st.checkbox(f"{nome}", value=st.session_state["checklist_selecionados"].get(nome, False), key=f"chk_{nome}")
                st.session_state["checklist_selecionados"][nome] = marcado
                if marcado:
                    selecionados.append(nome)

            # Mostrar botão de download se houver selecionados
            if selecionados:
                st.markdown("### 📦 Baixar arquivos selecionados")

                # Botões individuais
                for nome_arquivo in selecionados:
                    caminho = os.path.join(pasta_convertidos, nome_arquivo)
                    with open(caminho, "rb") as f:
                        conteudo = f.read()
                    st.download_button(
                        label=f"📥 Baixar {nome_arquivo}",
                        data=conteudo,
                        file_name=nome_arquivo,
                        mime="application/octet-stream"
                    )

                # Botão ZIP
                buffer = io.BytesIO()
                with zipfile.ZipFile(buffer, "w") as zipf:
                    for nome_arquivo in selecionados:
                        caminho = os.path.join(pasta_convertidos, nome_arquivo)
                        zipf.write(caminho, arcname=nome_arquivo)

                buffer.seek(0)
                st.download_button(
                    label="📦 Baixar ZIP com selecionados",
                    data=buffer,
                    file_name="arquivos_convertidos.zip",
                    mime="application/zip"
                )




def main():

    conn = conectar()
    mostrar_arquivos_selecionados(conn)

if __name__ == "__main__":
    main()