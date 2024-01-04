import database.firebase as firebaseCon

def get_all_rankings():
    db = firebaseCon.get_firestore_client()
    doc_ref = db.collection('user').stream()
    data = []
    for doc in doc_ref:
        data.append({
            "name":doc.to_dict()["data"]["name"],
            "score":doc.to_dict()["data"]["score"],
            "lastPlayed":doc.to_dict()["data"]["leval"],
        })

    data.sort(key=lambda x: x["score"], reverse=True)
    for i in range(len(data)):
        data[i]["rank"] = i+1
    return data