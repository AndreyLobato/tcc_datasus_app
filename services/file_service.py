# Lógica de negócio relacionada a arquivos (exibir, navegar, etc)

import streamlit as st
from database.queries import buscar_arquivos, contar_arquivos,listar_nomes_arquivos_unicos,listar_filtros_unicos,obter_traducoes_distintas
import math

# Conversão segura dos filtros para inteiros
def filtrar_inteiros(valores):
    return [int(v) for v in valores if v is not None and str(v).isdigit()]

def mostrar_arquivos(conn, caminho_atual, subpastas):
    st.markdown(f"\U0001F4C2 **Caminho atual:** `{caminho_atual}`")

    mostrar_botao_voltar(caminho_atual)
    mostrar_subpastas(caminho_atual, subpastas)
    filtros = mostrar_filtros(conn, caminho_atual)
    mostrar_lista_arquivos(conn, caminho_atual, filtros)
    mostrar_traducoes_setores(conn)

def mostrar_botao_voltar(caminho_atual):
    if caminho_atual != "/":
        if st.button("\U0001F519 Voltar"):
            novo = "/".join(caminho_atual.rstrip("/").split("/")[:-1]) or "/"
            st.session_state["caminho_atual"] = novo
            st.session_state["pagina_atual"] = 1
            st.rerun()

def mostrar_subpastas(caminho_atual, subpastas):
    if subpastas:
        cols = st.columns(min(4, len(subpastas)))
        for i, sub in enumerate(subpastas):
            if cols[i % len(cols)].button(f"\U0001F4C1 {sub}"):
                novo_caminho = f"{caminho_atual.rstrip('/')}/{sub}"
                st.session_state["caminho_atual"] = novo_caminho
                st.session_state["pagina_atual"] = 1
                st.rerun()

def mostrar_filtros(conn, caminho_atual):
    filtros = listar_filtros_unicos(conn, caminho_atual)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.multiselect("\U0001F4CD UF", filtros["uf"], key="filtro_uf")
        st.multiselect("\U0001F527 Subsistema", filtros["subsistema_traducao"], key="filtro_sigla_subsistema")
    with col2:
        st.multiselect("\U0001F4C6 Mês", filtros["mes"], key="filtro_mes")
        st.multiselect("\U0001F4C5 Ano", filtros["ano"], key="filtro_ano")
    with col3:
        st.multiselect("\U0001F9E9 Extensão", filtros["extensao"], key="filtro_extensao")
        st.multiselect("\U0001F5C2️ Complemento", filtros["complemento"], key="filtro_complemento")

    return {
        "subsistema_traducao": st.session_state.get("filtro_sigla_subsistema", []),
        "uf": st.session_state.get("filtro_uf", []),
        "mes": filtrar_inteiros(st.session_state.get("filtro_mes", [])),
        "ano": filtrar_inteiros(st.session_state.get("filtro_ano", [])),
        "extensao": st.session_state.get("filtro_extensao", []),
        "complemento": st.session_state.get("filtro_complemento", [])
    }

def mostrar_lista_arquivos(conn, caminho_atual, filtros_selecionados):
    pagina = st.session_state.get("pagina_atual", 1)
    por_pagina = 10
    termo_busca = st.session_state.get("busca", "")
    nomes_filtro = st.session_state.get("filtro_nomes", [])

    total = contar_arquivos(conn, caminho_atual, termo_busca, nomes_filtro, filtros_selecionados)
    total_paginas = max(1, math.ceil(total / por_pagina))

    df = buscar_arquivos(conn, caminho_atual, termo_busca, nomes_filtro, filtros_selecionados, (pagina - 1) * por_pagina, por_pagina)

    selecionados = st.session_state.get("selecionados", set())
    novos_selecionados = set()

    st.markdown(f"\U0001F4C4 **{total} arquivo(s)** — Página {pagina} de {total_paginas}")
    for _, arq in df.iterrows():
        chave_checkbox = f"check_{arq['path']}"
        if st.checkbox(f"\U0001F4C4 {arq['nome']} — `{arq['tamanho'] / 1024:.1f} KB`", key=chave_checkbox):
            novos_selecionados.add(arq["path"])

    st.session_state["selecionados"] = selecionados.union(novos_selecionados)

    if st.session_state.get("selecionados"):
        if st.button("➡️ Prosseguir"):
            st.session_state["pagina_destino"] = "processamento"
            st.rerun()
    else:
        st.info("Selecione pelo menos um arquivo para continuar.")

    col1, _, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅️ Anterior") and pagina > 1:
            st.session_state["pagina_atual"] -= 1
            st.rerun()
    with col3:
        if st.button("➡️ Próxima") and pagina < total_paginas:
            st.session_state["pagina_atual"] += 1
            st.rerun()

def mostrar_traducoes_setores(conn):
    traducoes_df = obter_traducoes_distintas(conn)
    if not traducoes_df.empty:
        st.markdown("### ℹ️ Tradução de Setores")
        for _, row in traducoes_df.iterrows():
            st.markdown(f"- `{row['sigla_sistema']}` → {row['sistema_traducao']}")
