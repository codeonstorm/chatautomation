class ChatHistory:
    # Class-level storage for all chat histories
    _histories = {}
    _max_history_length = 3

    @classmethod
    def init_history(cls, chatbot_uuid, session_uuid):
        """Initialize a new chat history for a specific chatbot and session."""
        key = chatbot_uuid + session_uuid
        cls._histories[key] = []
        return key

    @classmethod
    def add_message(cls, key: str, role: str, content: str):
        """Add a new message to the chat history."""
        if key not in cls._histories:
            return

        message = {
            "role": role,
            "content": content,
        }
        cls._histories[key].append(message)

        # Trim history if it exceeds max length
        if len(cls._histories[key]) > cls._max_history_length:
            cls._histories[key] = cls._histories[key][-cls._max_history_length :]

    @classmethod
    def get_history(cls, key: str):
        """Return the full chat history."""
        return cls._histories.get(key, [])

    @classmethod
    def clear_history(cls, key: str):
        """Clear the chat history."""
        if key in cls._histories:
            cls._histories[key] = []

    @classmethod
    def get_last_n_messages(cls, key: str, n: int):
        """Get the last n messages from the chat history."""
        history = cls._histories.get(key, [])
        return history[-n:] if n > 0 else []

    @classmethod
    def format_for_prompt(cls, key: str):
        """Format the chat history for use in an LLM prompt."""
        history = cls._histories.get(key, [])
        return [{"role": msg["role"], "content": msg["content"]} for msg in history]
