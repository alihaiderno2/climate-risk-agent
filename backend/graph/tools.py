import os
import math
import pandas as pd
from smolagents import tool

# Connect to your actual CSV file
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
CSV_PATH = os.path.join(root_dir, 'pk_cities_cleanedAccApi_data.csv')

def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates the great-circle distance between two points on a sphere (in km)."""
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

@tool
def find_nearest_safe_cities(current_city: str) -> str:
    """
    Finds the nearest alternative cities for relocation during a climate emergency.
    It automatically filters out cities that are too close (under 50km) to avoid the same hazard zone.
    
    Args:
        current_city: The name of the city the user is currently in (e.g., 'Lahore').
    """
    print(f"   [TOOL EXECUTION] Calculating safe distances from {current_city} to all cities...")
    
    try:
        df = pd.read_csv(CSV_PATH)
        curr_city_lower = current_city.strip().lower()
        curr_row = df[df['city'].str.lower() == curr_city_lower]
        
        if curr_row.empty:
            return f"Error: Could not find {current_city} in the database."
            
        lat1, lon1 = curr_row.iloc[0]['lat'], curr_row.iloc[0]['lng']
        
        distances = []
        for index, row in df.iterrows():
            city_name = row['city']
            if city_name.lower() == curr_city_lower:
                continue # Skip the current city
                
            dist = haversine(lat1, lon1, row['lat'], row['lng'])
            
            # CRITICAL RULE: City must be more than 50km away to escape the local hazard!
            if dist > 50:
                distances.append({"city": city_name, "distance": dist, "population": row['population']})
                
        # Sort by closest distance
        distances.sort(key=lambda x: x['distance'])
        
        # Get the top 3 closest safe cities
        top_3 = distances[:3]
        
        result = "Top 3 nearest safe relocation cities (outside the 50km hazard zone):\n"
        for i, c in enumerate(top_3, 1):
            result += f"{i}. {c['city']} - {c['distance']:.2f} km away\n"
            
        return result
        
    except Exception as e:
        return f"Database Error: {str(e)}"