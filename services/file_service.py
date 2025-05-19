# Lógica de negócio relacionada a arquivos (exibir, navegar, etc)

import streamlit as st
from database.queries import buscar_arquivos, contar_arquivos,listar_nomes_arquivos_unicos,listar_filtros_unicos,obter_traducoes_distintas
import math

# Conversão segura dos filtros para inteiros
def filtrar_inteiros(valores):
    return [int(v) for v in valores if v is not None and str(v).isdigit()]

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

    filtros = listar_filtros_unicos(conn, caminho_atual)

    col1, col2, col3 = st.columns(3)
    with col1:

        st.multiselect("📍 UF", filtros["uf"], key="filtro_uf")
        st.multiselect("🔧 Subsistema", filtros["subsistema_traducao"], key="filtro_sigla_subsistema")

    with col2:

        st.multiselect("📆 Mês", filtros["mes"], key="filtro_mes")
        st.multiselect("📅 Ano", filtros["ano"], key="filtro_ano")

    with col3:

        st.multiselect("🧩 Extensão", filtros["extensao"], key="filtro_extensao")
        st.multiselect("🗂️ Complemento", filtros["complemento"], key="filtro_complemento")

    pagina = st.session_state.get("pagina_atual", 1)
    por_pagina = 10
    
    termo_busca = st.session_state.get("busca", "")
    nomes_filtro = st.session_state.get("filtro_nomes", [])

    filtros_selecionados = {
        "subsistema_traducao": st.session_state.get("filtro_sigla_subsistema", []),
        "uf": st.session_state.get("filtro_uf", []),
        "mes": filtrar_inteiros(st.session_state.get("filtro_mes", [])),
        "ano": filtrar_inteiros(st.session_state.get("filtro_ano", [])),
        "extensao": st.session_state.get("filtro_extensao", []),
        "complemento": st.session_state.get("filtro_complemento", [])
    }


    total = contar_arquivos(conn, caminho_atual, termo_busca, nomes_filtro, filtros_selecionados)
    total_paginas = max(1, math.ceil(total / por_pagina))

    df = buscar_arquivos(conn, caminho_atual, termo_busca, nomes_filtro, filtros_selecionados, (pagina - 1) * por_pagina, por_pagina)

    selecionados = st.session_state.get("selecionados", set())
    novos_selecionados = set()

    st.markdown(f"📄 **{total} arquivo(s)** — Página {pagina} de {total_paginas}")
    for _, arq in df.iterrows():
        chave_checkbox = f"check_{arq['path']}"
        if st.checkbox(f"📄 {arq['nome']} — `{arq['tamanho'] / 1024:.1f} KB`", key=chave_checkbox):
            novos_selecionados.add(arq["path"])

    # Atualiza os selecionados
    st.session_state["selecionados"] = st.session_state.get("selecionados", set()).union(novos_selecionados)

    if st.session_state.get("selecionados"):
        if st.button("➡️ Prosseguir"):
            st.session_state["pagina_destino"] = "processamento"
            st.rerun()
    else:
        st.info("Selecione pelo menos um arquivo para continuar.")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅️ Anterior") and pagina > 1:
            st.session_state["pagina_atual"] -= 1
            st.rerun()
    with col3:
        if st.button("➡️ Próxima") and pagina < total_paginas:
            st.session_state["pagina_atual"] += 1
            st.rerun()
    
    traducoes_df = obter_traducoes_distintas(conn)
    if not traducoes_df.empty:
        st.markdown("### ℹ️ Tradução de Setores")
        for _, row in traducoes_df.iterrows():
            st.markdown(f"- `{row['sigla_sistema']}` → {row['sistema_traducao']}")
    
    
