class TodolistError(Exception):
    """Base exception class for the todolist application."""
    pass

class ValidationError(TodolistError):
    """Raised for validation errors, like character limits or invalid values."""
    pass

class DuplicateError(TodolistError):
    """Raised when trying to create an item that already exists (e.g., duplicate project name)."""
    pass

class NotFoundError(TodolistError):
    """Raised when an item (project or task) is not found."""
    pass