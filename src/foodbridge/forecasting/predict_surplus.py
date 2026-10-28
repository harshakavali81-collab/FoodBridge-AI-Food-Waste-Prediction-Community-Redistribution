"""Loads a trusted trained model; predictions never create real stock."""
import argparse,json
import joblib,pandas as pd
from foodbridge.processing.features import FEATURES
def predict(model_path,partner,category,weekday,month,lag_1,lag_7,rolling_7):
    model=joblib.load(model_path)
    row=pd.DataFrame([dict(partner=partner,category=category,weekday=weekday,month=month,lag_1=lag_1,lag_7=lag_7,rolling_7=rolling_7)])[FEATURES]
    return {"estimated_surplus_kg":round(max(0,float(model.predict(row)[0])),2),"warning":"Estimate only; never confirmed inventory."}
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--model",default="models/surplus_model.joblib");p.add_argument("--partner",required=True);p.add_argument("--category",required=True)
    for v in ("lag-1","lag-7","rolling-7"):p.add_argument("--"+v,type=float,required=True)
    p.add_argument("--weekday",type=int,required=True);p.add_argument("--month",type=int,required=True);a=p.parse_args()
    print(json.dumps(predict(a.model,a.partner,a.category,a.weekday,a.month,a.lag_1,a.lag_7,a.rolling_7),indent=2))
