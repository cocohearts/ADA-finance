from directory_parameters import *
from google.cloud import storage
from os import listdir
from get_tickers import get_tickers
# tickers = get_tickers()

# file_names = listdir('data/')
output_names = [ticker+"_prediction.csv" for ticker in get_tickers()]

storage_client = storage.Client()
bucket = storage_client.bucket(gcs_bucket)

for index,outputname in enumerate(output_names):
    # outputname = output_names[index]
    blob = bucket.blob(f"predictions/{outputname}")
    try:
        data = blob.download_as_text()
        print(data)
        with open(f'predictions/{outputname}','w') as file:
            file.write(data)
    except:
        pass