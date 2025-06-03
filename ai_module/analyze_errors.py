import pandas as pd
import os
from ai_module.utils.logger import log_debug

# Caminho para o arquivo CSV de dados de erros
ERROR_DATA_PATH = "ai_module/data/errors.csv"

def analyze_errors():
    if not os.path.exists(ERROR_DATA_PATH):
        print("[INFO] Nenhum dado de erro encontrado para análise.")
        log_debug("Nenhum arquivo de dados de erros encontrado para análise.")
        return
    
    # Lê o arquivo CSV
    df = pd.read_csv(ERROR_DATA_PATH)
    if df.empty:
        print("[INFO] Arquivo de erros está vazio.")
        log_debug("Arquivo de dados de erros está vazio.")
        return
    
    # Mostra estatísticas básicas
    print("[ANÁLISE DE ERROS]")
    print(f"Total de erros registrados: {len(df)}")
    print("\nTipos de erro mais comuns:")
    error_counts = df['ErrorType'].value_counts()
    print(error_counts)
    log_debug(f"Análise de erros concluída. Total de erros: {len(df)}")
    
    # Sugestões de ações frequentes
    print("\nAções sugeridas mais comuns:")
    action_counts = df['SuggestedAction'].value_counts()
    print(action_counts)
    log_debug("Ações sugeridas analisadas.")

if __name__ == "__main__":
    log_debug("Iniciando análise de erros.")
    analyze_errors()
    log_debug("Análise de erros finalizada.") 