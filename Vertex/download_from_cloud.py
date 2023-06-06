from directory_parameters import *
from google.cloud import storage
from get_tickers import get_tickers

# fetch list of prediction output csv file names
output_names = [ticker+"_prediction.csv" for ticker in get_tickers()]

storage_client = storage.Client()
bucket = storage_client.bucket(gcs_bucket)

for outputname in output_names:
    # download cloud predictions to local
    blob = bucket.blob(f"predictions/{outputname}")
    try:
        data = blob.download_as_text()
        print(data)
        with open(f'predictions/{outputname}','w') as file:
            file.write(data)
    except:
        pass