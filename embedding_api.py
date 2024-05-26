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

import logging
# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)  # Get logger for the current module


load_dotenv()

app = FastAPI()
#app = FastAPI(debug=True)

class Settings(BaseModel):
    authjwt_secret_key: str = os.environ.get('JWT_SECRET_KEY')  # Change this to a secure secret key



def get_jwt_token(request: Request) -> str:
    """Function to extract JWT token from request headers"""
    auth_header = request.headers.get("Authorization")
    if not auth_header or "Bearer " not in auth_header:
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = auth_header.split("Bearer ")[1]
    return token

def verify_jwt_token(token: str, secret_key: str) -> dict:
    """Function to verify and decode JWT token"""
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload
    except jwt.JWTError as e:
        #raise HTTPException(status_code=401, detail="Invalid token")
        #raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
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

    except Exception as e:
        print(f"Error initializing model: {e}")
    finally:
        model_initialized.set()

# Start the thread to instantiate the model
model_thread = Thread(target=instantiate_model)
model_thread.start()

class TextData(BaseModel):
    text: str

@app.get("/healthcheck")
async def healthcheck():
  if not model_initialized.wait(timeout=10):
    return JSONResponse({"status": "unhealthy"}, status_code=503)
  return JSONResponse({"status": "healthy"})



@app.post("/get_embeddings")
# async def process_data(request: Request, user_id: str = Depends(verify_token)):
async def process_data(request: Request):
    print (request.headers)
    token = get_jwt_token(request)
    payload = verify_jwt_token(token, Settings().authjwt_secret_key)

    if not model_initialized.wait(timeout=10):  # Wait for model initialization with timeout
        print("Model not initialized")
        raise HTTPException(status_code=500, detail="Model initialization timeout")
    
    try:
        # Get the user_id from the JWT
        # user_id = Authorize.get_jwt_subject()
        user_id = payload.get("sub")
        
        # Parse JSON data from the request
        data = await request.json()
        text = data.get('text')
        
        if not text:
            raise HTTPException(status_code=400, detail="No text data received")

        embeddings = model.encode(text)

        print(f"Embeddings successful for {text}")
        
        # Return the user_id and caption in the response
        return {"user_id": user_id, "embeddings": embeddings.tolist(), "message": "Text embeddings"}

    except (ConnectionError, BrokenPipeError) as e:
        print(f"ConnectionError/BrokenPipeError: {e}")
        raise HTTPException(status_code=500, detail=f"ConnectionError/BrokenPipeError: Unable to send response: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5681)
