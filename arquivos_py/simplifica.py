from ftplib import FTP, error_perm
import csv

# Configurações do FTP
FTP_HOST = "ftp.datasus.gov.br"
FTP_USER = ""
FTP_PASS = ""
#REMOTE_DIR = "/dissemin/publicos/"
REMOTE_DIR ="/dissemin/publicos/SIASUS/200801_"

def listar_nomes(ftp):
    ftp.cwd(REMOTE_DIR)
    ftp.cwd("Dados")
    arquivos = ftp.nlst()  # Lista os arquivos disponíveis
    #diretorio = ftp.retrlines("LIST")
    #tipo = diretorio.split(" ")[2]
    print(ftp.size("SADTO1512.dbc"))
    #print(arquivos)
    return arquivos#, diretorio


ftp = FTP(FTP_HOST, FTP_USER, FTP_PASS)
ftp.login()
ftp.encoding = 'latin-1'

lista_nomes = listar_nomes(ftp)


         # diretório de arquivos: {lista_diretorio}\n""") 
          #tipo dos arquivos: {tipo}\n""")