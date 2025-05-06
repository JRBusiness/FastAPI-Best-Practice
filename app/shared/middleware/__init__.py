from fastapi.exception_handlers import http_exception_handler
from app.shared.middleware.exceptions import (
    ValidationError,
    AuthenticationFailed,
    PermissionDenied,
    NotFound,
    Throttled,
    InternalServerError,
)


def include_middleware(api_app):
    api_app.add_exception_handler(ValidationError, http_exception_handler)
    api_app.add_exception_handler(AuthenticationFailed, http_exception_handler)
    api_app.add_exception_handler(PermissionDenied, http_exception_handler)
    api_app.add_exception_handler(NotFound, http_exception_handler)
    api_app.add_exception_handler(Throttled, http_exception_handler)
    api_app.add_exception_handler(InternalServerError, http_exception_handler)
