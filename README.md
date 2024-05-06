**README: Embedding API**
=====================================================

**Overview**
-----------------

The `embedding` API is a Flask-based endpoint that encodes a text string and returns its embedding along with the user's ID. The API requires authentication using JSON Web Tokens (JWT) to ensure secure access.

***Key points***
---------------

* **Authentication**: To use the `embedding` API, you must provide a valid JWT token in your request header.
* **JSON Payload**: Your request body should contain a JSON object with an `text` key with the string you want to embeddings for.
* **Model**: The Hugging Face sentence transformer all-MiniLM-L6-v2 modoel is used for encoding images. 
* **Reference**: https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2

***Using the API***
-----------------

### Step 1: Authentication
Obtain a valid JWT token by authenticating with your application's authentication mechanism (e.g., username/password or social media login).

### Step 2: JSON Payload
Prepare a JSON object containing the `text` key and string you want embeddings for.

### Step 3: Send Request
Send a POST request to `/get_embeddings` with the JSON payload in the request body.

### Step 4: Verify Response
The API will return a JSON response containing:
	* `user_id`: Your user ID, obtained from the JWT token.
	* `embeddings`: The text embeddings.
	* `message`: A success message indicating that the encoding was successful.

***Error Handling***
-----------------

If any of the following errors occur:

* **Model not initialized**: The model is not ready for encoding. Wait for the model initialization timeout to expire, and try again.
* **No JSON data received**: Your request body does not contain valid JSON data.
* **Invalid text**: The provided `text` is invalid or cannot be accessed.

The API will return an error response with a relevant message and HTTP status code (400 or 500).
