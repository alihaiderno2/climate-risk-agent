import os
import math
import pandas as pd
from smolagents import tool

# Get the absolute path to the CSV file (assuming it's in the root folder)
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
CSV_PATH = os.path.join(root_dir, 'pk_cities_cleanedAccApi_data.csv')

def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0 
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

@tool
def calculate_safe_distance(current_city: str, destination_city: str) -> str:
    """
    Calculates the physical distance in kilometers between two cities in Pakistan.
    Use this to determine if a relocation city is far enough from the current disaster zone.
    
    Args:
        current_city: The name of the city the user is currently in (e.g., 'Karachi').
        destination_city: The name of the proposed safe city (e.g., 'Islamabad').
    """
    print(f"   [TOOL EXECUTION] Looking up exact distance from {current_city} to {destination_city} in CSV...")
    
    try:
        df = pd.read_csv(CSV_PATH)
        
        # Standardize names for searching
        curr_city_lower = current_city.strip().lower()
        dest_city_lower = destination_city.strip().lower()
        
        # Find the cities in the dataframe
        curr_row = df[df['city'].str.lower() == curr_city_lower]
        dest_row = df[df['city'].str.lower() == dest_city_lower]
        
        if curr_row.empty:
            return f"Error: Could not find {current_city} in the database."
        if dest_row.empty:
            return f"Error: Could not find {destination_city} in the database."
            
        # Extract coordinates
        lat1, lon1 = curr_row.iloc[0]['lat'], curr_row.iloc[0]['lng']
        lat2, lon2 = dest_row.iloc[0]['lat'], dest_row.iloc[0]['lng']
        
        # Calculate distance
        distance = haversine(lat1, lon1, lat2, lon2)
        
        return f"{distance:.2f} km"
        
    except Exception as e:
        return f"Database Error: {str(e)}"