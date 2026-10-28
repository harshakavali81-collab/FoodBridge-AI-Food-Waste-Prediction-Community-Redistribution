"""User-supplied FAO research exports are labeled as studies, not inventory."""
import pandas as pd
def load_fao_research(path):
    df=pd.read_csv(path)
    if df.empty:raise ValueError("Empty research export")
    df=df.copy()
    df["research_source"]="FAO Food Loss and Waste Database (user-supplied export)"
    df["is_live_operational_record"]=False
    return df
if __name__=="__main__":
    import argparse
    from pathlib import Path
    p=argparse.ArgumentParser();p.add_argument("csv");p.add_argument("--out",default="data/research/fao_research_labeled.csv");a=p.parse_args()
    result=load_fao_research(a.csv);Path(a.out).parent.mkdir(parents=True,exist_ok=True);result.to_csv(a.out,index=False)
