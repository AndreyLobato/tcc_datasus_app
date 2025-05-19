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

def buscar_arquivos(conn, caminho, termo, nomes_selecionados, filtros_extra, offset, limite):
    query = """
        SELECT * FROM arquivos ar
        LEFT JOIN de_para dp on ar.sigla_sistema = dp.sigla_sistema and ar.sigla_subsistema = dp.sigla_subsistema
        WHERE parent_path_new = ? AND LOWER(nome) LIKE ?
        and parent_path_new is not null
    """
    params = [caminho, f"%{termo.lower()}%"]

    if nomes_selecionados:
        placeholders = ",".join(["?"] * len(nomes_selecionados))
        query += f" AND nome IN ({placeholders})"
        params.extend(nomes_selecionados)

    for campo, valores in filtros_extra.items():
        if valores:
            ph = ",".join(["?"] * len(valores))
            query += f" AND {campo} IN ({ph})"
            params.extend(valores)

    query += " ORDER BY nome LIMIT ? OFFSET ?"
    params.extend([limite, offset])
    
    return pd.read_sql_query(query, conn, params=params)



def contar_arquivos(conn, caminho, termo, nomes_selecionados, filtros_extra):
    query = """
        SELECT COUNT(*) as total FROM arquivos ar 
        LEFT JOIN de_para dp on ar.sigla_sistema = dp.sigla_sistema and ar.sigla_subsistema = dp.sigla_subsistema
        WHERE parent_path_new = ? AND LOWER(nome) LIKE ?
        and parent_path_new is not null
    """
    params = [caminho, f"%{termo.lower()}%"]

    if nomes_selecionados:
        placeholders = ",".join(["?"] * len(nomes_selecionados))
        query += f" AND nome IN ({placeholders})"
        params.extend(nomes_selecionados)

    for campo, valores in filtros_extra.items():
        if valores:
            ph = ",".join(["?"] * len(valores))
            query += f" AND {campo} IN ({ph})"
            params.extend(valores)

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

def listar_filtros_unicos(conn, caminho):
    """Retorna os valores únicos de cada coluna usada como filtro."""
    query = """
        SELECT DISTINCT ar.sigla_sistema, dp.subsistema_traducao, uf, mes, ano, extensao, complemento
        FROM arquivos ar
        LEFT JOIN de_para dp on ar.sigla_sistema = dp.sigla_sistema and ar.sigla_subsistema = dp.sigla_subsistema
        WHERE parent_path_new = ? 
        and parent_path_new is not null
    """
    df = pd.read_sql_query(query, conn, params=(caminho,))
    return {

        "subsistema_traducao": sorted(df["subsistema_traducao"].dropna().unique()),
        "uf": sorted(df["uf"].dropna().unique()),
        "mes": sorted(df["mes"].dropna().unique()),
        "ano": sorted(df["ano"].dropna().unique()),
        "extensao": sorted(df["extensao"].dropna().unique()),
        "complemento": sorted(df["complemento"].dropna().unique())
    }
