"""Deterministic synthetic daily operations for development. No real charity data."""
import csv,math,random
from datetime import date,timedelta
from pathlib import Path
def main(output="data/synthetic/daily_operations.csv"):
    rng=random.Random(42);start=date(2026,10,27)-timedelta(days=209)
    partners=[("Green Bowl Cafe (Demo)","produce",70),("City Bakery (Demo)","bakery",60),("Harvest Market (Demo)","grains",115),("FreshFork Kitchen (Demo)","prepared",95)]
    rows=[]
    for i in range(210):
        dt=start+timedelta(days=i)
        for p,(partner,category,base) in enumerate(partners):
            weekend=dt.weekday()>=5
            prepared=round(max(10,base+(12 if weekend else 0)+math.sin(i/17+p)*7+rng.gauss(0,7)),1)
            sold=round(prepared*min(.94,max(.53,(.77 if weekend else .68)+rng.gauss(0,.045))),1)
            surplus=round(prepared-sold,1)
            donated=round(surplus*min(.9,max(.12,.56+rng.gauss(0,.13))),1)
            rows.append(dict(date=dt.isoformat(),partner=partner,category=category,prepared_kg=prepared,sold_kg=sold,surplus_kg=surplus,donated_kg=donated))
    out=Path(output);out.parent.mkdir(parents=True,exist_ok=True)
    with out.open("w",newline="") as f:
        wr=csv.DictWriter(f,fieldnames=list(rows[0]));wr.writeheader();wr.writerows(rows)
    print(f"Generated {len(rows)} synthetic records: {out}")
if __name__=="__main__":main()
