from typing import TypeDict, List, Dict, Any
class GraphState(TypeDict):
    city : str
    profession : str
    concern: str
    
    city_baseline : Dict[str, Any]
    profession_baseline : Dict[str, Any]
    historical_weather: List[Dict[str, Any]]
    forecast_weather: List[Dict[str, Any]]
    
    risk_assemssment : Dict[str, Any]
    
    overall_severity : str
    generalized_reocommendations : List[str]
    personalized_recommendations : List[str]
    
    safe_cities : List[Dict[str,Any]]