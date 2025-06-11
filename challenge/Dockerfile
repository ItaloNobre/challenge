FROM python:3.11-bookworm

# Define diretório de trabalho
WORKDIR /home/app

# Copia os arquivos para o container
COPY . .

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    postgresql-client \
    tzdata \
    sudo \
    git \
    nano \
    curl \
    build-essential \
    libpq-dev \
    zlib1g-dev \
    libtiff-dev \
    libfreetype6 \
    libfreetype6-dev \
    libwebp-dev \
    libopenjp2-7-dev \
    && apt-get clean

# Instala dependências do Python
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Comando padrão (ajuste conforme necessário)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
