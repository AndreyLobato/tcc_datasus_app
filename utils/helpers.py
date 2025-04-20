# Funções auxiliares gerais (ex: formatar tamanho, logs)

def formatar_tamanho(bytes_):
    return f"{bytes_ / 1024:.1f} KB" if bytes_ else "-"