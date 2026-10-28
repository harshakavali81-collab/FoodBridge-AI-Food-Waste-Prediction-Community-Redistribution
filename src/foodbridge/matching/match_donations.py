from .eligibility import eligibility

def ranked_matches(item,recipients,max_distance_km=20,recipient_holds=None):
    recipient_holds=recipient_holds or {}
    matches=[]
    for r in recipients:
        result=eligibility(item,r,max_distance_km=max_distance_km,
                           recipient_held_kg=recipient_holds.get(r.id,0))
        if result["eligible"]:
            matches.append({"recipient_id":r.id,"recipient_name":r.name,**result})
    return sorted(matches,key=lambda x:(x["distance_km"],-x["max_quantity_kg"]))
