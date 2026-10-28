from foodbridge.ingestion.partner_csv_loader import load_partner_csv
def clean_operations(path):
    df=load_partner_csv(path)
    df["weekday"]=df["date"].dt.dayofweek
    return df
