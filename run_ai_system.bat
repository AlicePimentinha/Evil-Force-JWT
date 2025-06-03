@echo off
setlocal EnableDelayedExpansion

cd "C:\Users\yami_\Documents\Tramoias\Virtual Linux\EVIL_JWT_FORCE_BACKUP\EVIL_JWT_FORCE"
if %ERRORLEVEL% neq 0 (
    echo Erro ao mudar para o diretório do projeto.
    pause
    exit /b 1
)

echo Ativando ambiente virtual...
call venv\Scripts\activate.bat
if %ERRORLEVEL% neq 0 (
    echo Erro ao ativar ambiente virtual. Verifique se o ambiente virtual foi criado com setup_advanced_environment.bat.
    pause
    exit /b 1
)

echo Iniciando sistema de IA avançado...
python ai_system\main.py %1
if %ERRORLEVEL% neq 0 (
    echo Erro ao executar o sistema de IA. Verifique os logs em ai_system\logs\.
    pause
    exit /b 1
)

echo Sistema de IA em execução. Pressione Ctrl+C no terminal para encerrar.
echo Pressione qualquer tecla para fechar esta janela...
pause > nul 