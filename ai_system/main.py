import os
import sys

# Adiciona o diretório raiz do projeto ao sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir) # Isso sobe um nível de 'ai_system' para 'EVIL_JWT_FORCE'
sys.path.insert(0, project_root)

import threading
import time
import subprocess
import json
from loguru import logger

# Configuração de logs
logger.add("ai_system/logs/main_log_{time}.log", rotation="500 MB", level="INFO")
logger.add("ai_system/logs/main_error_{time}.log", rotation="500 MB", level="ERROR")

# Importação de módulos do sistema de IA
try:
    from ai_system.monitoring.monitor import start_monitoring
    from ai_system.analysis.analyzer import train_error_predictor, predict_errors
    from ai_system.correction.corrector import apply_correction, check_predictions_and_correct
    from ai_system.evolution.evolver import analyze_for_improvements, save_suggestions, implement_improvement
except ImportError as e:
    logger.error(f"Erro ao importar módulos do sistema de IA: {str(e)}")
    sys.exit(1)

# Caminho para salvar previsões
PREDICTIONS_PATH = "ai_system/data/predictions.json"

# Função para executar o monitoramento em uma thread separada
def run_monitoring(target_pid=None):
    logger.info("Iniciando thread de monitoramento...")
    try:
        start_monitoring(target_pid)
    except Exception as e:
        logger.error(f"Erro na thread de monitoramento: {str(e)}")

# Função para executar análise e previsão
def run_analysis():
    logger.info("Iniciando análise e previsão de erros...")
    try:
        trained = train_error_predictor()
        if trained:
            prediction = predict_errors()
            if prediction:
                with open(PREDICTIONS_PATH, 'w', encoding='utf-8') as f:
                    json.dump(prediction, f, indent=2)
                logger.info(f"Previsão salva em {PREDICTIONS_PATH}")
                if prediction['prediction'] == 1:
                    logger.warning("Previsão indica alta probabilidade de erro.")
                    return "[ALERTA] Um erro é provável. Verifique o sistema."
        return "Análise concluída."
    except Exception as e:
        logger.error(f"Erro na análise: {str(e)}")
        return f"Erro na análise: {str(e)}"

# Função para executar correções
def run_correction():
    logger.info("Iniciando módulo de correção...")
    try:
        prediction_result = check_predictions_and_correct()
        return prediction_result
    except Exception as e:
        logger.error(f"Erro no módulo de correção: {str(e)}")
        return f"Erro na correção: {str(e)}"

# Função para executar evolução do código
def run_evolution():
    logger.info("Iniciando módulo de evolução...")
    try:
        suggestions = analyze_for_improvements()
        if suggestions:
            save_suggestions(suggestions)
            logger.info(f"{len(suggestions)} sugestões de melhoria geradas.")
            return f"{len(suggestions)} sugestões de melhoria geradas."
        return "Nenhuma sugestão de melhoria no momento."
    except Exception as e:
        logger.error(f"Erro no módulo de evolução: {str(e)}")
        return f"Erro na evolução: {str(e)}"

# Função para compilar e executar o monitor Rust (se disponível)
def run_rust_monitor(target_pid=None):
    rust_project_path = "ai_system/monitoring"
    if not os.path.exists(rust_project_path):
        logger.warning("Projeto Rust de monitoramento não encontrado.")
        return "Projeto Rust não encontrado."
    
    logger.info("Compilando monitor Rust...")
    try:
        # Tenta capturar a saída com encoding utf-8 e errors='ignore' para robustez
        compile_result = subprocess.run(
            ["cargo", "build", "--release", "--target", "x86_64-pc-windows-gnu"],
            cwd=rust_project_path,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'  # Ignora caracteres que não podem ser decodificados
        )
        if compile_result.returncode == 0:
            logger.info("Monitor Rust compilado com sucesso para target GNU.")
            # O nome do executável pode não mudar, mas o comportamento de vinculação sim.
            executable = os.path.join(rust_project_path, "target", "x86_64-pc-windows-gnu", "release", "process_monitor.exe")
            if not os.path.exists(executable):
                # Fallback para o caminho padrão se o específico do target não existir (embora devesse)
                executable = os.path.join(rust_project_path, "target", "release", "process_monitor.exe")
            
            if target_pid:
                cmd = [executable, str(target_pid)]
            else:
                cmd = [executable]
            logger.info(f"Executando monitor Rust: {cmd}")
            # Usar Popen para rodar em segundo plano sem esperar e sem capturar saida aqui
            subprocess.Popen(cmd, cwd=rust_project_path, creationflags=subprocess.CREATE_NEW_CONSOLE)
            return "Monitor Rust iniciado em uma nova janela."
        else:
            # Loga tanto stdout quanto stderr se houver erro de compilação
            error_message = f"Erro ao compilar monitor Rust.\nReturn Code: {compile_result.returncode}\nStdout: {compile_result.stdout}\nStderr: {compile_result.stderr}"
            logger.error(error_message)
            return f"Erro ao compilar monitor Rust: {compile_result.stderr.strip() if compile_result.stderr else 'Verifique os logs para detalhes.'}"
    except FileNotFoundError:
        logger.error("Comando 'cargo' não encontrado. Verifique se Rust está instalado e no PATH.")
        return "Comando 'cargo' não encontrado."
    except Exception as e:
        logger.error(f"Exceção ao executar monitor Rust: {str(e)}")
        return f"Exceção ao executar monitor Rust: {str(e)}"

# Função principal para orquestrar o sistema de IA
def run_ai_system(target_pid=None):
    logger.info("Iniciando sistema de IA avançado para código vivo e adaptável...")
    
    # Iniciar monitoramento Rust (se disponível)
    rust_monitor_result = run_rust_monitor(target_pid)
    print(f"[MONITOR RUST] {rust_monitor_result}")
    
    # Iniciar thread de monitoramento Python
    monitor_thread = threading.Thread(target=run_monitoring, args=(target_pid,), daemon=True)
    monitor_thread.start()
    logger.info("Thread de monitoramento Python iniciada.")
    print("[MONITOR PYTHON] Monitoramento iniciado.")
    
    # Aguardar um pouco para coletar dados iniciais
    time.sleep(10)
    
    # Executar análise
    analysis_result = run_analysis()
    print(f"[ANÁLISE] {analysis_result}")
    
    # Executar correção
    correction_result = run_correction()
    print(f"[CORREÇÃO] {correction_result}")
    
    # Executar evolução
    evolution_result = run_evolution()
    print(f"[EVOLUÇÃO] {evolution_result}")
    
    logger.info("Ciclo inicial do sistema de IA concluído.")
    print("[INFO] Ciclo inicial do sistema de IA concluído. O monitoramento continua em segundo plano.")
    print("[INFO] Pressione Ctrl+C para encerrar.")
    
    try:
        monitor_thread.join()
    except KeyboardInterrupt:
        logger.info("Sistema de IA interrompido pelo usuário.")
        print("[INFO] Sistema de IA interrompido.")

if __name__ == "__main__":
    target_pid = None
    if len(sys.argv) > 1:
        try:
            target_pid = int(sys.argv[1])
            logger.info(f"Monitorando PID específico: {target_pid}")
        except ValueError:
            logger.error(f"PID inválido fornecido: {sys.argv[1]}")
            target_pid = None
    run_ai_system(target_pid) 