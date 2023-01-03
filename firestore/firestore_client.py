import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from django.conf import settings


class FirebaseClient:

    def __init__(self):
        try:
            firebase_admin.get_app()
        except ValueError:
            firebase_admin.initialize_app(
                credentials.Certificate(settings.FIREBASE_ADMIN_CERT)
            )

        self._db = firestore.client()
        self._collections = {
            collection_name: self._db.collection(collection_name)
            for collection_name in settings.DB_COLLECTIONS}
        self._collection = self._collections[settings.DEFAULT_COLLECTION]

    def use_collection(self, collection_name):
        self._collection = self._collections[collection_name]

    def create(self, data):
        doc_ref = self._collection.document()
        doc_ref.set(data)

    def update(self, doc_id, data):
        doc_ref = self._collection.document(doc_id)
        doc_ref.update(data)

    def delete_by_id(self, doc_id):
        self._collection.document(doc_id).delete()

    def get_by_id(self, doc_id):
        doc_ref = self._collection.document(doc_id)
        doc = doc_ref.get()

        if doc.exists:
            return {**doc.to_dict(), "doc_id": doc.doc_id}
        return

    def all(self):
        docs = self._collection.stream()
        return [{**doc.to_dict(), "doc_id": doc.doc_id} for doc in docs]

    def filter(self, field, condition, value):
        docs = self._collection.where(field, condition, value).stream()
        return [{**doc.to_dict(), "doc_id": doc.doc_id} for doc in docs]
