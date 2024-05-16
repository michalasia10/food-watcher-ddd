from http import HTTPStatus

from fastapi.responses import JSONResponse


class ErrorResponse(JSONResponse):
    def __init__(self, status_code: HTTPStatus, message: str):
        super().__init__(
            status_code=status_code,
            content=dict(
                error=message,
                status_code=status_code
            )
        )
