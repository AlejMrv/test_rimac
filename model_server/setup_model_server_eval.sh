echo '======================================================== INICIANDO PROCESO DE MICROSERVICIO ========================================================'
echo 'Creando y activando un entorno virtual ...'
python -m venv venv

echo 'Upgrade pip ...'
./venv/bin/pip install --upgrade pip

echo 'Instalando dependencias ...'
./venv/bin/pip install -r requirements.txt

echo 'Testing de servicio ...'
./venv/bin/pytest --junitxml=report.xml

echo 'Apagando y eliminando todos los contenedores Docker en ejecución...'
docker ps -q | xargs -r docker stop
docker ps -a -q | xargs -r docker rm

echo 'Eliminando entorno ...'
rm -rf venv