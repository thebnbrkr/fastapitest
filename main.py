
"""
# Import FastAPI
from fastapi import FastAPI

# Create an instance of the FastAPI class
app = FastAPI()

# Define a route at the root "/"
@app.get("/")
async def read_root():
    return {"Hello": "World"}

# Additional routes can be added below similarly
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Import necessary modules
from langchain.embeddings import HuggingFaceBgeEmbeddings
import qdrant_client
from qdrant_client import QdrantClient
from langchain_community.vectorstores import Qdrant

# Initialize FastAPI app
app = FastAPI()

# Define your settings and initializations
HF_TOKEN = "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"  # Use your actual HF_TOKEN

model_name = "BAAI/bge-base-en"
encode_kwargs = {'normalize_embeddings': True}  # set True to compute cosine similarity

# Initialize the HuggingFace Bge Embeddings
model_norm = HuggingFaceBgeEmbeddings(
    model_name=model_name,
    model_kwargs={'device': 'cpu'},
    encode_kwargs=encode_kwargs
)

# Initialize the Qdrant client
client = QdrantClient(
    "https://172bf761-4b1c-4b06-a99f-cec74ea238fc.us-east4-0.gcp.cloud.qdrant.io",  # Use your actual Qdrant endpoint
    api_key="QJ7Mnibhy2rPAHPDJMHsx5VjgFBXIn264TxT_e4t7zJwnWHj3rJv3A",  # Use your actual Qdrant API key
)
collection_name = "Finance_Test"

# Initialize the Qdrant object
qdrant = Qdrant(client, collection_name, model_norm)

# Define a Pydantic model for the request body
class QueryModel(BaseModel):
    query: str

# Define an endpoint for similarity search
@app.post("/similarity_search/")
async def similarity_search_endpoint(query_model: QueryModel):
    try:
        # Perform the similarity search
        found_docs = qdrant.similarity_search(query_model.query)
        
        # Return the page content of the first document found
        # You might want to modify this to return a different format
        return {"page_content": found_docs[0].page_content}
    except Exception as e:
        # If something goes wrong, return an HTTP error
        raise HTTPException(status_code=500, detail=str(e))

# Run this with 'uvicorn script_name:app --reload'
