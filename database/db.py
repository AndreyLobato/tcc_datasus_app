# Função para conectar ao banco SQLite

import sqlite3
from config.settings import DB_PATH

# Cache da conexão para evitar múltiplas aberturas
import streamlit as st

@st.cache_resource
def conectar():
    return sqlite3.connect(DB_PATH, check_same_thread=False)