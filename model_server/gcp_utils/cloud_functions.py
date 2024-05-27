from google.cloud import storage
import os

script_dir = os.path.dirname(os.path.realpath(__file__))
path_credentials = os.path.join(script_dir, 'gcp_credential.json')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path_credentials

storage_client = storage.Client()

def download_cs_file(bucket_name, file_name, destination_file_name): 

    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(file_name)
    blob.download_to_filename(destination_file_name)

    return True