# pages/1_processamento.py

import streamlit as st

def mostrar_arquivos_selecionados():
    """Exibe os arquivos selecionados na etapa anterior."""
    st.title("📦 Arquivos Selecionados")

    selecionados = st.session_state.get("selecionados", [])

    if not selecionados:
        st.warning("Nenhum arquivo selecionado.")
        if st.button("🔙 Voltar"):
            st.session_state["pagina_destino"] = "principal"
            st.rerun()
        return

    for caminho in selecionados:
        st.markdown(f"📄 `{caminho}`")

    # Aqui você pode colocar mais ações, como conversão, upload, etc.
    st.success("Aqui você pode realizar ações com os arquivos selecionados.")
    if st.button("🔙 Voltar"):
        st.session_state["pagina_destino"] = "principal"
        st.rerun()

mostrar_arquivos_selecionados()
