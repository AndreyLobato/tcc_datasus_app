# pages/1_processamento.py

import streamlit as st
import os
import pandas as pd
from database.db import conectar
from database.queries import buscar_tamanhos_por_path 
from services.file_service import formatar_tamanho

def mostrar_arquivos_selecionados(conn):

    st.title("📦 Arquivos Selecionados")

    selecionados = st.session_state.get("selecionados", [])

    # for caminho in selecionados:
    #     nome_arquivo = os.path.basename(caminho)
    #     st.markdown(f"📄 `{nome_arquivo}`")

    df = buscar_tamanhos_por_path(conn, selecionados)

    # Exibir arquivos com tamanho individual
    for _, row in df.iterrows():
        tamanho_kb = row['tamanho'] / 1024
        st.markdown(f"- 📄 **{row['nome']}** — `{tamanho_kb:.1f} KB`")
    
    tamanho_total = df["tamanho"].sum()
    st.info(f"📦 **Tamanho total dos arquivos:** {formatar_tamanho(tamanho_total)}")

    st.markdown("### 🔄 Converter arquivos selecionados")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📄 CSV"):
            st.success("Conversão para CSV iniciada (lógica será implementada).")

    with col2:
        if st.button("🧪 Parquet"):
            st.success("Conversão para Parquet iniciada (lógica será implementada).")

    with col3:
        if st.button("📦 ORC"):
            st.success("Conversão para ORC iniciada (lógica será implementada).")


    if st.button("🗑️ Limpar Seleção"):
        st.session_state["selecionados"] = set()
        st.rerun()

def main():

    conn = conectar()
    mostrar_arquivos_selecionados(conn)

if __name__ == "__main__":
    main()