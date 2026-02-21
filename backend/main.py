from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Import your working LangGraph AI brain
from graph.workflow import app as langgraph_app

# 1. This is like your Django project setup
app = FastAPI()

# 2. This is like django-cors-headers. It allows your React frontend to talk to this backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RiskRequest(BaseModel):
    city: str
    profession: str
    concern: str
    
@app.post("/api/analyze-risk")
async def analyze_risk(request: RiskRequest):
    print(f"📥 Received request from React: {request.city}, {request.concern}")
    
    initial_state = {
        "city": request.city,
        "profession": request.profession,
        "concern": request.concern,
        "city_baseline": {},
        "live_weather": {},
        "historical_weather": [],
        "forecast_weather": [],
        "risk_assessments": {},
        "overall_severity": "Low",
        "general_recommendations": [],
        "personalized_recommendations": [],
        "safe_cities": []
    }
    
    final_state = langgraph_app.invoke(initial_state)
    
    # Return the data to React (FastAPI handles the JSON conversion automatically, just like JsonResponse in Django)
    return final_state

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)