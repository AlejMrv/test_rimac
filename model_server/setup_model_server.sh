echo '======================================================== INICIANDO PROCESO DE MICROSERVICIO ========================================================'
echo 'Creando y activando un entorno virtual ...'
python -m venv venv

echo 'Upgrade pip ...'
./venv/bin/pip install --upgrade pip
#export GOOGLE_APPLICATION_CREDENTIALS="$(pwd)/gcp_credential.json"
echo 'Instalando dependencias ...'
./venv/bin/pip install -r requirements.txt

echo 'Testing de servicio ...'