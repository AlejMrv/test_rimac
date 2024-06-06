from google.cloud import storage, bigquery
from google.api_core.exceptions import NotFound, Conflict
import os

current_directory = os.getcwd()
print("Directorio actual:", current_directory)
#project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PATH_CREDENTIALS = os.path.join('gcp_credential.json')
#PATH_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = PATH_CREDENTIALS

#storage_client = storage.Client()


storage_client = storage.Client()

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