# Funções para consultas SQL
import pandas as pd

def get_subpastas(conn, caminho_atual):
    """Busca as subpastas diretas do caminho atual."""
    query = """
        SELECT DISTINCT parent_path_new FROM arquivos
        WHERE parent_path_new LIKE ? AND parent_path_new != ?
        and parent_path_new is not null
    """
    like_expr = caminho_atual.rstrip("/") + "/%"
    df = pd.read_sql_query(query, conn, params=(like_expr, caminho_atual))

    resultado = set()
    for p in df["parent_path_new"]:
        rel_path = p[len(caminho_atual):].strip("/")
        if "/" in rel_path:
            resultado.add(rel_path.split("/")[0])
        elif rel_path:
            resultado.add(rel_path)
    return sorted(resultado)

def buscar_arquivos(conn, caminho, termo, nomes_selecionados, offset, limite):
    """Busca arquivos no caminho atual filtrando por texto e nomes exatos."""
    query = """
        SELECT * FROM arquivos
        WHERE parent_path_new = ? AND LOWER(nome) LIKE ?
        and parent_path_new is not null
    """
    params = [caminho, f"%{termo.lower()}%"]

    if nomes_selecionados:
        placeholders = ",".join(["?"] * len(nomes_selecionados))
        query += f" AND nome IN ({placeholders})"
        params.extend(nomes_selecionados)

    query += " ORDER BY nome LIMIT ? OFFSET ?"
    params.extend([limite, offset])

    return pd.read_sql_query(query, conn, params=params)


def contar_arquivos(conn, caminho, termo, nomes_selecionados):
    """Conta arquivos considerando busca e filtro por nome."""
    query = """
        SELECT COUNT(*) as total FROM arquivos
        WHERE parent_path_new = ? AND LOWER(nome) LIKE ?
        and parent_path_new is not null
    """
    params = [caminho, f"%{termo.lower()}%"]

    if nomes_selecionados:
        placeholders = ",".join(["?"] * len(nomes_selecionados))
        query += f" AND nome IN ({placeholders})"
        params.extend(nomes_selecionados)

    return pd.read_sql_query(query, conn, params=params)["total"].iloc[0]


def listar_nomes_arquivos_unicos(conn, caminho):
    """Retorna lista única de nomes de arquivos no caminho atual."""
    query = """
        SELECT DISTINCT nome FROM arquivos
        WHERE parent_path_new = ? 
        and parent_path_new is not null
        ORDER BY nome
    """
    df = pd.read_sql_query(query, conn, params=(caminho,))
    return df["nome"].tolist()
