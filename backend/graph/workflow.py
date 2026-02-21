import sys
import os
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)


from smolagents import LiteLLMModel, ToolCallingAgent
from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END
from graph.tools import calculate_safe_distance

token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
ai_model = LiteLLMModel(
    model_id="huggingface/Qwen/Qwen2.5-Coder-32B-Instruct", 
    api_key=token
)

class GraphState(TypedDict):
    city: str
    profession: str              
    concern: str                 
    city_baseline: Dict[str, Any] 
    live_weather: Dict[str, Any]  
    historical_weather: List[Dict[str, Any]] 
    forecast_weather: List[Dict[str, Any]]   
    risk_assessments: Dict[str, str]
    overall_severity: str         
    general_recommendations: List[str]
    personalized_recommendations: List[str]
    safe_cities: List[Dict[str, Any]] 

# ==========================================
# 2. Define Dummy Node Functions
# ==========================================

def fetch_data_node(state: GraphState) -> Dict[str, Any]:
    city = state.get("city", "")
    print(f"📥 Fetching baseline data and weather for: {city}...")
    
    city_baseline = {}
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.abspath(os.path.join(current_dir, '..', '..', 'pk_cities_cleanedAccApi_data.csv'))
        
        df = pd.read_csv(csv_path)
        city_row = df[df['city'].str.lower() == city.lower()]
        
        if not city_row.empty:
            city_baseline = {
                "lat": city_row.iloc[0]['lat'],
                "lng": city_row.iloc[0]['lng'],
                "population": city_row.iloc[0]['population'],
                "province": city_row.iloc[0]['admin_name']
            }
            print(f"   [DATA] Found {city}: Lat={city_baseline['lat']}, Lng={city_baseline['lng']}, Pop={city_baseline['population']}")
        else:
            print(f"   [WARNING] City '{city}' not found in CSV.")
            
    except Exception as e:
        print(f"   [ERROR] Could not load CSV: {e}")

    # 2. Mocking the Weather API (Backend Engineer will replace this with a real API later)
    # Since we don't have the API key plugged in yet, we'll return a dynamic mock based on the concern
    concern = state.get("concern", "").lower()
    mock_temp = 42 if concern == "heatwave" else 25
    mock_aqi = 300 if concern == "aqi" else 50
    
    live_weather = {"temp": mock_temp, "aqi": mock_aqi, "description": "Sunny"}
    
    return {
        "city_baseline": city_baseline,
        "live_weather": live_weather, 
        "historical_weather": []
    }

def flood_agent_node(state: GraphState) -> Dict[str, Any]:
    print("Running Flood Assessment...")
    return {"risk_assessments": {**state.get("risk_assessments", {}), "Flood": "High"}}

def drought_agent_node(state: GraphState) -> Dict[str, Any]:
    print("Running Drought Assessment...")
    return {"risk_assessments": {**state.get("risk_assessments", {}), "Drought": "Medium"}}

def heatwave_agent_node(state: GraphState) -> Dict[str, Any]:
    print("🤖 Agent thinking: Running Heatwave Assessment...")
    
    city = state.get("city")
    live_weather = state.get("live_weather", {})
    temp = live_weather.get("temp", "Unknown")
    
    # Write the prompt for the AI
    prompt = f"""
    You are an expert climate risk assessor. 
    The city of {city} is currently experiencing a temperature of {temp}°C.
    Based on standard climate hazard thresholds, assess the heatwave risk level (Low, Medium, or High).
    Return ONLY a single word: Low, Medium, or High. Do not explain.
    """
    
    # Wrap the prompt in the format smolagents expects
    messages = [{"role": "user", "content": prompt}]
    
    # Call the Hugging Face model
    ai_response = ai_model(messages)
    
    # Extract the text from the response object
    decision = ai_response.content.strip()
    
    print(f"✅ AI Decision: Heatwave Risk is {decision}")
    
    # Update the state with the AI's actual decision
    return {"risk_assessments": {**state.get("risk_assessments", {}), "Heatwave": decision}}

def aqi_agent_node(state: GraphState) -> Dict[str, Any]:
    print("Running AQI Assessment...")
    return {"risk_assessments": {**state.get("risk_assessments", {}), "AQI": "Low"}}

def supervisor_node(state: GraphState) -> Dict[str, Any]:
    print("Supervisor evaluating overall severity...")
    return {"overall_severity": "High"}

def emergency_relocation_node(state: GraphState) -> Dict[str, Any]:
    print("🚨 CRITICAL: Relocation Agent Activated...")
    
    city = state.get("city", "Lahore")
    
    # Initialize the true Agent with the tool we imported from tools.py
    relocation_agent = ToolCallingAgent(
        tools=[calculate_safe_distance], 
        model=ai_model
    )
    
    prompt = f"""
    The user is in {city} and facing a severe climate emergency.
    You must find a safe relocation city. Consider 'Islamabad' as an option.
    You MUST use your calculate_safe_distance tool to verify the distance before recommending it.
    Return a short plan stating the safe city and the distance.
    """
    
    print("🤖 Agent thinking and using tools...")
    
    # Let the agent run its ReAct (Reason + Act) loop
    decision = relocation_agent.run(prompt)
    
    print(f"✅ AI Relocation Plan: {decision}")
    
    return {"safe_cities": [{"city": "Islamabad", "plan": decision}]}

def personalization_node(state: GraphState) -> Dict[str, Any]:
    profession = state.get("profession", "Citizen")
    print(f"Generating personalized advice for a {profession}...")
    return {"personalized_recommendations": ["Evacuate immediately."]}

# ==========================================
# 3. Define the Routing Logic (Edges)
# ==========================================

def route_to_specific_hazard(state: GraphState) -> str:
    concern = state.get("concern", "").lower()
    
    if concern == "flood":
        return "flood_agent"
    elif concern == "drought":
        return "drought_agent"
    elif concern == "heatwave":
        return "heatwave_agent"
    elif concern == "aqi":
        return "aqi_agent"
    else:
        return "supervisor"

def route_based_on_severity(state: GraphState) -> str:
    severity = state.get("overall_severity", "Low")
    if severity == "High":
        return "emergency_relocation"
    return "personalization"

# ==========================================
# 4. Build and Compile the Graph
# ==========================================

workflow = StateGraph(GraphState)

workflow.add_node("fetch_data", fetch_data_node)
workflow.add_node("flood_agent", flood_agent_node)
workflow.add_node("drought_agent", drought_agent_node)
workflow.add_node("heatwave_agent", heatwave_agent_node)
workflow.add_node("aqi_agent", aqi_agent_node)
workflow.add_node("supervisor", supervisor_node)
workflow.add_node("emergency_relocation", emergency_relocation_node)
workflow.add_node("personalization", personalization_node)

workflow.set_entry_point("fetch_data")

workflow.add_conditional_edges(
    "fetch_data",
    route_to_specific_hazard,
    {
        "flood_agent": "flood_agent",
        "drought_agent": "drought_agent",
        "heatwave_agent": "heatwave_agent",
        "aqi_agent": "aqi_agent",
        "supervisor": "supervisor"
    }
)

for agent_node in ["flood_agent", "drought_agent", "heatwave_agent", "aqi_agent"]:
    workflow.add_edge(agent_node, "supervisor")

workflow.add_conditional_edges(
    "supervisor",
    route_based_on_severity,
    {
        "emergency_relocation": "emergency_relocation",
        "personalization": "personalization"
    }
)

workflow.add_edge("emergency_relocation", "personalization")
workflow.add_edge("personalization", END)

app = workflow.compile()

# ==========================================
# 5. Testing the Graph Execution
# ==========================================
if __name__ == "__main__":
    print("\n" + "="*50)
    print("🚀 TESTING LANGGRAPH WORKFLOW ROUTING")
    print("="*50)

    initial_state = {
        "city": "Lahore",
        "profession": "Farmer",
        "concern": "Heatwave", 
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

    print(f"\nUser Input: City={initial_state['city']}, Profession={initial_state['profession']}, Concern={initial_state['concern']}\n")
    print("--- Execution Trace ---")

    final_state = app.invoke(initial_state)

    print("\n--- Final Output State ---")
    print(f"Risk Assessments: {final_state.get('risk_assessments')}")
    print(f"Overall Severity: {final_state.get('overall_severity')}")
    
    if final_state.get("safe_cities"):
        print(f"Emergency Relocation Triggered: {final_state.get('safe_cities')}")
    
    if final_state.get("personalized_recommendations"):
        print(f"Personalized Advice: {final_state.get('personalized_recommendations')}")
    
    print("="*50 + "\n")