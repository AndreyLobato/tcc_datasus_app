from ftplib import FTP, error_perm, all_errors
import csv
import os
import time

# Configurações do FTP
FTP_HOST = "ftp.datasus.gov.br"
FTP_USER = ""
FTP_PASS = ""
REMOTE_DIR = "/dissemin/publicos/"

def conectar_ftp():
    ftp = FTP(FTP_HOST)
    ftp.login(FTP_USER, FTP_PASS)
    ftp.encoding = 'latin-1'
    return ftp

def listar_ftp_recursivo(ftp, path='/', resultado=None, tempo_inicio=None):
    if resultado is None:
        resultado = []

    if tempo_inicio is None:
        tempo_inicio = time.time()

    # Se o caminho atual contém 'uploads', pulamos
    """if 'uploads' not in path.lower():
        print(f"Pulando o diretório proibido: {path}\n")
        return resultado """
    try:
        ftp.cwd(path)
        itens = ftp.nlst()
    except error_perm:
        return resultado
    except all_errors as e:
        print(f"Erro ao acessar {path}: {e}")
        print("Tentando reconectar...")
        ftp = conectar_ftp()
        ftp.cwd(path)
        itens = ftp.nlst()

    if ('uploads' in itens)|('uploads' in path):

        for item in itens:
            if item in ['.', '..']:
                continue
            caminho_completo = path.rstrip('/') + '/' + item
            if ('uploads' in path):
                if '.' in item:
                    try:
                        tamanho = ftp.size(caminho_completo)
                    except:
                        tamanho = 0
                    resultado.append({
                        'nome': item,
                        'tamanho': tamanho,
                        'path': caminho_completo
                    })
                else:
                    tempo_diretorio_inicio = time.time()
                    print(f"Entrando no diretório: {caminho_completo}")

                    listar_ftp_recursivo(ftp, caminho_completo, resultado, tempo_inicio)

                    tempo_diretorio_fim = time.time()
                    delta_diretorio = tempo_diretorio_fim - tempo_diretorio_inicio
                    print(f"Diretório {caminho_completo} processado em {delta_diretorio:.2f} segundos\n")
            else:
                listar_ftp_recursivo(ftp, caminho_completo, resultado, tempo_inicio)
    
    if path == REMOTE_DIR:
        tempo_total = time.time() - tempo_inicio
        print(f"\nTempo total de processamento: {tempo_total:.2f} segundos.")

    return resultado

def gerar_csv(ftp, caminho_raiz='/', nome_arquivo_csv='arquivos_ftp.csv'):
    dados = listar_ftp_recursivo(ftp, caminho_raiz)
    """
    diretorio_script = os.path.dirname(os.path.abspath(__file__))
    caminho_csv = os.path.join(diretorio_script, nome_arquivo_csv)
    
    with open(caminho_csv, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['nome', 'tamanho', 'path'])
        writer.writeheader()
        for linha in dados:
            writer.writerow(linha)
    """
    print(f"CSV não gerado com sucesso: {nome_arquivo_csv}")

if __name__ == "__main__":
    ftp = conectar_ftp()
    gerar_csv(ftp, caminho_raiz=REMOTE_DIR, nome_arquivo_csv="df_arquivos_sus_uploads.csv")
