# Imagem base leve com Python 3.12
FROM python:3.12-slim

# Instala dependências de sistema necessárias para:
#   - psycopg2-binary (libpq-dev)
#   - WeasyPrint (libpango, libgdk-pixbuf, libffi, libcairo, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    libcairo2 \
    && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia e instala as dependências Python primeiro (para aproveitar o cache de camadas)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação
COPY . .

# Expõe a porta usada pelo Flask
EXPOSE 5000

# Comando padrão para iniciar a aplicação
CMD ["python", "app.py"]
