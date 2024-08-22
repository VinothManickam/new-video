from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
CORS(app)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017')
db = client['video_annotations']
annotations_collection = db['annotations']

# Save a new annotation
@app.route('/api/annotations', methods=['POST'])
def save_annotation():
    data = request.json
    # Insert the data into the collection
    inserted_id = annotations_collection.insert_one(data).inserted_id
    data['_id'] = str(inserted_id)  # Convert ObjectId to string
    return jsonify(data), 201

# Fetch annotations for a specific video using a query parameter
@app.route('/api/annotations', methods=['GET'])
def get_annotations():
    video_url = request.args.get('video_url')
    annotations = list(annotations_collection.find({"videoUrl": video_url}))
    for annotation in annotations:
        annotation['_id'] = str(annotation['_id'])  # Convert ObjectId to string
    return jsonify(annotations)

if __name__ == '__main__':
    app.run(debug=True)
