class ChatBot:
  def __init__(self, name):
    self.name = name
    self.state = {}
    self.history = []

  def set_state(self, key, value):
    self.state[key] = value

  def get_state(self, key):
    return self.state.get(key, None)

  def add_to_history(self, message):
    self.history.append(message)

  def get_history(self):
    return self.history

  def clear_history(self):
    self.history = []

  def respond(self, message):
    # Basic response logic (to be expanded)
    response = f"{self.name} received: {message}"
    self.add_to_history({"user": message, "bot": response})
    return response