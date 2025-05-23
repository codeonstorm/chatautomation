import re

class RegexNERExtractor:
    @staticmethod
    def get_patterns():
        """
        Returns a dictionary of entity types and their regex patterns.
        Extend this method to add more entities.
        """
        return {
            'email': r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b',
            'mobile': r'\b(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?){1,2}\d{4}\b'
        }

    @staticmethod
    def extract_entities(text, patterns=None):
        """
        Extract entities from text using regex patterns.
        :param text: str, input text
        :param patterns: dict, entity name to regex pattern (optional)
        :return: dict, entity name to list of extracted values or None if no match
        """
        if patterns is None:
            patterns = RegexNERExtractor.get_patterns()
        results = {}
        for entity, pattern in patterns.items():
            matches = re.findall(pattern, text)
            results[entity] = matches if matches else None
        return results

# Example usage:
if __name__ == "__main__":
    sample_text = """
    Contact us at support@example.com or sales@company.org.
    You can also reach us at +1-800-555-1212 or (123) 456-7890.
    """
    extracted = RegexNERExtractor.extract_entities(sample_text)
    print("Extracted Entities:")
    for entity, values in extracted.items():
        print(f"{entity.capitalize()}: {values}")
