import logging

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from backend.domain.exception import (  # adapt to your path
    AlreadyExistException,
    NotFoundException,
    UnAuthorizedException,
    ValidationException,
)

logger = logging.getLogger(__name__)


def _body(code: str, message: str) -> dict[str, str]:
    return {"code": code, "message": message}


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(ValidationException)
    async def _validation(_: Request, exc: ValidationException) -> JSONResponse:
        return JSONResponse(_body(exc.keyError, exc.message), status.HTTP_422_UNPROCESSABLE_ENTITY)

    @app.exception_handler(UnAuthorizedException)
    async def _unauthorized(_: Request, exc: UnAuthorizedException) -> JSONResponse:
        return JSONResponse(_body(exc.keyError, exc.message), status.HTTP_401_UNAUTHORIZED)

    @app.exception_handler(NotFoundException)
    async def _not_found(_: Request, exc: NotFoundException) -> JSONResponse:
        return JSONResponse(_body(exc.keyError, exc.message), status.HTTP_404_NOT_FOUND)

    @app.exception_handler(AlreadyExistException)
    async def _already_exist(_: Request, exc: AlreadyExistException) -> JSONResponse:
        return JSONResponse(_body(exc.keyError, exc.message), status.HTTP_409_CONFLICT)

    @app.exception_handler(Exception)
    async def _unexpected(_: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unhandled error", exc_info=exc)
        # Never leak internal details (SQL errors, etc.) to the client
        return JSONResponse(
            _body("INTERNAL_ERROR", "Internal server error"),
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )