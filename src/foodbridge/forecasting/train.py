"""Offline evaluation: chronological holdout versus seasonal-naive lag-7."""
import argparse,json
from pathlib import Path
from datetime import datetime,timezone
import joblib
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from foodbridge.ingestion.partner_csv_loader import load_partner_csv
from foodbridge.processing.features import make_features,CATEGORICAL,NUMERICAL,FEATURES
from foodbridge.forecasting.evaluate import metrics
def train(csv_path,output_dir="models"):
    df=make_features(load_partner_csv(csv_path))
    dates=sorted(df.date.unique())
    if len(dates)<30:raise ValueError("Need at least 30 usable dates")
    cutoff=dates[int(len(dates)*.8)]
    training=df[df.date<cutoff];testing=df[df.date>=cutoff]
    if training.empty or testing.empty:raise ValueError("Insufficient holdout")
    preprocess=ColumnTransformer([("categorical",OneHotEncoder(handle_unknown="ignore"),CATEGORICAL),("numeric","passthrough",NUMERICAL)])
    model=Pipeline([("preprocess",preprocess),("estimator",RandomForestRegressor(n_estimators=120,min_samples_leaf=3,random_state=42,n_jobs=-1))])
    model.fit(training[FEATURES],training["surplus_kg"])
    predictions=model.predict(testing[FEATURES])
    report={"data_label":"synthetic" if "synthetic" in str(csv_path) else "partner_supplied","train_rows":len(training),"test_rows":len(testing),"train_last_date":str(training.date.max().date()),"test_first_date":str(testing.date.min().date()),"model":metrics(testing.surplus_kg,predictions),"baseline_lag7":metrics(testing.surplus_kg,testing.lag_7),"limitation":"One-step historical evaluation with previous actuals; NOT a recursive forecast or production accuracy proof.","generated_utc":datetime.now(timezone.utc).isoformat()}
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=True)
    joblib.dump(model,out/"surplus_model.joblib");(out/"evaluation.json").write_text(json.dumps(report,indent=2))
    return report
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--data",default="data/synthetic/daily_operations.csv");p.add_argument("--output",default="models");a=p.parse_args()
    print(json.dumps(train(a.data,a.output),indent=2))
