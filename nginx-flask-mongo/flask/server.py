#!/usr/bin/env python
import os

from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

client_host = os.environ.get("MONGO_SERVER_URL", "mongodb-nginx-flask-mongo-mongo.internal")
print(f"Connecting to MongoDB at {client_host}")

try:
    client = MongoClient(host=client_host,
                         directConnection=True,
                         serverSelectionTimeoutMS=2000,
                         appname="unikraft")
except Exception as e:
    print(f"Error creating MongoDB client: {e}")


@app.route('/')
def todo():
    try:
        client.admin.command('ismaster')
        return "Hello from the MongoDB client!\n"
    except Exception as e:
        print(f"MongoDB connection error: {e}")
        return "MongoDB server not available, but Flask is running!\n"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("FLASK_SERVER_PORT", 9090)), debug=False)
