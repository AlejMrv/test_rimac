from google.cloud import storage, bigquery
from google.api_core.exceptions import NotFound, Conflict
import os


#project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
#PATH_CREDENTIALS = os.path.join('gcp_credential.json')
PATH_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '/gcp_credential.json'

#storage_client = storage.Client()
credentials = {
  "type": "service_account",
  "project_id": "ultra-solution-424503-b2",
  "private_key_id": "5bc27aae3cf551668f003cfdb0be371c28f1c29a",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDvDGcYbdSHQW5o\n8w9j/fJ5+RJ0U2wti2wF6+JEKMWxQV9b317zTJtpHV2F3iea3058iCJuhBZrWf9p\nOLlw4yNOFklmXimHiZvZaX2xkAKQy4gSU/fMv5XWQ2D54K6mvTl+wZysOigdp/Md\n7D/rUXgK5I7MYmuaB/OIvyZMMpoNaesL3f9fZiJidHY51pYzh59Q8PF8cbGLEVPO\ng0ja9lpMkHhLq3FIKM+1IiY3UU8v4uWy2IKwyM+pdlkguW8KS66dljGB7246V6b+\nHdojRQ99akN9XxXghMxDczfoqAltcwArmA1CWQ5NAqXutg8wogzkm5K2+1aZN8S2\neVLiA5cjAgMBAAECggEAF2AOmsBuplU7Hy8ZY6067ztwVwirTN7TztZslz6najha\nw0iZ58+naMVy1jrNg6LvcVT8jPMEoDW6OIdP9t53HtUmE0kE5ZiKsV1T6a+L2K3W\nXfhxBEf9tmh7TKPwYCSjwSXclKjRMGkyaEwoSfH6+5Gy9wBuxi6d3VLXw161Wrc+\n3jnwxexIzOuRE+4xCBrxleYQAvzKr3mlpkDV2MUimbrsHRXRORSLOfXOXoN56Iu8\n0D5DyUowwCjpNChsSzVjU0WBfa/nkIfRVr3jvlXLhcWzyx4Ym72qBRBFJxuzptjw\nzeFd3DOlUCslTfFAzJWJrN+06iQck3YMV8OrS5mHCQKBgQD7Zo6tnp8d6Bhawh8K\nIdrVnwNQHlacjDhcJ60VHcfAu6wcGP0IcVvNPyDGc2rCpsX7UokT2NTSKoTEH6KH\nGPsZM+8r9lzfUJ/210Sqphr69QyZ4tGzg67Ip90zT9VbYkinx5xvK08PifqBpLoH\nZIFf6shC9AbUQsyy92GPwEdYaQKBgQDza/5d7B4XyL2yoIMUDnrtLJlyG73mG2qR\nq8+MBHzw5TgYXiV1hryKCm1MLa+vWTXyqn0XVm0RWwFERMtjZLbYsmwrWOdqXTV3\nXWMF5SoqcN46qISllHODtWFRvUfGITFFH5EhHP2rwm8qf0qYsQKa8YBPbZZirTzr\nIBBFEYYhqwKBgD2/jfHlEQ4GcNzx6y/Q6vAnU2f9W6at5jX0ZNXX77VOI1LvbE8D\nkNnT1JgJx0IyNlSpjBO84WERonSNlJz8LMie8fLpWxxasD+v1iTYEa5sPAEcLgea\no3aTjIhK5ovAkznqlGjVyWB2snnfXPXt4L0PbMrNJ1RBaAfZLTRitONpAoGBAMWI\nN0yEVQ876SRROM1Hyt04OfTtKjbWvK4lXDDlW3YorFKp43/xrIHgYD1XPZ/vpuWb\nEBOmIK/ax7ZclSe9DNvgPgMXDAO2S7LnZ3nbM1JpcQzsv2eWhf61a5nnHZ1cRh0v\ntpfGbNu61ncIAMLTsaeGnnbWGRlON4cd59YEmHItAoGBALSBlZhoqXTwINXTcEmt\nUZj3L6EzwTeeJrwo042VWkybRLVxcHU5A29HEgGmNqxkp40NfSm0ekslVS4XHCSg\nvmH7310Z8mtnyOB2v0oKQCGJVJEmSRNIRZs85nk1uTE95KSLJS7R9ty13RXH9IX8\n7DzxsvU/dmGjz9sg7lC6bM93\n-----END PRIVATE KEY-----\n",
  "client_email": "mlops-user@ultra-solution-424503-b2.iam.gserviceaccount.com",
  "client_id": "115331441664927615686",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/mlops-user%40ultra-solution-424503-b2.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}


storage_client = storage.Client(credentials=credentials)

def create_bucket(bucket_name, storage_class='STANDARD', location='us-central1'): 

    # Verificar si el bucket ya existe
    try:
        bucket = storage_client.get_bucket(bucket_name)
        return f'Bucket {bucket_name} already exists.'
    except NotFound:
        pass

    bucket = storage_client.bucket(bucket_name)
    bucket.storage_class = storage_class
   
    bucket = storage_client.create_bucket(bucket, location=location) 
    # for dual-location buckets add data_locations=[region_1, region_2]
    
    return f'Bucket {bucket.name} successfully created.'


# define function that uploads a file from the bucket
def upload_cs_file(bucket_name, source_file_name, destination_file_name, overwrite=False): 

    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(destination_file_name)

    # Verificar si el archivo ya existe en el bucket
    if overwrite==False:
        try:
            blob.reload()
            return False
        except Conflict:
            pass

    blob.upload_from_filename(source_file_name)

    return True


def download_cs_file(bucket_name, file_name, destination_file_name): 

    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(file_name)
    blob.download_to_filename(destination_file_name)

    return True


def list_cs_files(bucket_name): 

    file_list = storage_client.list_blobs(bucket_name)
    file_list = [file.name for file in file_list]

    return file_list


def create_bigquery_dataset_table(dataset_id, table_name, bucket_name, file_name):

    client = bigquery.Client()


    schema = [
        bigquery.SchemaField("Age", "INT64", mode="REQUIRED"),
        bigquery.SchemaField("Sex", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("ChestPainType", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("RestingBP", "INT64", mode="REQUIRED"),
        bigquery.SchemaField("Cholesterol", "INT64", mode="REQUIRED"),
        bigquery.SchemaField("FastingBS", "INT64", mode="REQUIRED"),
        bigquery.SchemaField("RestingECG", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("MaxHR", "INT64", mode="REQUIRED"),
        bigquery.SchemaField("ExerciseAngina", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("Oldpeak", "FLOAT64", mode="REQUIRED"),
        bigquery.SchemaField("ST_Slope", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("HeartDisease", "INT64", mode="REQUIRED"),
    ]


    dataset_ref = client.dataset(dataset_id)
    dataset = bigquery.Dataset(dataset_ref)
    try:
        dataset = client.create_dataset(dataset)
        print(f'Se ha creado el conjunto de datos {dataset.dataset_id} en BigQuery')
    except Conflict:
        print(f'El conjunto de datos {dataset_id} ya existe en BigQuery')


    table_ref = dataset_ref.table(table_name)


    job_config = bigquery.LoadJobConfig(
        schema=schema, 
        skip_leading_rows=1,  # Si el archivo tiene encabezados omite la primera fila
        source_format=bigquery.SourceFormat.CSV,  # Especifica el formato del archivo
    )

    # Carga los datos a la tabla en BigQuery
    uri = f'gs://{bucket_name}/{file_name}'
    load_job = client.load_table_from_uri(uri, table_ref, job_config=job_config)

    # Espera a que termine la carga del job
    load_job.result()

    print(f'La carga de datos desde {uri} a la tabla {table_ref.path} se ha completado.')


def get_dataset_from_bigquery(project_id, dataset_id, table_name):

    table_id = f"{project_id}.{dataset_id}.{table_name}"
    
    query = f"""       
        SELECT *
        FROM {table_id}
        """

    client = bigquery.Client()
    query_job = client.query(query)
    result = query_job.result()
    dataset = result.to_dataframe()

    return dataset