**README: Embeddings API**
=====================================================

**Overview**
-----------------

The `embeddings` API is a Flask-based endpoint that encodes a text string and returns its embeddings along with the user's ID. The API requires authentication using JSON Web Tokens (JWT) to ensure secure access.

***Key points***
---------------

* **Authentication**: To use the `embeddings` API, you must provide a valid JWT token in your request header.
* **JSON Payload**: Your request body should contain a JSON object with an `text` key with the string you want to embeddings for.
* **Model**: The Hugging Face sentence transformer all-MiniLM-L6-v2 model is used to perform the embeddings of vector size 384. 
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


***Running in a Docker container***
-----------------


1. Rename file "env-template" to ".env" and add the key(s) listed.

2. Before you begin, ensure you have  Docker and Docker Compose installed and running, and have downloaded the entire project directory including the docker-compose.yml file. You can use the following git command to clone the project.

     ```
     git clone https://github.com/cognicraftcc/embeddings-api
     ```

3. Build the project from the project directory by running
     ```
     docker-compose up -d
     ```

3. If database is not set up or need to be upgrade following the instructions for database migrations below.

4. To use the api point your app with the above parameters to the following url to access the api. Replace 'localhost' with the hostname or ip address if the app is remote.
     ```
     http://localhost:5681/get_embeddings
     ```

5. For development and debugging purposes, you can run a separate docker-compose-dev.yml file as follows instead:

     ```
     docker-compose -f docker-compose-dev.yml up
     ```

6. To stop and remove all running containers and services, use the following command:

     ```
     docker-compose down
     ```

***Pytest***
-----------------

To run the included test using Pytest, you'll need to install the following additional libraries not included in requirements.txt. This is intentional to reduce the size of the deployment docker image.

    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
    pip install --no-deps sentence-transformers
    pip install pytest pytest-mock pytest-asyncio

