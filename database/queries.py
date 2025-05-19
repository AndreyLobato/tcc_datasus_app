# Funções para consultas SQL
import pandas as pd

def get_subpastas(conn, caminho_atual):
    """Busca as subpastas diretas do caminho atual."""
    query = """
        SELECT DISTINCT parent_path FROM arquivos
        WHERE parent_path LIKE ? AND parent_path != ?
    """
    like_expr = caminho_atual.rstrip("/") + "/%"
    df = pd.read_sql_query(query, conn, params=(like_expr, caminho_atual))

    resultado = set()
    for p in df["parent_path"]:
        rel_path = p[len(caminho_atual):].strip("/")
        if "/" in rel_path:
            resultado.add(rel_path.split("/")[0])
        elif rel_path:
            resultado.add(rel_path)
    return sorted(resultado)

def buscar_arquivos(conn, caminho, termo, offset, limite):
    """Busca arquivos no caminho atual com termo e paginação."""
    termo_sql = f"%{termo.lower()}%"
    query = """
        SELECT * FROM arquivos
        WHERE parent_path = ? AND LOWER(nome) LIKE ? AND is_dir = 0
        ORDER BY nome
        LIMIT ? OFFSET ?
    """
    return pd.read_sql_query(query, conn, params=(caminho, termo_sql, limite, offset))

def contar_arquivos(conn, caminho, termo):
    """Conta arquivos para a paginação."""
    termo_sql = f"%{termo.lower()}%"
    query = """
        SELECT COUNT(*) as total FROM arquivos
        WHERE parent_path = ? AND LOWER(nome) LIKE ? AND is_dir = 0
    """
    return pd.read_sql_query(query, conn, params=(caminho, termo_sql))["total"].iloc[0]

def listar_nomes_arquivos_unicos(conn, caminho):
    """Retorna lista única de nomes de arquivos no caminho atual."""
    query = """
        SELECT DISTINCT nome FROM arquivos
        WHERE parent_path = ? AND is_dir = 0
        ORDER BY nome
    """
    df = pd.read_sql_query(query, conn, params=(caminho,))
    return df["nome"].tolist()
