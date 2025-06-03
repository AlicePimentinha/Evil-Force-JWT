FROM python:3.10-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Instala dependências do sistema para Tkinter e ferramentas de rede
RUN apt-get update && apt-get install -y \
    gcc \
    tk \
    tcl \
    libx11-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copia os arquivos do projeto para o container
COPY . .

# Instala as dependências do Python manualmente
RUN pip install --no-cache-dir python-jwt PyJWT requests httpx==0.23.0 pyyaml termcolor beautifulsoup4

# Tenta instalar outras dependências do requirements.txt, ignorando erros
RUN pip install --no-cache-dir -r requirements.txt || echo 'Erro ao instalar algumas dependências, continuando para teste.'

# Remove arquivos desnecessários para reduzir o tamanho da imagem
RUN rm -rf /root/.cache /var/cache/apt/* /var/lib/apt/lists/*

# Define o comando padrão para executar o programa
CMD ["python", "main.py", "--cli", "--auto"]

# Adiciona metadados para a imagem
LABEL maintainer="EVIL_JWT_FORCE Team" \
      version="1.0" \
      description="Ferramenta de teste de segurança para JWT e injeção SQL" 