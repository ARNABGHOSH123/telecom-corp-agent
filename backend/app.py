from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.request_models import ErrorQuery
from services.multi_agent_service import handle_query
from dotenv import load_dotenv
from ingest_marketing_data_to_db import seed_db
import uvicorn
import os

app = FastAPI()

origins = ["https://telecom-corp-agent-arnab.netlify.app"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()


@app.post("/query")
def process_query(request: ErrorQuery):
    """API endpoint to handle user queries."""
    result = handle_query(request.query)
    return {"response": result}

if __name__== '__main__':
    port = int(os.getenv("PORT", 8000))
    seed_db()
    uvicorn.run(app,host="0.0.0.0", port=port)
