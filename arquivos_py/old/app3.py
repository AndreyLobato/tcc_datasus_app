import streamlit as st
import pandas as pd
from pathlib import PurePosixPath

"""versão simulando a leitura direto do arquivo csv"""

st.set_page_config(page_title="Navegação de Arquivos via CSV", layout="wide")
st.title("📁 Navegação Virtual de Arquivos")

# Simula leitura do CSV
# Aqui você pode usar: pd.read_csv("seuarquivo.csv")
# dados = pd.DataFrame({
#     "index": [0],
#     "nome": ["TAB_CIH.zip"],
#     "tamanho": [15346666],
#     "path": ["/dissemin/publicos/CIH/200801_201012/Auxiliar/TAB_CIH.zip"]
# })

dados = pd.read_csv("~/Projetos/tcc_app/tcc_datasus_app/df_arquivos_sus.csv")

# Transforma paths em objetos manipuláveis
dados["path_parts"] = dados["path"].apply(lambda x: PurePosixPath(x).parts[:-1])  # sem o nome do arquivo
dados["file_name"] = dados["path"].apply(lambda x: PurePosixPath(x).name)

# Define caminho atual na sessão
if "caminho_atual" not in st.session_state:
    st.session_state["caminho_atual"] = []

caminho_atual = st.session_state["caminho_atual"]

# Mostrar caminho atual
st.markdown(f"📂 Caminho atual: `/{'/'.join(caminho_atual)}`" if caminho_atual else "📂 Caminho atual: `/`")

# Botão voltar
if caminho_atual:
    if st.button("🔙 Voltar"):
        st.session_state["caminho_atual"] = caminho_atual[:-1]
        st.rerun()

# Filtra arquivos e subpastas que começam com esse caminho
def match_nivel(linha):
    partes = linha["path_parts"]
    if len(partes) < len(caminho_atual):
        return False
    return partes[:len(caminho_atual)] == tuple(caminho_atual)

dados_filtrados = dados[dados.apply(match_nivel, axis=1)]

# Identificar próximas subpastas disponíveis
subpastas = sorted(set(linha["path_parts"][len(caminho_atual)]
                       for _, linha in dados_filtrados.iterrows()
                       if len(linha["path_parts"]) > len(caminho_atual)))

# Mostra subpastas como botões
for pasta in subpastas:
    if st.button(f"📁 {pasta}"):
        st.session_state["caminho_atual"].append(pasta)
        st.rerun()

# Arquivos no nível atual
arquivos_nivel_atual = dados_filtrados[dados_filtrados["path_parts"].apply(lambda p: len(p) == len(caminho_atual))]

# Mostra arquivos com botão de download
for _, linha in arquivos_nivel_atual.iterrows():
    nome = linha["file_name"]
    tamanho_kb = linha["tamanho"] / 1024
    st.markdown(f"📄 **{nome}** — `{tamanho_kb:.1f} KB`")
    
    # Aqui, simula o conteúdo; substitua com leitura real se quiser
    conteudo_simulado = "Conteúdo do arquivo"
    st.download_button(
        label="⬇️ Baixar",
        data=conteudo_simulado,
        file_name=nome,
        key=nome
    )
    st.markdown("---")
