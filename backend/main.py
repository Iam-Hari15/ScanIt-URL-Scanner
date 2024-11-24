from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

# Initialize FastAPI app
app = FastAPI()

# Enable CORS to allow requests from any origin for testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing purposes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the request body model
class URLRequest(BaseModel):
    url: str

# Define the /scan endpoint to handle scanning a URL
@app.post("/scan")
async def scan_url(request: URLRequest):
    try:
        # Attempt to send a GET request to the provided URL
        response = requests.get(request.url)

        # Check if the URL request is successful
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve the URL: {response.status_code}")

        # Return the response details
        return {
    "message": "URL Scanned",
    "url": request.url,
    "status_code": response.status_code,
    "content_length": len(response.content),
    "headers": dict(response.headers),
}

    except requests.exceptions.RequestException as e:
        # Handle errors during the request (e.g., invalid URL)
        raise HTTPException(status_code=500, detail=f"Error scanning URL: {str(e)}")
    except Exception as e:
        # Handle any unexpected errors
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
