from kfp.dsl import pipeline
from kfp.v2 import compiler
from kfp.v2.dsl import component
from kfp.v2.google.client import AIPlatformClient
from Vertex.directory_parameters import *
from Vertex.write_data import *
from time import sleep
import yfinance as yf
import numpy as np
from datetime import datetime
import pandas as pd
from Forecasting.preprocessing import make_lags
from google.cloud import aiplatform
from Vertex.predict_custom import *

class VertexContainer:
    def __init__(self):
        self.project = project_id
        self.location = region
        aiplatform.init(project=self.project,
                location=self.location)

    def predict(self, X):
        endpoint = aiplatform.Endpoint(f"projects/{project_num}/locations/us-central1/endpoints/{endpoint_id}")
        instances = [X]
        predict_custom_trained_model_sample(
            project="741599104884",
            endpoint_id="132886975333007360",
            location="us-central1",
            instances=instances
        )

    def predict_future(self, y, f):
        y_future = pd.concat([y, pd.Series({y.index.shift(j)[-1]: 0 for j in range(1, f + 1)})])
        for i in range(1, f + 1):
            X_future = make_lags(y_future, 24).dropna().iloc[-f + i - 1]
            y_future[y.index.shift(i)[-1]] = self.predict(pd.DataFrame(X_future).T)[0][0]

        return y_future.iloc[-f:]