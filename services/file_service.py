# Lógica de negócio relacionada a arquivos (exibir, navegar, etc)

import streamlit as st
from database.queries import buscar_arquivos, contar_arquivos
import math

def mostrar_arquivos(conn, caminho_atual, subpastas):
    """Exibe subpastas e arquivos paginados."""
    st.markdown(f"📂 **Caminho atual:** `{caminho_atual}`")

    if caminho_atual != "/":
        if st.button("🔙 Voltar"):
            novo = "/".join(caminho_atual.rstrip("/").split("/")[:-1]) or "/"
            st.session_state["caminho_atual"] = novo
            st.session_state["pagina_atual"] = 1
            st.rerun()

    if subpastas:
        cols = st.columns(min(4, len(subpastas)))
        for i, sub in enumerate(subpastas):
            if cols[i % len(cols)].button(f"📁 {sub}"):
                novo_caminho = f"{caminho_atual.rstrip('/')}/{sub}"
                st.session_state["caminho_atual"] = novo_caminho
                st.session_state["pagina_atual"] = 1
                st.rerun()
    else:
        st.info("Nenhuma subpasta.")

    st.text_input("🔍 Buscar arquivos", key="busca", on_change=lambda: st.session_state.update({"pagina_atual": 1}))
    pagina = st.session_state.get("pagina_atual", 1)
    por_pagina = 10

    total = contar_arquivos(conn, caminho_atual, st.session_state["busca"])
    total_paginas = max(1, math.ceil(total / por_pagina))

    df = buscar_arquivos(conn, caminho_atual, st.session_state["busca"], (pagina - 1) * por_pagina, por_pagina)

    st.markdown(f"📄 **{total} arquivo(s)** — Página {pagina} de {total_paginas}")
    for _, arq in df.iterrows():
        st.markdown(f"📄 **{arq['nome']}** — `{arq['tamanho'] / 1024:.1f} KB`")
        st.download_button("⬇️ Simular Download", data=b"dados", file_name=arq["nome"], key=arq["path"])

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅️ Anterior") and pagina > 1:
            st.session_state["pagina_atual"] -= 1
            st.rerun()
    with col3:
        if st.button("➡️ Próxima") and pagina < total_paginas:
            st.session_state["pagina_atual"] += 1
            st.rerun()
