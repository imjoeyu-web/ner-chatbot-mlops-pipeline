import pandas as pd
import psycopg2
from sqlalchemy import create_engine

df = pd.read_csv("./Fraud.csv")
engine = create_engine("postgresql+psycopg2://mlops:mlops@localhost:5432/mlops")
df.to_sql('sample_data', engine, if_exists='replace', index=False)