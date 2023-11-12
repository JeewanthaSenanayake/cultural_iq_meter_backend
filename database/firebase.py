import firebase_admin
from firebase_admin import credentials, storage
from firebase_admin import firestore


path = 'database/cultural-iq-meter-firebase-adminsdk-z5bfu-f269a9a80c.json'
cred = credentials.Certificate(path)
firebase_admin.initialize_app(cred,{
    'storageBucket':'cultural-iq-meter.appspot.com'
})

# Create a reference to the Firebase Storage bucket
def get_firestore_img_upload():
    return storage.bucket()

def get_firestore_client():
    return firestore.client()


