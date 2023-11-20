import database.firebase as firebaseCon
import re

def use_create(userd:str):
    auth = firebaseCon.get_auth()
    # u_name = userd.lower().replace(" ", "")
    u_name = re.sub(r'[^a-zA-Z0-9]', '', userd.lower())
    email = f"{u_name}@iqmeater.com"
    password = u_name
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
        # user = auth.get_user_by_email(email)
        # db = firebaseCon.get_firestore_client()
        # doc_ref = db.collection('user').document(user.uid)
        # print('Successfully signed in user:', user.uid)
        return False

def update_soce(uid:str,score:float,leval:int):
    db = firebaseCon.get_firestore_client()
    doc_ref = db.collection('user').document(uid)
    data = doc_ref.get().to_dict()["data"]
    data["score"] = data["score"] + score
    data["leval"] = leval
    doc_ref.set({"user":data})
    return data
    