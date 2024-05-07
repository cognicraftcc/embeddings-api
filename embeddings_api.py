from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
# import time

from sentence_transformers import SentenceTransformer

import requests

from threading import Thread, Event

from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')  # Change this to a secure secret key
jwt = JWTManager(app)

# Global variables for the AI model
image_model = None
model_initialized = Event()

# Instantiate the AI model which takes time to load in a separate thread
def instantiate_model():
    global model
    try:
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    except Exception as e:
        print(f"Error initializing model: {e}")
    finally:
        model_initialized.set()



# Start the thread to instantiate the model
model_thread = Thread(target=instantiate_model)
model_thread.start()


@app.route("/healthcheck")
def healthcheck():
    if not model_initialized.wait(timeout=10):
        return jsonify({"status": "unhealthy", "error": "AI model not initialised!"}), 503
    else:    
        # Return a JSON response indicating healthy status
        return jsonify({"status": "healthy"})
    

@app.route('/get_embeddings', methods=['POST'])
@jwt_required()
def process_data():
    if not model_initialized.wait(timeout=10):  # Wait for model initialization with timeout
        print("Model not initialised")
        return jsonify(error="Model initialization timeout"), 500
    try:
        # Get the user_id from the JWT
        user_id = get_jwt_identity()
        
        # Parse JSON data from the request
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data received'}), 400
        
        # Extract the caption from the JSON data
        text = data.get('text')

        if text:

            embeddings = model.encode(text)
            # embeddings_array = embeddings.numpy()  # Convert to NumPy array

            print(f"Embeddings sucessful for {text}")

        # Return the user_id and caption in the response
        try:
            return jsonify({'user_id': user_id, 'embeddings': embeddings.tolist(), 'message': 'Text embeddings'})
        except (ConnectionError, BrokenPipeError) as e:
            print(f"ConnectionError/BrokenPipeError: {e}")
            return jsonify({'error': 'ConnectionError/BrokenPipeError: Unable to send response', 'details': str(e)}), 500
        except Exception as e:
            print(f"Unexpected error: {e}")
            return jsonify({'error': 'Unexpected error', 'details': str(e)}), 500
    except Exception as e:
        # Handle other exceptions
        print(e)
        return jsonify({'error': str(e)}), 500
        

if __name__ == '__main__':
    app.run(debug=True, port=5681)