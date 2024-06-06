echo '======================================================== INICIANDO PROCESO DE TRAIN MODEL ========================================================'
echo 'Creando y activando un entorno virtual ...'
python -m venv venv

echo 'Upgrade pip ...'
./venv/bin/pip install --upgrade pip

echo 'Instalando dependencias ...'
./venv/bin/pip install -r requirements.txt

export GOOGLE_APPLICATION_CREDENTIALS="$(pwd)/gcp_credential.json"

echo 'Procesando dataset ...'
./venv/bin/python3 scr/processing_pipeline.py

echo 'Fitting model ...'
./venv/bin/python3 scr/fit_pipeline.py

echo 'Ejecutando pruebas ...'
./venv/bin/pytest --junitxml=report.xml

echo 'Limpiando entorno virtual ...'
rm -rf venv