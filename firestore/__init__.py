from firestore.firestore_client import FirebaseClient

firebase_client = FirebaseClient()


def collection(collection_name):
    firebase_client.use_collection(collection_name)
