# Usa uma imagem base oficial do Python
FROM python:3.12-slim

# Instala o cron e outras dependências básicas
RUN apt-get update && apt-get install -y cron nano && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia os arquivos de requisitos e o script principal
COPY requirements.txt .
COPY coletor.py .
COPY my-cron-job /etc/cron.d/my-cron-job
COPY start.sh /app/start.sh
COPY exec.sh /app/exec.sh

# Da permissão de execução aos scripts
RUN chmod +x /etc/cron.d/my-cron-job
RUN chmod +x /app/start.sh
RUN chmod +x /app/exec.sh

# Instala as dependências do Python
RUN pip install -r requirements.txt

# Cria um log para o cron
RUN touch /var/log/cron.log

# Comando para rodar o cron em foreground, mantendo o contêiner ativo
CMD ["cron", "-f"]