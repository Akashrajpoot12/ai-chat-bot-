import sys
import json
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QScrollArea, QLabel,
    QFrame, QSizePolicy, QSpacerItem
)
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QPalette, QColor, QTextCursor, QPixmap, QIcon
from chatbot_logic import ChatbotLogic

class MessageBubble(QFrame):
    """
    Custom message bubble widget for chat messages.
    Supports different styles for user and bot messages.
    Now includes feedback buttons for bot messages.
    """
    
    def __init__(self, text: str, is_user: bool = False, timestamp: str = None, parent=None, on_feedback=None):
        super().__init__(parent)
        self.is_user = is_user
        self.text = text
        self.timestamp = timestamp or datetime.now().strftime("%H:%M")
        self.on_feedback = on_feedback
        
        self.setup_ui()
        self.apply_styling()
    
    def setup_ui(self):
        """Setup the message bubble UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(4)
        
        # Message text
        self.text_label = QLabel(self.text)
        self.text_label.setWordWrap(True)
        self.text_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.text_label.setStyleSheet("color: inherit; background: transparent; border: none;")
        
        # Timestamp
        self.time_label = QLabel(self.timestamp)
        self.time_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.time_label.setStyleSheet("color: inherit; background: transparent; border: none; font-size: 10px; opacity: 0.7;")
        
        layout.addWidget(self.text_label)
        layout.addWidget(self.time_label)
        
        # Add feedback buttons for bot messages
        if not self.is_user and self.on_feedback:
            self.setup_feedback_buttons(layout)
        
        # Set size policy
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.setMaximumWidth(400)
    
    def setup_feedback_buttons(self, layout):
        """Setup feedback buttons for bot messages."""
        feedback_layout = QHBoxLayout()
        feedback_layout.setSpacing(5)
        
        # Thumbs up button
        self.thumbs_up_btn = QPushButton("👍")
        self.thumbs_up_btn.setFixedSize(24, 24)
        self.thumbs_up_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                font-size: 14px;
                color: #4CAF50;
            }
            QPushButton:hover {
                background-color: rgba(76, 175, 80, 0.1);
                border-radius: 12px;
            }
        """)
        self.thumbs_up_btn.clicked.connect(lambda: self.on_feedback("positive"))
        
        # Thumbs down button
        self.thumbs_down_btn = QPushButton("👎")
        self.thumbs_down_btn.setFixedSize(24, 24)
        self.thumbs_down_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                font-size: 14px;
                color: #F44336;
            }
            QPushButton:hover {
                background-color: rgba(244, 67, 54, 0.1);
                border-radius: 12px;
            }
        """)
        self.thumbs_down_btn.clicked.connect(lambda: self.on_feedback("negative"))
        
        feedback_layout.addWidget(self.thumbs_up_btn)
        feedback_layout.addWidget(self.thumbs_down_btn)
        feedback_layout.addStretch()
        
        layout.addLayout(feedback_layout)
    
    def apply_styling(self):
        """Apply styling based on message type (user or bot)."""
        if self.is_user:
            # User message styling (right-aligned, blue background)
            self.setStyleSheet("""
                QFrame {
                    background-color: #0084ff;
                    color: white;
                    border-radius: 18px;
                    border-top-right-radius: 4px;
                    margin-left: 50px;
                    margin-right: 5px;
                }
            """)
            # Set layout alignment for right-aligned user messages
            self.layout().setAlignment(Qt.AlignRight)
        else:
            # Bot message styling (left-aligned, light gray background)
            self.setStyleSheet("""
                QFrame {
                    background-color: #f0f0f0;
                    color: #333333;
                    border-radius: 18px;
                    border-top-left-radius: 4px;
                    margin-right: 50px;
                    margin-left: 5px;
                }
            """)
            # Set layout alignment for left-aligned bot messages
            self.layout().setAlignment(Qt.AlignLeft)

class ChatArea(QWidget):
    """
    Scrollable chat area that displays message bubbles.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the chat area UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        # Add spacer to push messages to bottom
        self.spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(self.spacer)
        
        # Set background
        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                border: none;
            }
        """)
    
    def add_message(self, text: str, is_user: bool = False, timestamp: str = None, on_feedback=None):
        """Add a new message bubble to the chat area."""
        # Remove spacer temporarily
        self.layout().removeItem(self.spacer)
        
        # Create and add message bubble
        bubble = MessageBubble(text, is_user, timestamp, self, on_feedback)
        self.layout().addWidget(bubble)
        
        # Re-add spacer
        self.layout().addItem(self.spacer)
        
        # Scroll to bottom
        self.scroll_to_bottom()
        
        return bubble
    
    def scroll_to_bottom(self):
        """Scroll the chat area to the bottom."""
        # Find the parent scroll area and scroll to bottom
        parent = self.parent()
        while parent and not isinstance(parent, QScrollArea):
            parent = parent.parent()
        
        if parent:
            parent.verticalScrollBar().setValue(parent.verticalScrollBar().maximum())

class InputArea(QWidget):
    """
    Input area with text field and send button.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the input area UI."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 15)
        layout.setSpacing(10)
        
        # Text input field
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Type your message here...")
        self.text_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #e1e1e1;
                border-radius: 20px;
                padding: 10px 15px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #0084ff;
            }
        """)
        
        # Send button
        self.send_button = QPushButton("Send")
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #0084ff;
                color: white;
                border: none;
                border-radius: 20px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0073e6;
            }
            QPushButton:pressed {
                background-color: #005bb5;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        
        # Set fixed height for consistent appearance
        self.text_input.setFixedHeight(40)
        self.send_button.setFixedHeight(40)
        
        layout.addWidget(self.text_input)
        layout.addWidget(self.send_button)
        
        # Set background
        self.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                border-top: 1px solid #e1e1e1;
            }
        """)

class AI_ChatBot(QMainWindow):
    """
    Main AI ChatBot application window with modern messenger-like interface.
    """
    
    def __init__(self):
        super().__init__()
        self.chatbot = ChatbotLogic()
        self.setup_ui()
        self.setup_connections()
        self.show_welcome_message()
    
    def setup_ui(self):
        """Setup the main application UI."""
        self.setWindowTitle("AI ChatBot - Learning Edition")
        self.setMinimumSize(800, 600)
        self.resize(900, 700)
        
        # Set window icon (optional)
        # self.setWindowIcon(QIcon("icon.png"))
        
        # Setup menu bar
        self.setup_menu_bar()
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header
        self.setup_header(main_layout)
        
        # Chat area with scroll
        self.setup_chat_area(main_layout)
        
        # Input area
        self.input_area = InputArea()
        main_layout.addWidget(self.input_area)
        
        # Apply main window styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ffffff;
            }
        """)
    
    def setup_menu_bar(self):
        """Setup the application menu bar with learning options."""
        menubar = self.menuBar()
        
        # Learning menu
        learning_menu = menubar.addMenu('🤖 Learning')
        
        # Show statistics action
        stats_action = learning_menu.addAction('📊 Show Statistics')
        stats_action.triggered.connect(self.show_learning_stats)
        
        # Reset learning action
        reset_action = learning_menu.addAction('🔄 Reset Learning')
        reset_action.triggered.connect(self.reset_learning)
        
        # Separator
        learning_menu.addSeparator()
        
        # About action
        about_action = learning_menu.addAction('ℹ️ About Learning')
        about_action.triggered.connect(self.show_learning_info)
    
    def setup_header(self, parent_layout):
        """Setup the application header."""
        header = QWidget()
        header.setFixedHeight(60)
        header.setStyleSheet("""
            QWidget {
                background-color: #0084ff;
                color: white;
                border: none;
            }
        """)
        
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 0, 20, 0)
        
        # Title
        title_label = QLabel("AI ChatBot")
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 20px;
                font-weight: bold;
                background: transparent;
                border: none;
            }
        """)
        
        # Status indicator
        status_label = QLabel("● Online")
        status_label.setStyleSheet("""
            QLabel {
                color: #90EE90;
                font-size: 12px;
                background: transparent;
                border: none;
            }
        """)
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(status_label)
        
        parent_layout.addWidget(header)
    
    def setup_chat_area(self, parent_layout):
        """Setup the scrollable chat area."""
        # Create scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Style the scroll area
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #ffffff;
            }
            QScrollBar:vertical {
                background-color: #f0f0f0;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #c0c0c0;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #a0a0a0;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        # Create chat area widget
        self.chat_area = ChatArea()
        self.scroll_area.setWidget(self.chat_area)
        
        parent_layout.addWidget(self.scroll_area)
    
    def setup_connections(self):
        """Setup signal connections."""
        # Connect send button
        self.input_area.send_button.clicked.connect(self.send_message)
        
        # Connect enter key in text input
        self.input_area.text_input.returnPressed.connect(self.send_message)
        
        # Connect text changed to enable/disable send button
        self.input_area.text_input.textChanged.connect(self.on_text_changed)
    
    def on_text_changed(self, text):
        """Handle text input changes."""
        # Enable/disable send button based on text content
        self.input_area.send_button.setEnabled(bool(text.strip()))
    
    def send_message(self):
        """Send the current message."""
        text = self.input_area.text_input.text().strip()
        if not text:
            return
        
        # Store last user message for feedback
        self.last_user_message = text
        
        # Add user message to chat
        self.add_user_message(text)
        
        # Clear input field
        self.input_area.text_input.clear()
        
        # Get bot response
        self.get_bot_response(text)
    
    def add_user_message(self, text: str):
        """Add a user message to the chat."""
        self.chat_area.add_message(text, is_user=True)
    
    def add_bot_message(self, text: str):
        """Add a bot message to the chat."""
        self.chat_area.add_message(text, is_user=False, on_feedback=self.handle_feedback)
    
    def handle_feedback(self, feedback_type: str):
        """Handle user feedback on bot responses."""
        if hasattr(self, 'last_user_message') and hasattr(self, 'last_bot_response'):
            self.chatbot.provide_feedback(self.last_user_message, feedback_type)
            print(f"Feedback recorded: {feedback_type} for response to '{self.last_user_message}'")
    
    def show_learning_stats(self):
        """Show learning statistics and insights."""
        stats = self.chatbot.get_conversation_stats()
        
        stats_text = f"""
🤖 ChatBot Learning Statistics:

📊 Total Conversations: {stats['total_conversations']}
👍 Positive Feedback: {stats['feedback_stats']['positive']}
👎 Negative Feedback: {stats['feedback_stats']['negative']}
📝 Total Feedback: {stats['feedback_stats']['total_feedback']}

👤 User Preferences:
"""
        
        for pref, count in stats['user_preferences'].items():
            if pref == "likes_jokes":
                stats_text += f"• Loves Jokes: {count} times\n"
            elif pref == "needs_motivation":
                stats_text += f"• Needs Motivation: {count} times\n"
            else:
                stats_text += f"• {pref}: {count} times\n"
        
        stats_text += f"\n🕒 Last Updated: {stats['last_updated']}"
        
        # Show stats in a simple message box
        from PyQt5.QtWidgets import QMessageBox
        msg = QMessageBox()
        msg.setWindowTitle("Learning Statistics")
        msg.setText(stats_text)
        msg.exec_()
    
    def reset_learning(self):
        """Reset all learning data."""
        from PyQt5.QtWidgets import QMessageBox
        reply = QMessageBox.question(self, 'Reset Learning', 
                                   'Are you sure you want to reset all learning data? This cannot be undone.',
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.chatbot.reset_learning()
            QMessageBox.information(self, 'Learning Reset', 'All learning data has been reset successfully!')
    
    def show_learning_info(self):
        """Show information about the learning capabilities."""
        info_text = """
🤖 AI ChatBot Learning Features:

✨ **Conversation Memory**: Remembers all your conversations
👤 **User Preferences**: Learns what you like (jokes, motivation, etc.)
📊 **Feedback System**: Use 👍/👎 buttons to rate responses
🔄 **Continuous Improvement**: Gets better with each conversation
💾 **Persistent Learning**: Saves data between sessions

🎯 **How to Use**:
• Chat normally with the bot
• Use 👍/👎 buttons on bot responses
• Check statistics in Learning menu
• Reset learning if needed

The more you chat and provide feedback, the smarter the bot becomes! 🚀
"""
        
        from PyQt5.QtWidgets import QMessageBox
        msg = QMessageBox()
        msg.setWindowTitle("About Learning Features")
        msg.setText(info_text)
        msg.exec_()
    
    def get_bot_response(self, user_message: str):
        """Get and display bot response."""
        # Simulate typing delay for more natural feel
        QTimer.singleShot(500, lambda: self.display_bot_response(user_message))
    
    def display_bot_response(self, user_message: str):
        """Display the bot's response."""
        response = self.chatbot.get_response(user_message)
        self.last_bot_response = response
        self.add_bot_message(response)
    
    def show_welcome_message(self):
        """Show welcome message when app starts."""
        welcome_msg = self.chatbot.get_welcome_message()
        QTimer.singleShot(100, lambda: self.add_bot_message(welcome_msg))
    
    def keyPressEvent(self, event):
        """Handle key press events."""
        if event.key() == Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)

def main():
    """Main application entry point."""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("AI ChatBot")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("AI ChatBot")
    
    # Create and show main window
    window = AI_ChatBot()
    window.show()
    
    # Start the application event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
