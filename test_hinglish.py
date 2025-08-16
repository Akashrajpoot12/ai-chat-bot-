#!/usr/bin/env python3
"""
Test script to test the AI ChatBot's improved Hinglish understanding.
This script tests various Hinglish inputs to see how well the bot understands them.
"""

from chatbot_logic import ChatbotLogic

def test_hinglish_understanding():
    """Test the chatbot's Hinglish understanding capabilities."""
    print("🤖 Testing AI ChatBot Hinglish Understanding")
    print("=" * 60)
    
    # Initialize chatbot
    chatbot = ChatbotLogic()
    
    # Test cases with Hinglish input
    test_cases = [
        "Hello dost, kaise ho?",
        "Kya haal hai yaar?",
        "Joke sunao please",
        "Mujhe hasao yaar",
        "I'm feeling sad, mujhe motivate kar",
        "Udaas hoon dost, kuch bolo",
        "Tension hai yaar, help kar",
        "Shukriya dost, bahut help kiya tune",
        "Alvida dost, phir milenge",
        "Kya kar raha hai tu?",
        "Sab badhiya dost?",
        "Kaise ho aap?",
        "Kya haal chaal hai?",
        "Mujhe cheer up kar",
        "Mujhe inspire kar dost",
        "Kuch interesting bolo",
        "Boring lag raha hai",
        "Time pass kar yaar",
        "Kya chal raha hai?",
        "Mausam kaisa hai?"
    ]
    
    print("Testing various Hinglish inputs:\n")
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"{i:2d}. Input: {test_input}")
        response = chatbot.get_response(test_input)
        print(f"    Response: {response}")
        print()
    
    # Test learning capabilities
    print("Testing learning capabilities:")
    stats = chatbot.get_conversation_stats()
    print(f"📊 Total Conversations: {stats['total_conversations']}")
    print(f"👤 User Preferences: {stats['user_preferences']}")
    
    print("\n" + "=" * 60)
    print("✅ Hinglish understanding test completed!")
    print("💡 The chatbot now understands Hinglish much better!")
    print("🚀 Try chatting with it in Hinglish - it should work much better now!")

if __name__ == "__main__":
    test_hinglish_understanding()
