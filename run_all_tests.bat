@echo off
setlocal EnableDelayedExpansion

set LOG_FILE=test_results.log

echo Iniciando testes automáticos em %DATE% %TIME% > %LOG_FILE%
echo --------------------------------------- >> %LOG_FILE%

echo Teste 1: Mudança de diretório
cd "C:\Users\yami_\Documents\Tramoias\Virtual Linux\EVIL_JWT_FORCE_BACKUP\EVIL_JWT_FORCE"
if %ERRORLEVEL% neq 0 (
    echo Erro ao mudar para o diretório. Verifique se o caminho está correto. >> %LOG_FILE%
    echo Teste 1: FALHOU >> %LOG_FILE%
    echo Erro ao mudar para o diretório. Verifique se o caminho está correto.
    pause
    exit /b 1
) else (
    echo Teste 1: SUCESSO - Diretório alterado com sucesso. >> %LOG_FILE%
    echo Teste 1: SUCESSO
)

echo Teste 2: Verificação da instalação do Python
python --version > nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Erro: Python não encontrado. Por favor, instale o Python 3.9 ou superior de https://www.python.org/downloads/. >> %LOG_FILE%
    echo Teste 2: FALHOU >> %LOG_FILE%
    echo Erro: Python não encontrado. Por favor, instale o Python 3.9 ou superior.
    pause
    exit /b 1
) else (
    echo Teste 2: SUCESSO - Python encontrado. >> %LOG_FILE%
    echo Teste 2: SUCESSO
)

echo Teste 3: Criação do ambiente virtual
if not exist "venv" (
    python -m venv venv
    if %ERRORLEVEL% neq 0 (
        echo Erro ao criar ambiente virtual. >> %LOG_FILE%
        echo Teste 3: FALHOU >> %LOG_FILE%
        echo Erro ao criar ambiente virtual.
        pause
        exit /b 1
    ) else (
        echo Teste 3: SUCESSO - Ambiente virtual criado. >> %LOG_FILE%
        echo Teste 3: SUCESSO
    )
) else (
    echo Teste 3: SUCESSO - Ambiente virtual já existe. >> %LOG_FILE%
    echo Teste 3: SUCESSO
)

echo Teste 4: Ativação do ambiente virtual
call venv\Scripts\activate.bat
if %ERRORLEVEL% neq 0 (
    echo Erro ao ativar ambiente virtual. Verifique se o diretório venv existe. >> %LOG_FILE%
    echo Teste 4: FALHOU >> %LOG_FILE%
    echo Erro ao ativar ambiente virtual.
    pause
    exit /b 1
) else (
    echo Teste 4: SUCESSO - Ambiente virtual ativado. >> %LOG_FILE%
    echo Teste 4: SUCESSO
)

echo Teste 5: Instalação de dependências
pip install loguru pandas numpy scikit-learn torch flask websocket-client psutil joblib
if %ERRORLEVEL% neq 0 (
    echo Erro ao instalar dependências Python. >> %LOG_FILE%
    echo Teste 5: FALHOU >> %LOG_FILE%
    echo Erro ao instalar dependências Python.
    pause
    exit /b 1
) else (
    echo Teste 5: SUCESSO - Dependências instaladas. >> %LOG_FILE%
    echo Teste 5: SUCESSO
)

echo Teste 6: Criação de diretórios para o sistema de IA
mkdir ai_system\monitoring ai_system\analysis ai_system\correction ai_system\evolution ai_system\data ai_system\logs ai_system\interfaces 2> nul
if %ERRORLEVEL% neq 0 (
    echo Erro ao criar diretórios para o sistema de IA. >> %LOG_FILE%
    echo Teste 6: FALHOU >> %LOG_FILE%
    echo Erro ao criar diretórios para o sistema de IA.
    pause
    exit /b 1
) else (
    echo Teste 6: SUCESSO - Diretórios criados. >> %LOG_FILE%
    echo Teste 6: SUCESSO
)

echo Todos os testes concluídos com sucesso! >> %LOG_FILE%
echo Todos os testes concluídos com sucesso!
echo Resultados salvos em %LOG_FILE%
echo Pressione qualquer tecla para fechar...
pause > nul 