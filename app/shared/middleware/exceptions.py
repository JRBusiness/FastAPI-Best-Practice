import logging

from fastapi import HTTPException, status
from loguru import logger

from app.shared.middleware import restart_app


class ServiceNotAvailable(HTTPException):
    pass


class MismatchingServiceAccount(HTTPException):
    pass


class ImproperInputException(ValueError):
    pass


class ExternalApiException(Exception):
    pass


class ValidationError(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = ("Invalid input.",)

    def __init__(self, detail=None):
        if detail:
            logger.error(detail)
            self.detail = detail
        super().__init__(status_code=self.status_code, detail=self.detail)


class AuthenticationFailed(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = ("Incorrect authentication credentials.",)

    def __init__(self, detail=None):
        if detail:
            logger.error(detail)
            self.detail = detail
        super().__init__(status_code=self.status_code, detail=self.detail)


class PermissionDenied(HTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = ("You do not have permission to perform this action.",)

    def __init__(self, detail=None):
        if detail:
            logger.error(detail)
            self.detail = detail
        super().__init__(status_code=self.status_code, detail=self.detail)


class NotFound(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = ("Not found.",)

    def __init__(self, detail=None):
        if detail:
            logger.error(detail)
            self.detail = detail
        print(self.detail)
        super().__init__(status_code=self.status_code, detail=self.detail)


class Throttled(HTTPException):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    detail = ("Request was throttled.",)

    def __init__(self, detail=None):
        if detail:
            logger.error(detail)
            self.detail = detail
        super().__init__(status_code=self.status_code, detail=self.detail)


class InternalServerError(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ("Internal service error.",)

    def __init__(self, detail=None):
        if detail:
            logger.error(detail)
            self.detail = detail
        super().__init__(status_code=self.status_code, detail=self.detail)


class processing(HTTPException):
    detail = ("Still processing request.",)

    def __init__(self, detail=None):
        if detail:
            print(
                f"I think i deperecated this a long time ago, this is my code: {detail}"
            )
            self.detail = detail
        print(self.detail)
        super().__init__(status_code=202, detail=self.detail)


class MisconfigurationError(Exception):
    pass


class ExceptionCounter:
    count = 0
    max_exceptions = 3

    @classmethod
    def increment(cls):
        cls.count += 1
        if cls.count >= cls.max_exceptions:
            cls.restart_app()

    @staticmethod
    def restart_app():
        logging.warning("Restarting app due to multiple exceptions.")
        # Restart the app (use the appropriate command for your application)
        restart_app()
