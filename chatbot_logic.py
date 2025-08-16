import json
import random
import re
import os
from datetime import datetime
from typing import List, Dict, Any
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Download required NLTK data (uncomment if running for the first time)
# nltk.download('punkt')
# nltk.download('stopwords')

class ChatbotLogic:
    """
    Chatbot logic class that handles intent recognition and response generation.
    Uses NLTK for natural language processing and keyword matching.
    Now includes learning capabilities to improve over time.
    """
    
    def __init__(self, intents_file: str = "intents.json"):
        """
        Initialize the chatbot with intents data and learning capabilities.
        
        Args:
            intents_file (str): Path to the intents JSON file
        """
        self.intents_file = intents_file
        self.intents_data = self._load_intents()
        self.learning_data_file = "chatbot_learning.json"
        self.conversation_history = []
        self.user_preferences = {}
        self.response_feedback = {}
        
        # Load learning data
        self.learning_data = self._load_learning_data()
        
        self.fallback_responses = [
            "Arey dost, samajh nahi aaya! 😅 Thoda aur simple tarike se bolo na!",
            "Yaar, yeh kya bola tune? 😄 Thoda aur clearly bolo!",
            "Arey, main toh abhi learning phase mein hoon! 😊 Thoda aur simple bolo!",
            "Interesting lag raha hai, lekin main samajh nahi paa raha! 😅 Thoda aur explain kar!",
            "Arey dost, yeh topic toh mujhe pata nahi! 😄 Koi aur baat kar sakte hain hum!",
            "Yaar, yeh toh meri samajh se bahar hai! 😊 Koi aur sawal puch sakta hai tu!",
            "Arey, main toh bas simple baatein samajh sakta hoon! 😄 Thoda basic level pe bolo!",
            "Dost, yeh toh meri knowledge se bahar hai! 😅 Koi aur topic pe baat karte hain!",
            "Arey yaar, yeh kya bola tune? 😅 Thoda aur clearly bolo na!",
            "Dost, main toh abhi Hinglish samajh raha hoon! 😊 Thoda simple bolo!",
            "Yaar, yeh kya language hai? 😄 English ya Hindi mein bolo!",
            "Arey, main toh bas basic Hinglish samajh sakta hoon! 😊 Thoda simple bolo!",
            "Dost, yeh kya bola tune? 😅 Thoda aur clearly explain kar!",
            "Arey yaar, main toh abhi learning kar raha hoon! 😄 Thoda simple bolo!",
            "Dost, yeh kya bola tune? 😊 Thoda aur clearly bolo na!"
        ]
        
        # Initialize NLTK components
        try:
            self.stop_words = set(stopwords.words('english'))
        except LookupError:
            # If stopwords not available, use a basic set
            self.stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
    
    def _load_learning_data(self) -> Dict[str, Any]:
        """Load learning data from file."""
        try:
            if os.path.exists(self.learning_data_file):
                with open(self.learning_data_file, 'r', encoding='utf-8') as file:
                    return json.load(file)
        except Exception as e:
            print(f"Warning: Could not load learning data: {e}")
        
        # Return default learning data structure
        return {
            "conversation_history": [],
            "user_preferences": {},
            "response_feedback": {},
            "learned_patterns": [],
            "custom_responses": {},
            "last_updated": datetime.now().isoformat()
        }
    
    def _save_learning_data(self):
        """Save learning data to file."""
        try:
            self.learning_data.update({
                "conversation_history": self.conversation_history[-100:],  # Keep last 100 conversations
                "user_preferences": self.user_preferences,
                "response_feedback": self.response_feedback,
                "last_updated": datetime.now().isoformat()
            })
            
            with open(self.learning_data_file, 'w', encoding='utf-8') as file:
                json.dump(self.learning_data, file, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Could not save learning data: {e}")
    
    def _load_intents(self) -> List[Dict[str, Any]]:
        """
        Load intents data from JSON file.
        
        Returns:
            List[Dict[str, Any]]: List of intent dictionaries
        """
        try:
            with open(self.intents_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data.get('intents', [])
        except FileNotFoundError:
            print(f"Warning: {self.intents_file} not found. Using default intents.")
            return []
        except json.JSONDecodeError:
            print(f"Warning: Error parsing {self.intents_file}. Using default intents.")
            return []
    
    def _preprocess_text(self, text: str) -> List[str]:
        """
        Preprocess text by tokenizing and removing stop words.
        Now handles Hinglish (Hindi-English mixed) text better.
        
        Args:
            text (str): Input text to preprocess
            
        Returns:
            List[str]: List of preprocessed tokens
        """
        # Convert to lowercase and tokenize
        tokens = word_tokenize(text.lower())
        
        # Keep both English and Hindi tokens, remove only English stop words
        # Don't filter out Hindi words as they might be important
        filtered_tokens = []
        for token in tokens:
            # Keep tokens that are either:
            # 1. English words that are not stop words
            # 2. Hindi words (non-English characters)
            # 3. Mixed words (containing both English and Hindi)
            if (token.isalpha() and token not in self.stop_words) or \
               any(ord(char) > 127 for char in token) or \
               (any(ord(char) > 127 for char in token) and any(ord(char) <= 127 for char in token)):
                filtered_tokens.append(token)
        
        return filtered_tokens
    
    def _calculate_similarity(self, user_tokens: List[str], pattern_tokens: List[str]) -> float:
        """
        Calculate similarity between user input and intent pattern.
        Now handles Hinglish and mixed language better.
        
        Args:
            user_tokens (List[str]): Preprocessed user input tokens
            pattern_tokens (List[str]): Preprocessed pattern tokens
            
        Returns:
            float: Similarity score (0.0 to 1.0)
        """
        if not user_tokens or not pattern_tokens:
            return 0.0
        
        # Count exact matches
        exact_matches = sum(1 for token in user_tokens if token in pattern_tokens)
        
        # Count partial matches (for Hinglish variations)
        partial_matches = 0
        for user_token in user_tokens:
            for pattern_token in pattern_tokens:
                # Check if tokens are similar (partial match)
                if self._are_tokens_similar(user_token, pattern_token):
                    partial_matches += 1
                    break
        
        # Use the better of exact or partial matches
        best_matches = max(exact_matches, partial_matches)
        
        # Calculate similarity as matches over total unique tokens
        total_unique = len(set(user_tokens + pattern_tokens))
        if total_unique == 0:
            return 0.0
        
        return best_matches / total_unique
    
    def _are_tokens_similar(self, token1: str, token2: str) -> bool:
        """
        Check if two tokens are similar (for Hinglish variations).
        
        Args:
            token1 (str): First token
            token2 (str): Second token
            
        Returns:
            bool: True if tokens are similar
        """
        # Exact match
        if token1 == token2:
            return True
        
        # Check for common Hinglish variations
        variations = {
            'hello': ['hi', 'hey', 'namaste', 'kaise ho', 'kya haal'],
            'hi': ['hello', 'hey', 'namaste', 'kaise ho', 'kya haal'],
            'hey': ['hello', 'hi', 'namaste', 'kaise ho', 'kya haal'],
            'joke': ['joke', 'funny', 'hasao', 'mazak', 'comedy'],
            'funny': ['joke', 'funny', 'hasao', 'mazak', 'comedy'],
            'sad': ['sad', 'depressed', 'udaas', 'dukhi', 'unhappy'],
            'happy': ['happy', 'khush', 'mast', 'excited', 'joyful'],
            'help': ['help', 'madad', 'sahayata', 'assist', 'support'],
            'thanks': ['thanks', 'thank you', 'shukriya', 'dhanyawad', 'gratitude'],
            'bye': ['bye', 'goodbye', 'alvida', 'phir milenge', 'see you']
        }
        
        # Check if tokens are in the same variation group
        for group, words in variations.items():
            if token1 in words and token2 in words:
                return True
        
        # Check for partial string matching (for Hinglish variations)
        if len(token1) > 2 and len(token2) > 2:
            # Check if one token contains the other
            if token1 in token2 or token2 in token1:
                return True
            
            # Check for similar length and character overlap
            if abs(len(token1) - len(token2)) <= 2:
                common_chars = sum(1 for c in token1 if c in token2)
                if common_chars >= min(len(token1), len(token2)) * 0.6:
                    return True
        
        return False
    
    def _learn_from_conversation(self, user_input: str, bot_response: str, feedback: str = None):
        """
        Learn from conversation and user feedback.
        
        Args:
            user_input (str): User's message
            bot_response (str): Bot's response
            feedback (str): User feedback (optional)
        """
        # Store conversation
        conversation = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "bot_response": bot_response,
            "feedback": feedback
        }
        self.conversation_history.append(conversation)
        
        # Store user preferences based on conversation patterns
        if "joke" in user_input.lower() or "funny" in user_input.lower():
            self.user_preferences["likes_jokes"] = self.user_preferences.get("likes_jokes", 0) + 1
        
        if "motivation" in user_input.lower() or "sad" in user_input.lower():
            self.user_preferences["needs_motivation"] = self.user_preferences.get("needs_motivation", 0) + 1
        
        # Store feedback if provided
        if feedback:
            self.response_feedback[user_input] = feedback
        
        # Save learning data periodically
        if len(self.conversation_history) % 10 == 0:  # Save every 10 conversations
            self._save_learning_data()
    
    def _get_personalized_response(self, intent_tag: str, responses: List[str]) -> str:
        """
        Get personalized response based on user preferences and conversation history.
        
        Args:
            intent_tag (str): Intent tag
            responses (List[str]): Available responses
            
        Returns:
            str: Personalized response
        """
        # Check if user has specific preferences
        if intent_tag == "joke" and self.user_preferences.get("likes_jokes", 0) > 2:
            # User likes jokes, give more variety
            return random.choice(responses)
        elif intent_tag == "motivation" and self.user_preferences.get("needs_motivation", 0) > 1:
            # User needs motivation, give encouraging responses
            motivational_responses = [
                "Arey dost, sun! Life mein ups and downs toh aate rehte hain! 😊 Tu strong hai, tu kar sakta hai! Main yahan hoon na! 🌟",
                "Hey! Don't worry yaar! 😄 Tough times don't last, tough people do! Tu toh ekdum strong hai! 💪",
                "Arey yaar, tension mat le! 😊 Har problem ka solution hota hai! Tu bas positive rah, sab theek ho jayega! ✨"
            ]
            return random.choice(motivational_responses)
        
        # Default to random response
        return random.choice(responses)
    
    def get_response(self, user_input: str) -> str:
        """
        Get chatbot response based on user input with learning capabilities.
        Now handles Hinglish and mixed language better.
        
        Args:
            user_input (str): User's message
            
        Returns:
            str: Chatbot's response
        """
        if not user_input.strip():
            return "Please say something!"
        
        # Check if input is primarily Hinglish and provide helpful response
        if self._is_hinglish_input(user_input):
            # Try to understand Hinglish input better
            response = self._handle_hinglish_input(user_input)
            if response:
                self._learn_from_conversation(user_input, response)
                return response
        
        # Preprocess user input
        user_tokens = self._preprocess_text(user_input)
        
        if not user_tokens:
            response = random.choice(self.fallback_responses)
            self._learn_from_conversation(user_input, response)
            return response
        
        best_match = None
        best_score = 0.0
        
        # Find the best matching intent
        for intent in self.intents_data:
            for pattern in intent.get('patterns', []):
                pattern_tokens = self._preprocess_text(pattern)
                similarity = self._calculate_similarity(user_tokens, pattern_tokens)
                
                if similarity > best_score:
                    best_score = similarity
                    best_match = intent
        
        # If we have a good match, return a personalized response
        if best_match and best_score > 0.3:  # Threshold for acceptable match
            responses = best_match.get('responses', [])
            if responses:
                response = self._get_personalized_response(best_match.get('tag', ''), responses)
                self._learn_from_conversation(user_input, response)
                return response
        
        # Return fallback response if no good match found
        response = random.choice(self.fallback_responses)
        self._learn_from_conversation(user_input, response)
        return response
    
    def _is_hinglish_input(self, text: str) -> bool:
        """Check if input is primarily Hinglish (Hindi-English mixed)."""
        # Count Hindi and English characters
        hindi_chars = sum(1 for char in text if ord(char) > 127)
        english_chars = sum(1 for char in text if ord(char) <= 127 and char.isalpha())
        
        # If there are both Hindi and English characters, it's likely Hinglish
        return hindi_chars > 0 and english_chars > 0
    
    def _handle_hinglish_input(self, text: str) -> str:
        """Handle Hinglish input with better understanding."""
        text_lower = text.lower()
        
        # Common Hinglish patterns and their responses
        hinglish_patterns = {
            'kaise ho': 'Hey dost! Main toh bilkul badhiya hoon! 😊 Tu bata, tu kaise hai?',
            'kya haal': 'Arey yaar, main toh perfect hoon! 😄 Tu bata, kya haal hai?',
            'sab badhiya': 'Dost, main toh ekdum mast hoon! 😊 Tu bata, sab theek?',
            'kya kar raha': 'Arey dost, main toh bas tumse baat kar raha hoon! 😄 Tu bata, tu kya kar raha hai?',
            'joke sunao': 'Ek joke sun! 😄 Doctor ne patient se pucha: "Aapko kya hua hai?" Patient bola: "Doctor sahab, main toh bas check-up ke liye aaya hoon!" 😂',
            'hasao mujhe': 'Arey yaar, ek joke sun! 😊 Teacher ne pucha: "2+2 kya hota hai?" Student bola: "4!" Teacher: "Perfect!" Student: "Perfect kya hota hai?" 😄',
            'mujhe motivate': 'Arey dost, sun! Life mein ups and downs toh aate rehte hain! 😊 Tu strong hai, tu kar sakta hai! Main yahan hoon na! 🌟',
            'udaas hoon': 'Hey! Don\'t worry yaar! 😄 Tough times don\'t last, tough people do! Tu toh ekdum strong hai! 💪',
            'tension hai': 'Arey yaar, tension mat le! 😊 Har problem ka solution hota hai! Tu bas positive rah, sab theek ho jayega! ✨',
            'shukriya': 'Arey yaar, koi baat nahi! 😊 Dost dost hote hain!',
            'dhanyawad': 'Welcome dost! Koi tension nahi! 😄',
            'alvida': 'Bye dost! Phir milenge! 👋 Khush raho!',
            'phir milenge': 'See you later! Miss karunga! 😊 Jaldi wapas aana!'
        }
        
        # Check for Hinglish patterns
        for pattern, response in hinglish_patterns.items():
            if pattern in text_lower:
                return response
        
        return None
    
    def provide_feedback(self, user_input: str, feedback: str):
        """
        Allow user to provide feedback on bot responses.
        
        Args:
            user_input (str): Original user input
            feedback (str): User feedback (positive/negative)
        """
        self.response_feedback[user_input] = feedback
        self._save_learning_data()
    
    def get_conversation_stats(self) -> Dict[str, Any]:
        """
        Get conversation statistics and learning insights.
        
        Returns:
            Dict[str, Any]: Conversation statistics
        """
        total_conversations = len(self.conversation_history)
        positive_feedback = sum(1 for f in self.response_feedback.values() if "positive" in f.lower())
        negative_feedback = sum(1 for f in self.response_feedback.values() if "negative" in f.lower())
        
        return {
            "total_conversations": total_conversations,
            "user_preferences": self.user_preferences,
            "feedback_stats": {
                "positive": positive_feedback,
                "negative": negative_feedback,
                "total_feedback": len(self.response_feedback)
            },
            "last_updated": self.learning_data.get("last_updated", "Never")
        }
    
    def get_welcome_message(self) -> str:
        """
        Get a welcome message for the chatbot.
        
        Returns:
            str: Welcome message
        """
        welcome_messages = [
            "Hey dost! 😊 Main tumhara AI buddy hoon! Kya haal hai?",
            "Hi yaar! 😄 Main toh bas tumse baat karne ke liye ready hoon! Kya chal raha hai?",
            "Welcome buddy! 😊 Main toh bas tumhara dost hoon! Kya kar sakte hain hum?",
            "Arey, aao aao! 😄 Main toh bas tumse chat karne ke liye hoon! Kya haal hai?"
        ]
        return random.choice(welcome_messages)
    
    def reload_intents(self) -> bool:
        """
        Reload intents from the JSON file.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.intents_data = self._load_intents()
            return True
        except Exception as e:
            print(f"Error reloading intents: {e}")
            return False
    
    def reset_learning(self):
        """Reset all learning data."""
        self.conversation_history = []
        self.user_preferences = {}
        self.response_feedback = {}
        self.learning_data = {
            "conversation_history": [],
            "user_preferences": {},
            "response_feedback": {},
            "learned_patterns": [],
            "custom_responses": {},
            "last_updated": datetime.now().isoformat()
        }
        self._save_learning_data()
