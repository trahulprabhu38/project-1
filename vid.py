import requests
import json
import time

# List of common mental health states
mental_health_states = [
    "anxious", "lonely", "sad", "stressed",
    "depressed", "frustrated", "angry", "worried", "nervous",  "exhausted", "hopeless", 
    "shame", "fear", "panic", 
    "self-doubt", "low self-esteem", "distressed",
    "unmotivated",   
]

url = 'https://magicloops.dev/api/loop/358a84e8-378e-47b3-9af1-9a658bbf97d4/run'

# Dictionary to store all recommendations
all_recommendations = {}

print("Collecting recommendations for all mental health states...")
for mood in mental_health_states:
    print(f"Processing: {mood}")
    payload = { "mood": mood }
    
    try:
        response = requests.get(url, json=payload)
        responseJson = response.json()
        
        # Limit recommendations to 3 items
        if isinstance(responseJson, list):
            limited_recommendations = responseJson[:3]
        elif isinstance(responseJson, dict):
            # If the response is a dictionary, try to find a list of recommendations
            for key, value in responseJson.items():
                if isinstance(value, list):
                    responseJson[key] = value[:3]
            limited_recommendations = responseJson
        else:
            limited_recommendations = responseJson
            
        all_recommendations[mood] = limited_recommendations
        
        # Add a small delay to avoid overwhelming the API
        time.sleep(1)
        
    except Exception as e:
        print(f"Error processing {mood}: {str(e)}")
        all_recommendations[mood] = {"error": str(e)}

# Store all recommendations in a single JSON file
with open('mental_health_recommendations.json', 'w') as json_file:
    json.dump(all_recommendations, json_file, indent=4)

print("\nAll recommendations have been saved to mental_health_recommendations.json")
print(f"Processed {len(mental_health_states)} mental health states")
print("Limited to 3 recommendations per state")