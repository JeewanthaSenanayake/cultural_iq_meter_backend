import database.firebase as firebaseCon

def use_create(userd:str):
    auth = firebaseCon.get_auth()
    email = f"{userd}@iqmeater.com"
    password = userd
    if(len(password)<=6):
        password = password + "123456"
    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        # 1 for easy
        data={
            "name":userd,
            "uid":user.uid,
            "leval":1,
            "score":0
        }

        db = firebaseCon.get_firestore_client()
        doc_ref = db.collection('user').document(user.uid)
        doc_ref.set({"data":data})

        return data
    except:
        print("User already exist")
        user = auth.get_user_by_email(email)
        db = firebaseCon.get_firestore_client()
        doc_ref = db.collection('user').document(user.uid)
        print('Successfully signed in user:', user.uid)
        return doc_ref.get().to_dict()["data"]

def update_soce(uid:str,score:int):
    db = firebaseCon.get_firestore_client()
    doc_ref = db.collection('user').document(uid)
    data = doc_ref.get().to_dict()["data"]
    data["score"] = data["score"] + score
    doc_ref.set({"user":data})
    return data
    