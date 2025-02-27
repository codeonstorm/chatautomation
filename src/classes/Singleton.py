class Singleton:
    _instance = None  # Stores the single instance

    def __new__(cls, *args, **kwargs):  # cls refers to the class itself
        if cls._instance is None:
            cls._instance = super().__new__(cls)  # Create a new instance
        return cls._instance  # Return the existing instance

    def __init__(self, value):
        if not hasattr(self, "value"):  # Only set once
            self.value = value

# Example
obj1 = Singleton("First")
obj2 = Singleton("Second")

print(obj1 is obj2)  # True (Same instance)
print(obj1.value)    # "First" (obj2 didn't overwrite it)
print(obj2.value)    # "First"
