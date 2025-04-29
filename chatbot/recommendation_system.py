import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json

class MoodBasedRecommender:
    def __init__(self, dataset_path="mental_health_chatbot_interactions.csv"):
        self.df = pd.read_csv(dataset_path)
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df['mood'])
        
    def get_recommendations(self, user_mood, num_recommendations=3):
        mood_vector = self.vectorizer.transform([user_mood])
        similarities = cosine_similarity(mood_vector, self.tfidf_matrix)
        top_indices = similarities[0].argsort()[-num_recommendations:][::-1]
        
        recommendations = []
        for idx in top_indices:
            recommendation = {
                'exercise': self.df.iloc[idx]['exercise'],
                'similarity_score': float(similarities[0][idx])
            }
            recommendations.append(recommendation)
            
        return recommendations

def main():
    recommender = MoodBasedRecommender()
    
    print("Welcome to the Mood-Based Exercise Recommender!")
    print("Tell me how you're feeling, and I'll suggest some exercises to help.")
    
    while True:
        user_mood = input("\nHow are you feeling today? (or type 'exit' to quit): ")
        
        if user_mood.lower() == 'exit':
            print("Take care! Hope you feel better soon!")
            break
            
        recommendations = recommender.get_recommendations(user_mood)
        
        print("\nBased on how you're feeling, here are some exercises that might help:")
        for i, rec in enumerate(recommendations, 1):
            print(f"\n{i}. {rec['exercise']}")

if __name__ == "__main__":
    main()