from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "OK"}

@app.get("/region-and-az")
async def get_region_and_az():
    try:
        # Fetch availability zone from EC2 metadata
        az_response = requests.get("http://169.254.169.254/latest/meta-data/placement/availability-zone")
        az_response.raise_for_status()  # Raise an exception for any error
        availability_zone = az_response.text

        # Extract region from the availability zone (e.g., "us-west-2a" becomes "us-west-2")
        region = availability_zone[:-1]

        return {
            "region": region,
            "availability_zone": availability_zone
        }
    except requests.exceptions.RequestException as e:
        # Handle HTTP or connection errors
        raise HTTPException(status_code=500, detail=f"Error fetching metadata: {str(e)}")
