FROM python:3.9

RUN apt-get update && apt-get install -y git git-lfs
RUN git lfs install

# Set working directory
WORKDIR /app

# Copy requirements file
COPY ./requirements.txt .

# Copy gcp_credentials
COPY ./gcp_credential.json .

# Copy app.py
COPY ./app/app_service.py .

# Install dependencies
RUN pip install -r requirements.txt

# Copy cloud functions
COPY ./gcp_utils/cloud_functions.py cloud_functions.py

# Download model
RUN python -c "import cloud_functions; cloud_functions.download_cs_file('mlops-model-testing', 'lightgbm_model_1.0.pkl', '/app/lightgbm_model.pkl')"

# Expose port 8080
EXPOSE 8080

# Start gunicorn
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:8080", "--timeout", "30", "--log-level", "debug", "app_service:app"]