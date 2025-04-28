from recommendation_system import MoodBasedRecommender
import json
import os
import sys

def load_chat_history():
    try:
        with open('chat_history.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_chat_history(history):
    try:
        with open('chat_history.json', 'w') as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        print(f"Warning: Could not save chat history: {str(e)}")

def clear_screen():
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except:
        print("\n" * 50)  # Fallback to printing newlines

def print_header():
    print("=" * 50)
    print("Welcome to the Mental Health Support Chat!")
    print("I'm here to listen and suggest activities that might help you feel better.")
    print("Type 'exit' to end the conversation.")
    print("=" * 50)

def main():
    # Initialize the recommender
    try:
        recommender = MoodBasedRecommender('my_dataset.csv')
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Please make sure my_dataset.csv exists in the current directory.")
        sys.exit(1)
    
    # Load chat history
    chat_history = load_chat_history()
    
    clear_screen()
    print_header()
    
    while True:
        try:
            user_input = input("\nHow are you feeling today? ").strip()
            
            if user_input.lower() == 'exit':
                print("\nTake care! Remember, you're not alone. 💚")
                break
            
            if not user_input:
                print("Please share how you're feeling.")
                continue
            
            # Get recommendations based on user's mood
            recommendations = recommender.get_recommendations(user_input)
            
            # Save the interaction to chat history
            chat_history.append({
                'user_input': user_input,
                'recommendations': recommendations
            })
            save_chat_history(chat_history)
            
            # Display recommendations
            print("\nBased on how you're feeling, here are some activities that might help:")
            for i, rec in enumerate(recommendations, 1):
                print(f"\n{i}. {rec['activity']}")
                print(f"   Type: {rec['type']}")
                print(f"   Tags: {rec['tags']}")
            
            # Ask for feedback
            feedback = input("\nWould you like to try any of these activities? (yes/no): ").strip().lower()
            if feedback == 'yes':
                print("\nThat's great! Remember to be gentle with yourself and take things one step at a time.")
            else:
                print("\nThat's okay! Would you like to talk about something else?")
                
        except Exception as e:
            print(f"\nI apologize, but I encountered an error: {str(e)}")
            print("Please try again with a different description of how you're feeling.")

if __name__ == "__main__":
    main() 