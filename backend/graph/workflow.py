import sys
import os
import pandas as pd
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta
load_dotenv()

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)


from smolagents import LiteLLMModel, ToolCallingAgent
from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END
from graph.tools import find_nearest_safe_cities

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
    survival_kit: List[str]
    official_dispatch: str         
    relief_logistics: Dict[str, int]


def fetch_data_node(state: GraphState) -> Dict[str, Any]:
    # 1. DEFINE BOTH VARIABLES RIGHT AT THE TOP
    city = state.get("city", "")
    concern = state.get("concern", "").lower() 
    
    print(f"📥 Fetching data for: {city}...")
    
    # --- 1. Fetch CSV Baseline (We always want real population data) ---
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
    except Exception as e:
        print(f"   [ERROR] Could not load CSV: {e}")

    # ==========================================
    # 🚨 HACKATHON DEMO MODE TOGGLE 🚨
    DEMO_MODE = True 
    # ==========================================

    if DEMO_MODE:
        print(f"   [DEMO MODE ACTIVE] Injecting extreme dummy data for {concern}...")
        
        # Inject catastrophic weather based on whatever the user selected
        return {
            "city_baseline": city_baseline,
            "live_weather": {
                "temp": 49 if concern == "heatwave" else 25,
                "aqi": 450 if concern == "aqi" else 50,
                "condition": "Heavy Rain and Thunderstorms" if concern == "flood" else "Sunny",
                "humidity": 10 if concern == "drought" else 60
            },
            "forecast_weather": [
                {"date": "Tomorrow", "max_temp": 50, "min_temp": 35, "condition": "Extreme Heat"},
                {"date": "Day 2", "max_temp": 48, "min_temp": 34, "condition": "Sunny"}
            ],
            "historical_weather": []
        }

    # --- 2. Real WeatherAPI Logic (Only runs if DEMO_MODE = False) ---
    API_KEY = os.getenv("WEATHER_API_KEY", "YOUR_API_KEY_HERE")
    live_weather, forecast_weather, historical_weather = {}, [], []
    
    try:
        url_forecast = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days=3&aqi=yes"
        resp = requests.get(url_forecast, timeout=5)
        
        if resp.status_code != 200:
            raise Exception("API Request Failed")
            
        resp_f = resp.json()
        
        live_weather = {
            "temp": resp_f["current"]["temp_c"],
            "condition": resp_f["current"]["condition"]["text"],
            "humidity": resp_f["current"]["humidity"],
            "wind_kph": resp_f["current"]["wind_kph"],
            "aqi": resp_f["current"]["air_quality"].get("pm2_5", 50)
        }
        
        for day in resp_f.get("forecast", {}).get("forecastday", []):
            forecast_weather.append({
                "date": day["date"],
                "max_temp": day["day"]["maxtemp_c"],
                "min_temp": day["day"]["mintemp_c"],
                "condition": day["day"]["condition"]["text"]
            })
            
        print(f"   [LIVE WEATHER SUCCESS] {live_weather['temp']}°C")
        
    except Exception as e:
        print(f"   [API ERROR] {e}")
        # Note: I removed the duplicate `concern = ...` from here to prevent the scope error!
    
    return {
        "city_baseline": city_baseline,
        "live_weather": live_weather, 
        "forecast_weather": forecast_weather,
        "historical_weather": historical_weather
    }


def flood_agent_node(state: GraphState) -> Dict[str, Any]:
    print("Agent thinking: Running Flood Assessment...")
    city = state.get("city")
    live_weather = state.get("live_weather", {})
    forecast = state.get("forecast_weather", [])

    # Extract conditions to see if it's raining
    current_condition = live_weather.get("condition", "Unknown")
    forecast_conditions = [day.get("condition", "") for day in forecast]

    prompt = f"""
    You are an expert flood risk assessor.
    City: {city}
    Current Weather: {current_condition}
    3-Day Forecast: {', '.join(forecast_conditions)}

    Based on the presence of heavy rain, storms, or clear weather, assess the flood risk level (Low, Medium, or High).
    Return ONLY a single word: Low, Medium, or High. Do not explain.
    """

    messages = [{"role": "user", "content": prompt}]
    ai_response = ai_model(messages)
    decision = ai_response.content.strip()

    print(f" AI Decision: Flood Risk is {decision}")
    return {"risk_assessments": {**state.get("risk_assessments", {}), "Flood": decision}}


def drought_agent_node(state: GraphState) -> Dict[str, Any]:
    print(" Agent thinking: Running Drought Assessment...")
    city = state.get("city")
    live_weather = state.get("live_weather", {})
    temp = live_weather.get("temp", "Unknown")
    humidity = live_weather.get("humidity", "Unknown")
    
    prompt = f"""
    You are an expert drought risk assessor.
    City: {city}
    Current Temperature: {temp}°C
    Current Humidity: {humidity}%
    
    If temperature is very high and humidity is very low, the risk is higher. Assess the drought risk level (Low, Medium, or High).
    Return ONLY a single word: Low, Medium, or High. Do not explain.
    """
    
    messages = [{"role": "user", "content": prompt}]
    ai_response = ai_model(messages)
    decision = ai_response.content.strip()
    
    print(f" AI Decision: Drought Risk is {decision}")
    return {"risk_assessments": {**state.get("risk_assessments", {}), "Drought": decision}}


def aqi_agent_node(state: GraphState) -> Dict[str, Any]:
    print(" Agent thinking: Running AQI Assessment...")
    city = state.get("city")
    live_weather = state.get("live_weather", {})
    aqi = live_weather.get("aqi", 50)
    
    prompt = f"""
    You are an expert air quality assessor.
    City: {city}
    Current PM2.5 AQI: {aqi}
    
    Use standard AQI thresholds (e.g., under 50 is Low risk, 50-150 is Medium risk, over 150 is High risk).
    Assess the health risk level (Low, Medium, or High).
    Return ONLY a single word: Low, Medium, or High. Do not explain.
    """
    
    messages = [{"role": "user", "content": prompt}]
    ai_response = ai_model(messages)
    decision = ai_response.content.strip()
    
    print(f" AI Decision: AQI Risk is {decision}")
    return {"risk_assessments": {**state.get("risk_assessments", {}), "AQI": decision}}

def heatwave_agent_node(state: GraphState) -> Dict[str, Any]:
    print(" Agent thinking: Running Heatwave Assessment...")
    
    city = state.get("city")
    live_weather = state.get("live_weather", {})
    temp = live_weather.get("temp", "Unknown")
    
    prompt = f"""
    You are an expert climate risk assessor. 
    The city of {city} is currently experiencing a temperature of {temp}°C.
    Based on standard climate hazard thresholds, assess the heatwave risk level (Low, Medium, or High).
    Return ONLY a single word: Low, Medium, or High. Do not explain.
    """
    
    messages = [{"role": "user", "content": prompt}]

    ai_response = ai_model(messages)
    
    decision = ai_response.content.strip()
    
    print(f"AI Decision: Heatwave Risk is {decision}")
    
    # Update the state with the AI's actual decision
    return {"risk_assessments": {**state.get("risk_assessments", {}), "Heatwave": decision}}


def supervisor_node(state: GraphState) -> Dict[str, Any]:
    print("Supervisor evaluating overall severity based on AI assessments...")
    
    assessments = state.get("risk_assessments", {})
    
    overall_severity = "Low"
    for hazard, risk_level in assessments.items():
        if "high" in risk_level.lower():
            overall_severity = "High"
            break
        elif "medium" in risk_level.lower() and overall_severity != "High":
            overall_severity = "Medium"
            
    print(f"   [SUPERVISOR DECISION] Overall Emergency Level is: {overall_severity}")
    return {"overall_severity": overall_severity}

def emergency_relocation_node(state: GraphState) -> Dict[str, Any]:
    print(" CRITICAL: Relocation Agent Activated...")
    
    city = state.get("city", "Lahore")
    
    relocation_agent = ToolCallingAgent(
        tools=[find_nearest_safe_cities], 
        model=ai_model
    )
    
    prompt = f"""
    The user is in {city} and facing a severe climate emergency.
    You MUST use the `find_nearest_safe_cities` tool to get a list of the 3 closest safe cities.
    Review the tool's result, pick the absolute best city for relocation, and write a short, clear evacuation plan stating the chosen city and its distance.
    """
    
    print(" Agent thinking and scanning all cities...")
    
    decision = relocation_agent.run(prompt)
    
    print(f"AI Relocation Plan: {decision}")
    
    return {"safe_cities": [{"plan": decision}]}
def personalization_node(state: GraphState) -> Dict[str, Any]:
    profession = state.get("profession", "Citizen")
    concern = state.get("concern", "Unknown Hazard")
    city = state.get("city", "Unknown City")
    severity = state.get("overall_severity", "Low")
    
    print(f"Generating personalized advice for a {profession} facing {concern}...")
    
    prompt = f"""
    You are a disaster response expert. The user is a {profession} in {city} facing a {severity} severity {concern}.
    Write 3 quick, highly actionable bullet points of advice specifically tailored to their profession.
    For example, if they are a Farmer, talk about livestock and crops. If a Doctor, talk about medical supplies.
    Keep it concise. Do not use formatting like markdown asterisks, just return plain text bullet points.
    """
    
    
    messages = [{"role": "user", "content": prompt}]
    

    ai_response = ai_model(messages)
    advice_text = ai_response.content.strip()
    
    advice_list = [line.strip() for line in advice_text.split('\n') if line.strip()]
    
    return {"personalized_recommendations": advice_list}

def survival_kit_node(state: GraphState) -> Dict[str, Any]:
    profession = state.get("profession", "Citizen")
    concern = state.get("concern", "Emergency")
    severity = state.get("overall_severity", "Low")
    
    print(f" Generating Emergency Survival Kit for a {profession} facing {concern}...")
    
    prompt = f"""
    You are a disaster preparedness expert. A {profession} is facing a {severity} severity {concern}.
    Generate a highly specific, 5-item emergency survival kit checklist tailored to their profession and this specific hazard.
    For example, a doctor needs medical supplies, a farmer needs animal feed or crop covers.
    Return ONLY the 5 items as a plain text bulleted list (using •). Keep each item to one short sentence. Do not include introductory text.
    """
    
    messages = [{"role": "user", "content": prompt}]
    
    ai_response = ai_model(messages)
    kit_text = ai_response.content.strip()
    
    kit_list = [line.strip() for line in kit_text.split('\n') if line.strip()]
    
    return {"survival_kit": kit_list}

def ngo_dispatch_node(state: GraphState) -> Dict[str, Any]:
    print("📡 Drafting Official Government/NGO Alert and calculating logistics...")
    
    city = state.get("city", "Unknown")
    concern = state.get("concern", "Emergency")
    
    # Safely get population, default to 100,000 if not found
    population = state.get("city_baseline", {}).get("population", 100000)
    # Ensure it's a valid number, otherwise fallback to 100000
    if pd.isna(population):
        population = 100000
    population = int(population)
    
    # 1. Macro Logistics Math
    # Assume in a High severity event, 10% of the population needs immediate assistance
    affected_pop = int(population * 0.10)
    logistics = {
        "affected_population": affected_pop,
        "water_liters": affected_pop * 3,  # 3 liters of water per person
        "tents": affected_pop // 5,        # 1 tent per 5 people
        "medical_kits": affected_pop // 50 # 1 medical kit per 50 people
    }
    
    safe_cities = state.get("safe_cities", [])
    evac_plan = safe_cities[0]["plan"] if safe_cities else "No evacuation route generated."
    
    # 2. AI Drafting the SitRep
    prompt = f"""
    You are an AI automated emergency broadcast system for the PDMA (Provincial Disaster Management Authority) of Pakistan.
    Write a short, highly professional, military-style Situation Report (SitRep) to alert the government.
    
    Incident: Severe {concern}
    Location: {city}
    Total Population: {population}
    Estimated Affected Population: {affected_pop}
    Required Relief Logistics: {logistics['water_liters']}L Water, {logistics['tents']} Tents, {logistics['medical_kits']} Medical Kits.
    AI Evacuation Plan: {evac_plan}
    
    Draft a 4-sentence alert summarizing the crisis, stating the exact logistical requirements, and outlining the evacuation recommendation. Do not include markdown formatting like asterisks.
    """
    
    messages = [{"role": "user", "content": prompt}]
    ai_response = ai_model(messages)
    dispatch_text = ai_response.content.strip()
    
    print(" Official Dispatch & Logistics Calculated")
    
    return {
        "official_dispatch": dispatch_text,
        "relief_logistics": logistics
    }

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


workflow = StateGraph(GraphState)

workflow.add_node("fetch_data", fetch_data_node)
workflow.add_node("flood_agent", flood_agent_node)
workflow.add_node("drought_agent", drought_agent_node)
workflow.add_node("heatwave_agent", heatwave_agent_node)
workflow.add_node("aqi_agent", aqi_agent_node)
workflow.add_node("supervisor", supervisor_node)
workflow.add_node("emergency_relocation", emergency_relocation_node)
workflow.add_node("personalization", personalization_node)
workflow.add_node("survival_kit", survival_kit_node)
workflow.add_node("ngo_dispatch", ngo_dispatch_node)

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

workflow.add_edge("emergency_relocation", "ngo_dispatch")
workflow.add_edge("ngo_dispatch", "personalization")
workflow.add_edge("personalization", "survival_kit")
workflow.add_edge("personalization", END)

app = workflow.compile()


if __name__ == "__main__":
    print("\n" + "="*50)
    print(" TESTING LANGGRAPH WORKFLOW ROUTING")
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