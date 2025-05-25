import re
import spacy


class SynonymNERExtractor:
    def __init__(self, canonical_synonyms):
        self.canonical_synonyms = canonical_synonyms
        self.inverse_map = {}
        self.patterns = {}
        self._build_mappings()

    def _build_mappings(self):
        """
        Build the inverse mapping from synonym to canonical name
        and compile regex patterns for each slot category.
        """
        for slot, canon_map in self.canonical_synonyms.items():
            slot_synonyms = []
            for canonical, synonyms in canon_map.items():
                for synonym in synonyms:
                    key = synonym.lower()
                    self.inverse_map[key] = canonical
                    slot_synonyms.append(re.escape(synonym))
            # Sort by length to prioritize longest match first
            slot_synonyms.sort(key=len, reverse=True)
            pattern = r"\b(" + "|".join(slot_synonyms) + r")\b"
            self.patterns[slot] = re.compile(pattern, flags=re.IGNORECASE)

    def extract_entities(self, text):
        """
        Extract entities from input text based on synonyms.
        Returns a dict: {slot: [list of canonical matches] or None}
        """
        slots = {slot: [] for slot in self.canonical_synonyms}
        for slot, pattern in self.patterns.items():
            matches = pattern.findall(text)
            for match in matches:
                canonical = self.inverse_map.get(match.lower(), match)
                if canonical not in slots[slot]:
                    slots[slot].append(canonical)
        # Convert empty lists to None
        return {k: (v if v else None) for k, v in slots.items()}


if __name__ == "__main__":
    # Load spaCy model if you want (not used directly here but you had it)
    nlp = spacy.load("en_core_web_sm")

    CANONICAL_SYNONYMS = {
        "origin": {
            "New York": ["nyc", "new york", "new-york"],
            "London": ["lhr", "london"],
        },
        "destination": {
            "San Francisco": ["sfo", "sf", "san francisco", "san-francisco"],
            "Paris": ["cdg", "paris"],
        },
        "food": {
            "Pizza": ["pizza", "Pizza"],
            "Burger": ["burger", "Burger"],
            "Sushi": ["sushi", "Sushi"],
            "Pasta": ["pasta", "Pasta"],
        },
        "animal": {
            "Dog": ["dog", "Dog"],
            "Cat": ["cat", "Cat"],
            "Elephant": ["elephant", "Elephant"],
            "Tiger": ["tiger", "Tiger"],
        },
        "bank": {
            "Wells Fargo": ["wells fargo", "Wells Fargo"],
            "JPMorgan Chase": ["chase", "Chase"],
            "Bank of America": ["boa", "Bank of America"],
            "Citibank": ["citibank", "Citibank"],
        },
        "flower": {
            "Rose": ["rose", "Rose"],
            "Tulip": ["tulip", "Tulip"],
            "Orchid": ["orchid", "Orchid"],
            "Daisy": ["daisy", "Daisy"],
        },
        "software": {
            "Adobe Photoshop": ["photoshop", "Photoshop"],
            "Visual Studio Code": ["vscode", "VSCode"],
            "Slack": ["slack", "Slack"],
            "Docker": ["docker", "Docker"],
        },
        "technology": {
            "Artificial Intelligence": ["ai", "AI"],
            "Machine Learning": ["ml", "ML"],
            "Blockchain": ["blockchain", "Blockchain"],
            "Internet of Things": ["iot", "IoT"],
        },
        "course": {
            "CS101 Introduction to Computer Science": ["cs101", "CS101"],
            "Math201 Calculus II": ["math201", "MATH201"],
            "ENG301 Advanced English Literature": ["eng301", "ENG301"],
            "HIST210 World History": ["hist210", "HIST210"],
        },
        "book": {
            "The Hobbit": ["hobbit", "The Hobbit"],
            "Dune": ["dune", "Dune"],
            "The Great Gatsby": ["gatsby", "The Great Gatsby"],
            "Harry Potter and the Sorcerer’s Stone": ["harry potter", "Harry Potter"],
        },
    }

    ner_extractor = SynonymNERExtractor(CANONICAL_SYNONYMS)

    examples = [
        "Book a flight from NYC to sanFranciscO",
        "I’m flying from new york to san Francisco next week",
        "Flight orig: LHR dest: CDG",
        "I want pizza and sushi",
        "She adopted a Dog and a cat",
        "Transfer money from Chase to BANK OF AMERICA",
        "He picked roses and tulip",
        "Let's code with vscode and docker",
        "We love AI and ML in IoT courses",
        "Enrolled in CS101 and ENG301",
        "Reading The Hobbit and gatsby",
    ]

    for sent in examples:
        print(f"Input: {sent}\nOutput: {ner_extractor.extract_entities(sent)}\n")
