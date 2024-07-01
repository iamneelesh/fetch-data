from flask import Flask, request, jsonify
from pymongo import MongoClient
import json
import chromadb
import logging

app = Flask(__name__)


logging.basicConfig(level=logging.DEBUG) #debugging and error handling k liye use kiya h


mongo_client = MongoClient("mongodb://localhost:27017/")


chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(name="bitcoin_collection")

@app.route('/btc', methods=['POST'])
def view_documents():
    try:
        data = request.get_json()
        db_name = data.get("db_name")
        collection_name = data.get("collection_name")

        if not db_name or not collection_name:
            return jsonify({"error": "db_name and collection_name are required"}), 400

        mongo_db = mongo_client[db_name]
        mongo_collection = mongo_db[collection_name]

        documents = list(mongo_collection.find({}, {"_id": 0}))
        return jsonify(documents)
    except Exception as e:
        logging.error(f"Error fetching documents: {e}")
        return jsonify({"error": "Error fetching documents"}), 500

@app.route('/btc/fetch', methods=['POST'])
def fetch_and_store():
    try:
        data = request.get_json()
        db_name = data.get("db_name")
        collection_name = data.get("collection_name")

        if not db_name or not collection_name:
            return jsonify({"error": "db_name and collection_name are required"}), 400

        mongo_db = mongo_client[db_name]
        mongo_collection = mongo_db[collection_name]

        documents = list(mongo_collection.find({}, {"_id": 0}))
        logging.debug(f"Fetched documents: {documents}")

        with open('mongo_data.json', 'w') as file:
            json.dump(documents, file, indent=4)

       
        valid_documents = [doc for doc in documents if 'content' in doc]
        missing_content_docs = [doc for doc in documents if 'content' not in doc]

        if missing_content_docs:
            logging.warning(f"Documents missing 'content' field: {missing_content_docs}")

        
        if valid_documents:
            docs = [doc['content'] for doc in valid_documents]
            ids = [str(i) for i in range(len(valid_documents))]
            collection.upsert(documents=docs, ids=ids)

        return jsonify({"message": "Data fetched, stored in mongo_data.json, and upserted into ChromaDB"}), 200
    except Exception as e:
        logging.error(f"Error in fetch_and_store: {e}")
        return jsonify({"error": "Error in fetch_and_store"}), 500

if __name__ == '__main__':
    app.run(debug=True)

