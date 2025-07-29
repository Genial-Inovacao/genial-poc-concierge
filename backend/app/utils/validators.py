import re
from typing import Optional


def validate_password_strength(password: str) -> tuple[bool, Optional[str]]:
    """
    Validate password strength.
    
    Requirements:
    - At least 8 characters long
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one digit
    - Contains at least one special character
    
    Args:
        password: Password to validate
        
    Returns:
        tuple[bool, Optional[str]]: (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r"\d", password):
        return False, "Password must contain at least one digit"
    
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character"
    
    return True, None


def validate_username(username: str) -> tuple[bool, Optional[str]]:
    """
    Validate username format.
    
    Requirements:
    - 3-20 characters long
    - Only alphanumeric characters and underscores
    - Cannot start with a number
    
    Args:
        username: Username to validate
        
    Returns:
        tuple[bool, Optional[str]]: (is_valid, error_message)
    """
    if len(username) < 3 or len(username) > 20:
        return False, "Username must be between 3 and 20 characters"
    
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9_]*$", username):
        return False, "Username must start with a letter and contain only letters, numbers, and underscores"
    
    return True, None


def sanitize_input(text: str) -> str:
    """
    Sanitize user input to prevent XSS and injection attacks.
    
    Args:
        text: Text to sanitize
        
    Returns:
        str: Sanitized text
    """
    # Handle None or empty strings
    if not text:
        return ""
    
    # Convert to string if needed
    text = str(text)
    
    # Remove any HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Escape special characters
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    text = text.replace("'", '&#x27;')
    
    return text.strip()