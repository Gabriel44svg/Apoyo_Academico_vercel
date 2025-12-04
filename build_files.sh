# build_files.sh
set -e

echo "Building the project..."

# 1. Asegurar que pip esté instalado (Esta línea arregla tu error actual)
python3.9 -m ensurepip --default-pip

# 2. Instalar dependencias
python3.9 -m pip install -r requirements.txt

# 3. Recolectar estáticos
echo "Collecting static files..."
python3.9 manage.py collectstatic --noinput --clear

echo "Build End"