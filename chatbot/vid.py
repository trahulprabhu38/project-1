import requests
import json
import time

mental_health_states = [
    "anxious", "lonely", "sad", "stressed",
    "depressed", "frustrated", "angry", "worried", "nervous", "exhausted", "hopeless",
    "shame", "fear", "panic",
    "self-doubt", "low self-esteem", "distressed", "unmotivated",
    "overwhelmed", "burnt out", "guilt", "grief", "emptiness",
    "worthless", "helpless", "restless", "isolated", "insecure",
    "broken", "lost", "unloved", "rejected", "abandoned",
    "confused", "betrayed", "powerless", "apathetic", "heartbroken",
    "disconnected", "vulnerable", "regretful", "irritable", "resentful",
    "emotional pain", "mental fatigue", "dread", "invisible",
    "despair", "detachment", "dissociation", "emotional numbness",
    "self-hatred",
    "suicidal thoughts", "desire to disappear", "feeling like a burden",
    "thoughts of self-harm", "hopeless about future",
    "writing goodbye notes", "emotional shutdown",
    "urge to escape life", "preparing for death", "existential dread",
    "flashbacks", "social withdrawal", "mistrust", "mania", "psychosis",
    "obsession", "compulsion", "nightmares", "loss of identity",
    "agitation", "self-harm urges"
]

url = 'https://magicloops.dev/api/loop/358a84e8-378e-47b3-9af1-9a658bbf97d4/run'

all_recommendations = {}

print("Collecting recommendations for all mental health states...")
for mood in mental_health_states:
    print(f"Processing: {mood}")
    payload = { "mood": mood }
    
    try:
        response = requests.get(url, json=payload)
        responseJson = response.json()
        
        if isinstance(responseJson, list):
            limited_recommendations = responseJson[:3]
        elif isinstance(responseJson, dict):
            for key, value in responseJson.items():
                if isinstance(value, list):
                    responseJson[key] = value[:3]
            limited_recommendations = responseJson
        else:
            limited_recommendations = responseJson
            
        all_recommendations[mood] = limited_recommendations
        time.sleep(1)
        
    except Exception as e:
        print(f"Error processing {mood}: {str(e)}")
        all_recommendations[mood] = {"error": str(e)}
with open('mental_health_recommendations.json', 'w') as json_file:
    json.dump(all_recommendations, json_file, indent=4)

print("\nAll recommendations have been saved to mental_health_recommendations.json")
print(f"Processed {len(mental_health_states)} mental health states")
print("Limited to 3 recommendations per state")