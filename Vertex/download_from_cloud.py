from directory_parameters import *
from google.cloud import storage
from os import listdir

file_names = listdir('data/')
output_names = [filename[:-9]+"_prediction.csv" for filename in file_names]

storage_client = storage.Client()
bucket = storage_client.bucket(gcs_bucket)

for index,filename in enumerate(file_names):
    outputname = output_names[index]
    blob = bucket.blob(f"predictions/{outputname}")
    try:
        data = blob.download_as_text()
        print(data)
        with open(f'predictions/{outputname}','w') as file:
            file.write(data)
    except:
        pass