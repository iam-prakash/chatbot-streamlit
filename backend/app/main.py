from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.qa import answer_question

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(BaseModel):
    question: str

@app.post("/ask")
def ask_question(q: Question):
    """Answer a question about Sixt rental terms using Gemini AI"""
    try:
        result = answer_question(q.question)
        return {
            "success": True,
            "question": result["question"],
            "answer": result["answer"],
            "sources_count": len(result["sources"])
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to process your question. Please try again."
        }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Sixt Q&A API"}
