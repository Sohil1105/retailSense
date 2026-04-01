import json
import math

def calculate_revenue(price, quantity, discount_pct=0):
    """
    Returns the final revenue after applying discount.
    Formula: price * quantity * (1 - discount_pct / 100)
    Default discount is 0%.
    """
    if price is None or quantity is None:
        return 0
    return float(price) * float(quantity) * (1 - float(discount_pct) / 100.0)

def classify_customer(age) -> str:
    """
    Returns customer segment as a string:
    - age < 25     → "Youth"
    - 25 <= age < 45 → "Adult"
    - age >= 45    → "Senior"
    - age is None  → "Unknown"
    Use type hints in your function signature.
    """
    if age is None or (isinstance(age, float) and math.isnan(age)):
        return "Unknown"
    
    age = float(age)
    if age < 25:
        return "Youth"
    elif 25 <= age < 45:
        return "Adult"
    else:
        return "Senior"

def is_valid_email(email: str) -> bool:
    """
    Returns True if email contains '@' and '.', else False.
    """
    if not isinstance(email, str):
        return False
    return "@" in email and "." in email

def load_config(filepath: str) -> dict:
    """
    Reads a JSON file and returns it as a Python dictionary.
    Use a context manager (with block).
    """
    with open(filepath, 'r') as f:
        return json.load(f)

def write_summary_report(stats: dict, output_path: str) -> None:
    """
    Writes a plain-text summary report to the given file path.
    Each key-value pair in stats should be on its own line.
    Format: "Key: Value"
    Use a context manager (with block).
    """
    with open(output_path, 'w') as f:
        for key, value in stats.items():
            f.write(f"{key}: {value}\n")

if __name__ == "__main__":
    config = load_config("config.json")
    print(f"Project Name: {config.get('project_name')}")
    print(f"Tax Rate: {config.get('tax_rate')}%")
    
    rev = calculate_revenue(1200, 3, 10)
    print(f"Revenue (1200, 3, 10% discount): {rev}")
    
    segment = classify_customer(None)
    print(f"Customer Segment (None): {segment}")
