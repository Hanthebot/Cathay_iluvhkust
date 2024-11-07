import re

def validate(digits):
    """ check digit validity """
    if len(digits) < 11:
        return False
    return int(digits[3:10]) % 7 == int(digits[-1])

def make_dash_separated(digits):
    """ make dash-separated string """
    return '-'.join([digits[:3], digits[3:10], digits[10]])

def extract_11_digit_number(text):
    """Extracts an 11-digit number ending with 0-6 from the given text, considering possible separators."""
    pattern = r'\b(?:\d[\s.,-]*){10}[0-6]\b'
    match = re.search(pattern, text)
    if match:
        digits = re.sub(r'[\s.,-]', '', match.group())
        return digits
    return None