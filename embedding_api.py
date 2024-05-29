from fastapi import FastAPI, HTTPException, Depends, Request, status
from fastapi.responses import JSONResponse
from jose import jwt
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

import os
from dotenv import load_dotenv
from threading import Thread, Event
from typing import Dict

from huggingface_hub import snapshot_download

# Configure logging
from loguru import logger

# Remove system defaults
logger.remove()

# Configure file handler
logger.add('embedding_api.log', format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}", level='INFO', serialize=True, rotation='1 day', retention='10 days' )


load_dotenv()

# app = FastAPI(docs_url=None, redoc_url=None)
app = FastAPI()
#app = FastAPI(debug=True)

class Settings(BaseModel):
    authjwt_secret_key: str = os.environ.get('JWT_SECRET_KEY')  # Change this to a secure secret key

# NOTE: use debugger in https://jwt.io to test token authentication issues
def get_jwt_token(request: Request) -> str:
    """Function to extract JWT token from request headers"""
    auth_header = request.headers.get("Authorization")
    if not auth_header or "Bearer " not in auth_header:
        logger.error(f"Unable to authenticate {request.headers}") 
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = auth_header.split("Bearer ")[1]
    return token

def verify_jwt_token(token: str, secret_key: str) -> dict:
    """Function to verify and decode JWT token"""
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload
    except jwt.JWTError as e:
        logger.error(f"JWT verification failed: {e}") 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid token: {e}")

    


# Global variables for the AI model
model = None
model_initialized = Event()


# Instantiate the AI model which takes time to load in a separate thread
def instantiate_model():
    global model
    try:
        model_path = snapshot_download(repo_id='sentence-transformers/all-MiniLM-L6-v2')

        # Initialize SentenceTransformer model
        model = SentenceTransformer(model_path)
        return model        
    except Exception as e:
#        print(f"Error initializing model: {e}")
        logger.error(f"Error initializing model: {e}")
    finally:
        model_initialized.set()

# Start the thread to instantiate the model
model_thread = Thread(target=instantiate_model)
model_thread.start()

class TextData(BaseModel):
    text: str

@app.get("/healthcheck")
async def healthcheck() -> JSONResponse:
    """
    Performs a health check to verify system readiness.

    This endpoint checks if the underlying model has been successfully initialized.

    **Response:**

    - 200: OK - The system is healthy and operational.
    - 503: Service Unavailable - The system is unhealthy (model not initialized).

    **Body:**

    ```json
    {
        "status": str  # "healthy" or "unhealthy" depending on system state
    }
    ```
    """
    if not model_initialized.is_set():
        logger.warning("System unhealthy")
        return JSONResponse({"status": "unhealthy"}, status_code=503)
    logger.info("System healthy")
    return JSONResponse({"status": "healthy"})



@logger.catch()
@app.post("/get_embeddings")
async def process_data(request: Request) -> dict:
    """
    This endpoint processes text data and generates embeddings.

    **Authorization:** Bearer JWT token is required.

    **Request Body:**

    ```json
    {
        "text": "This is the text you want to generate embeddings for."
    }
    ```

    **Response:**

    ```json
    {
        "user_id": str,  # User ID extracted from the JWT token
        "embeddings": list,  # List of generated embeddings
        "message": str  # Message indicating successful processing
    }
    ```

    **Errors:**

    - 400: Bad Request - No text data provided in the request body.
    - 500: Internal Server Error - Model initialization failed.
    """
    # logger.debug (request.headers)
    token = get_jwt_token(request)
    payload = verify_jwt_token(token, Settings().authjwt_secret_key)

    if not model_initialized.wait(timeout=10):  # Wait for model initialization with timeout
        logger.error("Model not initialized")
        raise HTTPException(status_code=500, detail="Model initialization timeout")
    
    try:
        # Get the user_id from the JWT
        user_id = payload.get("sub")
        
        # Parse JSON data from the request
        data = await request.json()
        text = data.get('text')
        
        if not text:
            logger.error("No text data received")
            raise HTTPException(status_code=400, detail="No text data received")

        embeddings = model.encode(text)

        logger.info(f"Embeddings successful for user {user_id}:{text}")
        
        # Return the user_id and caption in the response
        return {"user_id": user_id, "embeddings": embeddings.tolist(), "message": "Text embeddings"}

    except (ConnectionError, BrokenPipeError) as e:
        logger.error(f"ConnectionError/BrokenPipeError: {e}")
        raise HTTPException(status_code=500, detail=f"ConnectionError/BrokenPipeError: Unable to send response: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5681)
