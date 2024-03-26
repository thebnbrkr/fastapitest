# Import FastAPI
from fastapi import FastAPI

# Create an instance of the FastAPI class
app = FastAPI()

# Define a route at the root "/"
@app.get("/")
async def read_root():
    return {"Hello": "World"}

# Additional routes can be added below similarly
