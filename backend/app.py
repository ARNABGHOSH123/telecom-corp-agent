from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.request_models import ErrorQuery
from services.multi_agent_service import handle_query
from dotenv import load_dotenv

app = FastAPI()

origins = ["http://localhost:5173"]

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
