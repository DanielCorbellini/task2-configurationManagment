#!/bin/bash
set -e # Interrompe o script imediatamente se ocorrer algum erro

echo "🚀 Iniciando setup automatizado do projeto..."

# 1. Criar o ambiente virtual
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
fi

echo "🔄 Ativando ambiente virtual..."
source venv/bin/activate

# 2. Instalar as dependências do projeto
echo "📥 Instalando dependências do requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

# 3. Configurar a importação de dados
echo "🗄️ Lendo configurações do banco a partir do .env..."
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
else
    echo "Aviso: Arquivo .env não encontrado. Usando chaves padrão do postgres."
fi

DB_HOST=${DB_HOST:-localhost}
DB_PORT=${DB_PORT:-5432}
DB_USER=${DB_USER:-postgres}
export PGPASSWORD=$DB_PASSWORD

echo "⚙️ Importando banco de dados (dump.sql) via psql..."
# dump.sql tem "CREATE DATABASE", logo iniciamos com o banco default 'postgres'
psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d postgres -f dump.sql

echo "✅ Setup concluído com sucesso!"
echo "➡️  Para iniciar a aplicação localmente execute: venv/bin/python app.py"
