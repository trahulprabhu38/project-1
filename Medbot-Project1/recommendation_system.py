import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json

class MoodBasedRecommender:
    def __init__(self, recommender):
        self.df = pd.read_csv("my_dataset.csv")
        self.df['text_representation'] = self.df['item_description'] + ' ' + self.df['item_tags']
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df['text_representation'])
        self.issue_to_idx = {issue: idx for idx, issue in enumerate(self.df['reported_issue'].unique())}
        
    def get_recommendations(self, user_mood, num_recommendations=3):
        mood_vector = self.vectorizer.transform([user_mood])
        similarities = cosine_similarity(mood_vector, self.tfidf_matrix)
        top_indices = similarities[0].argsort()[-num_recommendations:][::-1]
        
        recommendations = []
        for idx in top_indices:
            recommendation = {
                'activity': self.df.iloc[idx]['item_description'],
                'type': self.df.iloc[idx]['item_type'],
                'tags': self.df.iloc[idx]['item_tags'],
                'similarity_score': float(similarities[0][idx])
            }
            recommendations.append(recommendation)
            
        return recommendations

def main():
    recommender = MoodBasedRecommender('my_dataset.csv')
    
    print("Welcome to the Mood-Based Activity Recommender!")
    print("Tell me how you're feeling, and I'll suggest some activities to help.")
    
    while True:
        user_mood = input("\nHow are you feeling today? (or type 'exit' to quit): ")
        
        if user_mood.lower() == 'exit':
            print("Take care! Hope you feel better soon!")
            break
            
        recommendations = recommender.get_recommendations(user_mood)
        
        print("\nBased on how you're feeling, here are some activities that might help:")
        for i, rec in enumerate(recommendations, 1):
            print(f"\n{i}. {rec['activity']}")
            print(f"   Type: {rec['type']}")
            print(f"   Tags: {rec['tags']}")

if __name__ == "__main__":
    main()