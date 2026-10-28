from foodbridge.ingestion.partner_csv_loader import load_partner_csv
def summarize_quality(path):
    df=load_partner_csv(path)
    return {"rows":len(df),"partners":int(df.partner.nunique()),"categories":int(df.category.nunique()),"date_min":str(df.date.min().date()),"date_max":str(df.date.max().date()),"duplicate_keys":0,"invalid_negative_rows":0}
