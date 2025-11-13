from app.exceptions.base import TodolistError

class NotFoundError(TodolistError):
    """Raised when an item (project or task) is not found."""
    pass

class DuplicateError(TodolistError):
    """Raised when trying to create an item that already exists (e.g., duplicate project name)."""
    pass