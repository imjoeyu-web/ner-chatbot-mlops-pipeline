import bentoml
import pandas as pd
from bentoml.io import JSON, NumpyNdarray
from pydantic import BaseModel

runner = bentoml.sklearn.get("fraud_detection:latest").to_runner()
svc = bentoml.Service("fraud_detection_service", runners=[runner])

class Features(BaseModel):
    step: int
    amount: float
    nameOrig: int
    nameDest: int
    isFlaggedFraud: int
    balanceOrg: float
    balanceDest: float
    type_CASH_IN: bool
    type_CASH_OUT: bool
    type_DEBIT: bool
    type_PAYMENT: bool
    type_TRANSFER: bool

@svc.api(input=JSON(pydantic_model=Features), output=NumpyNdarray())
async def predict(input_data: Features):
    input_df = pd.DataFrame([input_data.dict()])
    return await runner.predict.async_run(input_df)
