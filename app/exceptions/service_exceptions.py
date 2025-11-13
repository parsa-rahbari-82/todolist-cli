from app.exceptions.base import TodolistError

class ValidationError(TodolistError):
    """Raised for validation errors, like character limits or invalid values."""
    pass

class LimitExceededError(TodolistError):
    """Raised when an action would exceed a configured limit (e.g., max projects)."""
    pass