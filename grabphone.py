import re

def extract_phone_numbers(text):
    # Updated regular expression:
    # \+? - optionally matches a leading "+"
    # \(?\d{1,3}\)? - optionally matches area code in parentheses
    # [\d\s\-\.\(\)]{6,15} - matches the remaining part of the number, allowing common delimiters
    phone_pattern = r"(\+?\(?\d{1,3}\)?[\d\s\-\.\(\)]{7,15})"
    
    # Find all matches based on the pattern
    matches = re.findall(phone_pattern, text)
    
    # Clean up each phone number to only include digits, brackets, and plus sign
    cleaned_numbers = [''.join(re.findall(r'[\d\(\)\+]', match)) for match in matches]
    
    # Join the cleaned numbers with ";"
    return ";".join(cleaned_numbers)

# Example usage
if __name__ == "__main__":
    text = "Contact me at +1 (555) 123-4567, 0039 02 1234 5678. Office number is (987) 654-3210."
    print(extract_phone_numbers(text))
