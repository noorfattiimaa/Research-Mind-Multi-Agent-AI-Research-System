from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from pipeline.research_pipeline import run_research_pipeline


app = FastAPI(
    title="ResearchMind API",
    description="Multi-Agent AI Research System",
    version="1.0.0"
)


class ResearchRequest(BaseModel):
    topic: str


@app.get("/")
def root():
    return {
        "message": "ResearchMind API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/research")
def research(request: ResearchRequest):

    if not request.topic.strip():
        raise HTTPException(
            status_code=400,
            detail="Research topic cannot be empty"
        )

    try:
        result = run_research_pipeline(request.topic)

        return {
            "status": "completed",
            "topic": request.topic,
            "result": result
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )