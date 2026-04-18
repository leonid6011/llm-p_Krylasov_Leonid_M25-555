class AppError(Exception):
    """Base application error."""


class ConflictError(AppError):
    """Resource already exists (e.g. email taken)."""


class UnauthorizedError(AppError):
    """Invalid credentials."""


class ForbiddenError(AppError):
    """Access denied."""


class NotFoundError(AppError):
    """Resource not found."""


class ExternalServiceError(AppError):
    """External service (OpenRouter) returned an error."""
