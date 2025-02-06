# Function to clean text by removing unnecessary surrounding quotes
def clean_text(text):
    text = text.strip()

    # Remove surrounding quotes *only* if the entire string is quoted
    if (text.startswith('"') and text.endswith('"')) or (text.startswith("'") and text.endswith("'")):
        text = text[1:-1].strip()

    return text

# Test with some raw strings
test_strings = [
    '"This is a test with double quotes"',
    "'This is a test with single quotes'",
    'No quotes here',
    '"Another test with quotes"',
    "'And another one with single quotes'"
]

# Apply clean_text and print results
for test_str in test_strings:
    cleaned = clean_text(test_str)
    print(f"Original: {test_str} => Cleaned: {cleaned}")
