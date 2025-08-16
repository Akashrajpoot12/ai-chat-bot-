# AI ChatBot - PyQt5 Application

A modern, messenger-like AI ChatBot application built with Python and PyQt5, featuring a beautiful user interface and basic natural language processing capabilities.

## 🚀 Features

- **Modern UI Design**: Clean, WhatsApp/Telegram-like interface with chat bubbles
- **Responsive Layout**: Adapts to different window sizes
- **Chat Bubbles**: Different styles for user (blue, right-aligned) and bot (gray, left-aligned) messages
- **Timestamps**: Each message shows the time it was sent
- **Smart Responses**: Basic NLP using NLTK for intent recognition
- **Predefined Intents**: Configurable responses for common conversation patterns
- **Fallback Responses**: Handles unknown queries gracefully
- **Smooth Scrolling**: Auto-scrolls to latest messages
- **Keyboard Shortcuts**: Enter to send, Escape to close
- **🤖 Learning Capabilities**: Remembers conversations and learns from user feedback
- **👤 User Preferences**: Learns what you like (jokes, motivation, etc.)
- **📊 Feedback System**: Use 👍/👎 buttons to rate bot responses
- **🔄 Continuous Improvement**: Gets smarter with each conversation
- **💾 Persistent Learning**: Saves learning data between sessions

## 📋 Requirements

- Python 3.7+
- PyQt5
- NLTK (Natural Language Toolkit)

## 🛠️ Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Download NLTK data** (first time only):
   ```python
   import nltk
   nltk.download('punkt')
   nltk.download('stopwords')
   ```

## 🚀 Usage

### Running the Application

```bash
python chatbot_ui.py
```

### How to Use

1. **Start the app**: Run the main script
2. **Type messages**: Use the input field at the bottom
3. **Send messages**: Press Enter or click the Send button
4. **View responses**: Bot responses appear as chat bubbles
5. **Close app**: Press Escape or use the window close button

### Example Conversations

- **Greetings**: "Hello", "Hi", "Hey"
- **Help**: "What can you do?", "Help"
- **Jokes**: "Tell me a joke", "Make me laugh"
- **Goodbye**: "Bye", "See you later"

## 📁 Project Structure

```
ai-chatbot/
├── chatbot_ui.py          # Main PyQt5 UI application
├── chatbot_logic.py       # Chatbot logic and NLP processing
├── intents.json           # Intent patterns and responses
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🔧 Customization

### Adding New Intents

Edit `intents.json` to add new conversation patterns:

```json
{
  "tag": "custom_intent",
  "patterns": ["pattern1", "pattern2"],
  "responses": ["response1", "response2"]
}
```

### Modifying UI Styles

Edit the `setStyleSheet()` calls in `chatbot_ui.py` to customize:
- Colors
- Fonts
- Borders
- Spacing

### Extending Chatbot Logic

Modify `chatbot_logic.py` to:
- Add more sophisticated NLP
- Integrate with external APIs
- Implement machine learning models

## 🎨 UI Components

- **Header**: Blue bar with title and online status
- **Chat Area**: Scrollable message display with bubbles
- **Input Area**: Text field and send button
- **Message Bubbles**: Rounded corners, different colors for user/bot
- **Scrollbar**: Custom-styled vertical scrollbar

## 🔍 Technical Details

### NLP Implementation
- **Tokenization**: Uses NLTK's word_tokenize
- **Stop Words**: Removes common words for better matching
- **Similarity Scoring**: Calculates pattern matching scores
- **Intent Recognition**: Finds best matching intent based on similarity

### PyQt5 Features
- **Custom Widgets**: MessageBubble, ChatArea, InputArea
- **Layout Management**: QVBoxLayout, QHBoxLayout
- **Styling**: CSS-like stylesheets
- **Event Handling**: Signal-slot connections

### 🤖 Learning System
- **Conversation Memory**: Stores all conversations with timestamps
- **User Preference Tracking**: Learns user likes/dislikes automatically
- **Feedback Integration**: Collects user ratings on responses
- **Personalized Responses**: Adapts responses based on learned preferences
- **Data Persistence**: Saves learning data to JSON files
- **Statistics Dashboard**: Shows learning progress and insights

## 🐛 Troubleshooting

### Common Issues

1. **Import Error**: Ensure all dependencies are installed
2. **NLTK Data Missing**: Download required NLTK data
3. **UI Not Displaying**: Check PyQt5 installation
4. **Responses Not Working**: Verify intents.json file exists

### Debug Mode

Add debug prints in `chatbot_logic.py`:
```python
print(f"User input: {user_input}")
print(f"Best match: {best_match}")
print(f"Similarity score: {best_score}")
```

## 🚀 Future Enhancements

- **Voice Input/Output**: Speech recognition and synthesis
- **File Sharing**: Support for images and documents
- **User Authentication**: Login system
- **Chat History**: Persistent message storage
- **Multi-language Support**: Internationalization
- **Advanced NLP**: Integration with GPT or other LLMs
- **Themes**: Dark/light mode and custom themes



## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.



**Enjoy chatting with your AI assistant! 🤖💬**

