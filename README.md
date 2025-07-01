# 📊 TCC DATASUS App

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-ff4b4b?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Deploy](https://img.shields.io/badge/Deploy-Streamlit%20Cloud-green?logo=streamlit)](https://share.streamlit.io/)
[![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-orange)](#)

Aplicativo de conversão de bases do **portal DATASUS**.

Em meio à dificuldade atual de lidar com as bases do DATASUS (disponíveis para download de forma **granularizada e em formatos pouco amigáveis**), este app foi desenvolvido para **simplificar o processo de análise de dados**, permitindo:

✅ Download de múltiplas bases de forma instantânea  
✅ Conversão para formatos mais amigáveis (CSV, Parquet, ORC)  
✅ Visualização e filtragem por UF, subsistema, ano, mês, etc.  
✅ Interface leve com Streamlit, permitindo uso por qualquer usuário sem conhecimento técnico prévio.

---

## 🚀 Funcionalidades

- **Navegação hierárquica** por pastas das bases DATASUS
- **Filtros avançados** por sistema, subsistema, UF, ano, mês e extensão
- **Seleção múltipla de arquivos** para download ou conversão
- Conversão para:
  - CSV
  - Parquet
  - ORC
- **Download em lote (.zip)** das bases convertidas
- Limpeza automática de temporários para economia de espaço em nuvem

---

## 🗂️ Estrutura do projeto

tcc_datasus_app/
│
├── app.py # Ponto de entrada do Streamlit
│
├── config/ # Configurações globais
│ └── settings.py
│
├── convertidos/ # Armazena arquivos convertidos prontos para download
│
├── data/ # Dados persistentes e banco local
│ └── catalogo_arquivos.db
│
├── database/ # Conexão e consultas SQL
│ ├── db.py
│ └── queries.py
│
├── pages/ # Páginas adicionais do Streamlit
│ └── processamento.py
│
├── services/ # Lógicas de conversão e gerenciamento de arquivos
│ ├── conversion_service.py
│ └── file_service.py
│
├── temp/arquivos_baixados/ # Arquivos temporários baixados antes de conversão
│
├── ui/ # Componentes de interface
│ ├── components.py
│ └── layout.py
│
├── utils/ # Utilidades gerais
│ └── helpers.py
│
└── README.md # Este arquivo

---

## ⚙️ Como rodar localmente

1️⃣ **Clone o repositório:**

```bash
git clone https://github.com/seuusuario/tcc_datasus_app.git
cd tcc_datasus_app


2️⃣ Instale as dependências:

```bash
pip install -r requirements.txt

3️⃣ Execute o app:

```bash
streamlit run app.py

☁️ Deploy

Este projeto é compatível com Streamlit Cloud para deploy gratuito e escalável.

Basta conectar o repositório no Streamlit Cloud e iniciar.


📩 Contato

Em caso de dúvidas ou sugestões, entre em contato via andreylobatoem@gmail.com.