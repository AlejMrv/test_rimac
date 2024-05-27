echo 'Credenciales ...'
gcloud auth activate-service-account --key-file=gcp_credential.json

echo 'Poniendo proyecto'
gcloud config set project ultra-solution-424503-b2 --quiet

echo 'Poniendo en cloud ...'
gcloud run deploy ml-service-rimac --region=us-central1 --source=$(pwd) --allow-unauthenticated --quiet