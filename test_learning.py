#!/usr/bin/env python3
"""
Test script to demonstrate the AI ChatBot's learning capabilities.
This script shows how the chatbot learns from conversations and user feedback.
"""

from chatbot_logic import ChatbotLogic
import json

def test_learning_capabilities():
    """Test the chatbot's learning features."""
    print("🤖 Testing AI ChatBot Learning Capabilities")
    print("=" * 50)
    
    # Initialize chatbot
    chatbot = ChatbotLogic()
    
    # Test 1: Basic conversation
    print("\n1️⃣ Testing basic conversation...")
    user_input = "Hello"
    response = chatbot.get_response(user_input)
    print(f"User: {user_input}")
    print(f"Bot: {response}")
    
    # Test 2: Joke conversation (should increase joke preference)
    print("\n2️⃣ Testing joke preference learning...")
    user_input = "Tell me a joke"
    response = chatbot.get_response(user_input)
    print(f"User: {user_input}")
    print(f"Bot: {response}")
    
    # Test 3: Another joke (should further increase preference)
    print("\n3️⃣ Testing joke preference increase...")
    user_input = "Another joke please"
    response = chatbot.get_response(user_input)
    print(f"User: {user_input}")
    print(f"Bot: {response}")
    
    # Test 4: Motivation conversation
    print("\n4️⃣ Testing motivation preference learning...")
    user_input = "I'm feeling sad"
    response = chatbot.get_response(user_input)
    print(f"User: {user_input}")
    print(f"Bot: {response}")
    
    # Test 5: Provide feedback
    print("\n5️⃣ Testing feedback system...")
    chatbot.provide_feedback("Tell me a joke", "positive")
    chatbot.provide_feedback("I'm feeling sad", "positive")
    print("✅ Feedback provided for jokes and motivation")
    
    # Test 6: Show learning statistics
    print("\n6️⃣ Learning Statistics:")
    stats = chatbot.get_conversation_stats()
    print(f"📊 Total Conversations: {stats['total_conversations']}")
    print(f"👤 User Preferences: {stats['user_preferences']}")
    print(f"📝 Feedback Stats: {stats['feedback_stats']}")
    
    # Test 7: Test personalized responses
    print("\n7️⃣ Testing personalized responses...")
    user_input = "I need motivation"
    response = chatbot.get_response(user_input)
    print(f"User: {user_input}")
    print(f"Bot: {response}")
    
    print("\n" + "=" * 50)
    print("✅ Learning capabilities test completed!")
    print("💡 The chatbot now remembers your preferences and can provide personalized responses!")
    
    return chatbot

def show_learning_file():
    """Show the contents of the learning data file."""
    try:
        with open("chatbot_learning.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            print("\n📁 Learning Data File Contents:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
    except FileNotFoundError:
        print("\n📁 Learning data file not found yet. It will be created after conversations.")

if __name__ == "__main__":
    # Test the learning capabilities
    chatbot = test_learning_capabilities()
    
    # Show the learning data file
    show_learning_file()
    
    print("\n🚀 To see the full learning interface, run: python chatbot_ui.py")
    print("💡 Use the 👍/👎 buttons to provide feedback and watch the bot learn!")
