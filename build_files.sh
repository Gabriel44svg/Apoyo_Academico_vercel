# build_files.sh
set -e  # Detener el script si hay cualquier error

echo "Building the project..."
python3.9 -m pip install -r requirements.txt

echo "Collecting static files..."
python3.9 manage.py collectstatic --noinput --clear

echo "Build End"