# Flask MongoDB and ChromaDB Integration

This Flask application allows you to fetch data from a specified MongoDB database and collection, store the data in a JSON file, and upsert valid documents into ChromaDB. The application includes endpoints to view documents and to fetch and store documents dynamically.

## Features

- **Dynamic MongoDB Access:** Specify any MongoDB database and collection via POST requests.
- **Data Storage:** Store fetched data in a JSON file.
- **ChromaDB Integration:** Upsert valid documents into ChromaDB.
- **Error Handling:** Comprehensive logging and error handling.

## Requirements

- Python 3.6+
- Flask
- PyMongo
- ChromaDB
