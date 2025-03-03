import re

def convert_suffixed_value(value_str):
    # Match the numeric part and the suffix (case-insensitive)
    match = re.match(r"^([0-9]*\.?[0-9]+)([KMB]?)$", value_str, re.IGNORECASE)
    if not match:
        return value_str  # Return original if format doesn't match
    
    num_str, suffix = match.groups()
    suffix = suffix.upper()  # Ensure suffix is uppercase
    
    # Define multiplier factors for each suffix
    factors = {'K': 1e3, 'M': 1e6, 'B': 1e9}
    factor = factors.get(suffix, 1)  # Default to 1 if no suffix
    
    # Calculate the numeric value
    try:
        num = float(num_str) * factor
    except ValueError:
        return value_str  # Fallback if conversion fails
    
    # Convert to integer if no decimal part
    if num.is_integer():
        num = int(num)
    
    return str(num)

# Example usage
# print(convert_suffixed_value("1.2K"))  # Output: "1200"