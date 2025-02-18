from flask import Flask, request, jsonify
from flask_cors import CORS
from config import db
import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# 🔹 Cloudinary Configuration
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

COLLECTIONS = ["publications", "projects", "datasets", "resources", "people", "alumni", "news","indication"]

@app.route('/add_item', methods=['POST'])
def add_item():
    try:
        data = request.json  # Get JSON data
        collection = data.get("collection")  # Collection name

        if not collection or collection not in COLLECTIONS:
            return jsonify({"error": "Invalid or missing collection name"}), 400

        # Add data to Firestore
        doc_ref = db.collection(collection).add(data)
        return jsonify({"message": "Item added successfully", "doc_id": doc_ref[1].id}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# {
#            "collection": "projects",
#            "title": "AI-Powered Chatbot",
#            "description": "Developing a chatbot using NLP and ML.",
#            "start_date": "2024-01-10",
#            "end_date": "2024-12-31",
#            "status": "Ongoing"
# }



@app.route('/get_items/<collection>', methods=['GET'])
def get_items(collection):
    try:
        if collection not in COLLECTIONS:
            return jsonify({"error": "Invalid collection name"}), 400

        docs = db.collection(collection).stream()
        items = [{"doc_id": doc.id, **doc.to_dict()} for doc in docs]
        return jsonify(items), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
# {
#   "title": "AI-Powered Chatbot",
#   "description": "Developing a chatbot using NLP and ML.",
#   "start_date": "2024-01-10",
#   "end_date": "2024-12-31",
#   "status": "Ongoing"
# }

@app.route('/delete_item/<collection>/<doc_id>', methods=['DELETE'])
def delete_item(collection, doc_id):
    try:
        if collection not in COLLECTIONS:
            return jsonify({"error": "Invalid collection name"}), 400

        doc_ref = db.collection(collection).document(doc_id)
        
        # Check if document exists
        if not doc_ref.get().exists:
            return jsonify({"error": "Document not found"}), 404

        doc_ref.delete()
        return jsonify({"message": f"Document {doc_id} deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/upload_image', methods=['POST'])
def upload_image():
    try:
        # Get image from request
        file = request.files['image']

        # Upload image to Cloudinary
        result = cloudinary.uploader.upload(file)

        # Get the Cloudinary URL
        image_url = result["secure_url"]

        # Store image URL in Firestore (optional)
        doc_ref = db.collection("images").add({"image_url": image_url})

        return jsonify({"image_url": image_url, "doc_id": doc_ref[1].id}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/update_lab', methods=['POST'])
def update_lab():
    try:
        # Get doc_id (Hardcoded for now)
        doc_id = "1AjL70oGnfZvxaEX7wx3"

        # Get new boolean value from request
        data = request.get_json()
        new_value = data.get("value")  # Expected: true/false

        if new_value is None:
            return jsonify({"error": "Missing 'value' parameter"}), 400

        # Get the document reference
        doc_ref = db.collection("indication").document(doc_id)
        doc = doc_ref.get()

        if not doc.exists:
            return jsonify({"error": f"Document with ID '{doc_id}' not found"}), 404

        # Get document data
        doc_data = doc.to_dict()

        # Update only boolean fields
        updated_fields = {keys: new_value for keys, value in doc_data.items() if isinstance(value, bool)}

        if not updated_fields:
            return jsonify({"message": "No boolean fields found to update"}), 200

        # Update Firestore document
        doc_ref.update(updated_fields)

        return jsonify({"message": f"Updated document {doc_id}", "updated_fields": updated_fields}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/update_gpu', methods=['POST'])
def update_gpu():
    try:
        # Get doc_id (Hardcoded for now)
        doc_id = "8jT18xrSIjJVVeGKSrR3"

        # Get new boolean value from request
        data = request.get_json()
        new_value = data.get("value")  # Expected: true/false

        if new_value is None:
            return jsonify({"error": "Missing 'value' parameter"}), 400

        # Get the document reference
        doc_ref = db.collection("indication").document(doc_id)
        doc = doc_ref.get()

        if not doc.exists:
            return jsonify({"error": f"Document with ID '{doc_id}' not found"}), 404

        # Get document data
        doc_data = doc.to_dict()

        # Update only boolean fields
        updated_fields = {gpu: new_value for gpu, value in doc_data.items() if isinstance(value, bool)}

        if not updated_fields:
            return jsonify({"message": "No boolean fields found to update"}), 200

        # Update Firestore document
        doc_ref.update(updated_fields)

        return jsonify({"message": f"Updated document {doc_id}", "updated_fields": updated_fields}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
