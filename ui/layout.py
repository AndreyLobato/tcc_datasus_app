# Layout geral da interface

import streamlit as st

def show_header():
    """Cabeçalho da aplicação."""
    st.title("💊 Sistema de Gerenciamento de Dados da Saúde Brasileira")
    st.markdown("---")
    st.markdown("### **Por onde começo ?🤔**")
    st.write("- Nessa página você poderá navegar pelas principais pastas do portal DATASUS e selecionar quais bases você quer baixar.")
    st.write("- Assim que terminar de selecionar o seu conjunto de bases, vá para aba de ***processamento***. Lá você poderá escolher para qual formato seu conjunto de bases será convertido.")
    st.write("- Ficou na dúvida do que significa o nome da pasta? Sem problemas! No final da página estão as traduções de cada sigla.")
    st.markdown("---")
    st.markdown("### 📂 Catálogo de Bases do Portal DATASUS")
