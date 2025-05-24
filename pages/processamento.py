# pages/1_processamento.py

import streamlit as st
import os

def mostrar_arquivos_selecionados():
    st.title("📦 Arquivos Selecionados")

    selecionados = st.session_state.get("selecionados", [])

    for caminho in selecionados:
        nome_arquivo = os.path.basename(caminho)
        st.markdown(f"📄 `{nome_arquivo}`")
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

def mostrar_processamento(conn):
    st.title("🔧 Processamento dos Arquivos Selecionados")

    selecionados = st.session_state.get("selecionados", [])

    st.write("Arquivos selecionados:")
    for path in selecionados:
        st.markdown(f"- `{path}`")

    if st.button("🔙 Voltar"):
        st.session_state["pagina_destino"] = "navegacao"
        st.rerun()
    
mostrar_arquivos_selecionados()
