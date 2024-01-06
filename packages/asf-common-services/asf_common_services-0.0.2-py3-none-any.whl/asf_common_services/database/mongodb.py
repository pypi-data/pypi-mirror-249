from pymongo import MongoClient, ReplaceOne

from asf_common_services.service_config import MONGODB_CONFIG


class MongoDBService:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.client = MongoClient(**MONGODB_CONFIG)
        return cls._instance

    def get_collection(self, collection_name, db_name):
        return self.client.get_database(db_name)[collection_name]

    def insert_document(self, collection_name, document_data, db_name):
        collection = self.get_collection(collection_name, db_name)
        result = collection.insert_one(document_data)
        return result.inserted_id

    def get_document(self, collection_name, query, db_name):
        collection = self.get_collection(collection_name, db_name)
        return collection.find_one(query)

    def update_document(self, collection_name, query, update_data, db_name):
        collection = self.get_collection(collection_name, db_name)
        result = collection.update_many(query, {'$set': update_data})
        return result.modified_count

    def replace_document(self, collection_name, query, replacement_data, db_name):
        collection = self.get_collection(collection_name, db_name)
        result = collection.replace_one(query, replacement_data)
        return result.modified_count

    def bulk_insert_documents(self, collection_name, documents, db_name):
        collection = self.get_collection(collection_name, db_name)
        result = collection.insert_many(documents)
        return result.inserted_ids

    def bulk_update_documents(self, collection_name, bulk_operations, db_name):
        collection = self.get_collection(collection_name, db_name)
        operations = [ReplaceOne(filter=op['filter'], replacement=op['update']) for op in bulk_operations]
        result = collection.bulk_write(operations)
        return result.modified_count

    def bulk_delete_documents(self, collection_name, query, db_name):
        collection = self.get_collection(collection_name, db_name)
        result = collection.delete_many(query)
        return result.deleted_count
