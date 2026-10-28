from .eligibility import eligibility
def ranked_matches(item,recipients,max_distance_km=20):
    matches=[]
    for r in recipients:
        result=eligibility(item,r,max_distance_km=max_distance_km)
        if result["eligible"]:
            matches.append({"recipient_id":r.id,"recipient_name":r.name,**result})
    return sorted(matches,key=lambda x:(x["distance_km"],-x["max_quantity_kg"]))
