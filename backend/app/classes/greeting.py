import re

class GreetingResponder:
    def __init__(self):
        self.responses = {
            "hi": "Hello! 👋",
            "hello": "Hi there! 😊",
            "hey": "Hey! How can I help?",
            "good morning": "Good morning! ☀️",
            "good afternoon": "Good afternoon! 🌤️",
            "good evening": "Good evening! 🌙",
            "greetings": "Greetings!",
            "what's up": "Not much! How can I assist?",
            "thank you": "You're welcome! 😊",
            "thanks": "No problem at all! 👍",
            "thx": "Anytime!",
            "much appreciated": "Glad to help!",
            "cheers": "You're very welcome! 🥂",
            "bye": "Goodbye! 👋",
            "goodbye": "See you later!",
            "see ya": "Take care! ✌️",
            "catch you later": "Later!",
            "have a nice day": "You too! 😊",
            "talk to you later": "I'll be here when you need me!",
            "ok": "Glad to help!"
        }

    def check_greeting(self, user_input: str) -> str | None:
        normalized = user_input.lower().strip()
        
        # Remove common punctuation for matching
        normalized_clean = re.sub(r'[^\w\s]', '', normalized)
        
        # Only reply if the full input is close to a known greeting
        for key in self.responses:
            if normalized_clean == key or normalized_clean in [f"{key}", f"{key}!", f"{key}."]:
                return self.responses[key]
        
        return None
