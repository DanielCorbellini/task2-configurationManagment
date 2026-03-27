#!/bin/bash
set -e # Interrompe o script imediatamente se ocorrer algum erro

echo "🚀 Iniciando setup automatizado do projeto..."

# 0. Instalação de dependências do sistema operacional (Debian/Ubuntu)
echo "🖥️  Verificando dependências do sistema (Python e PostgreSQL)..."

# Comando para instalar os pacotes essenciais do sistema nativo
if ! command -v python3 &> /dev/null || ! command -v psql &> /dev/null; then
    echo "⚠️  Python3 ou PostgreSQL ausentes na sua máquina."
    echo "🔑 Solicitando permissão (sudo) para os instalar via instalador apt..."
    
    sudo apt-get update
    sudo apt-get install -y python3 python3-venv python3-pip postgresql postgresql-contrib
    
    # Inicia o serviço do postgresql caso esteja desligado
    sudo systemctl start postgresql || true
    
    echo "✅ Dependências do sistema instaladas!"
else
    echo "✅ Python e PostgreSQL já estão instalados no sistema."
fi

# 1. Criar o ambiente virtual
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual Python..."
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

echo "⚙️ Importando banco de dados (dump.sql) via psql..."
if [ "$DB_USER" = "postgres" ] && [ "$DB_HOST" = "localhost" ]; then
    # O postgres no Ubuntu geralmente usa 'peer authentication' e precisa rodar via sudo para o usuário padrão
    echo "🛠️ Detectado usuário postgres local. Executando via sudo..."
    sudo -u postgres psql -d postgres -f dump.sql
else
    export PGPASSWORD=$DB_PASSWORD
    psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d postgres -f dump.sql
fi

echo "✅ Setup concluído com sucesso!"
echo "➡️  Para iniciar a aplicação localmente execute: venv/bin/python app.py"
