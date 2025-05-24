import streamlit as st

# 🛠️ Esta linha deve vir antes de QUALQUER outro comando streamlit
st.set_page_config("Catálogo de Arquivos - DATASUS", layout="wide")

from ui.layout import show_header
from services.file_service import mostrar_arquivos
from database.db import conectar
from database.queries import get_subpastas
from pages.processamento import mostrar_processamento

def main():
   
    show_header()

    conn = conectar()
    caminho_atual = st.session_state.get("caminho_atual", "/")
    st.session_state["caminho_atual"] = caminho_atual

    pagina = st.session_state.get("pagina_destino", "navegacao")

    if pagina == "navegacao":
        subpastas = get_subpastas(conn, caminho_atual)
        mostrar_arquivos(conn, caminho_atual, subpastas)

        
    elif pagina == "processamento":
        mostrar_processamento(conn)

    else:
        st.error("Página não encontrada.")

if __name__ == "__main__":
    main()
