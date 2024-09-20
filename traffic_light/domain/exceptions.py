import json
from typing import Any, Dict, Optional

from fastapi import HTTPException, status


class TrafficLightBaseException(Exception):
    http_status = 500
    detail = "TrafficLightBaseException"
    message = None

    def __init__(
        self,
        message: Optional[str] = None,
        http_status: Optional[int] = None,
    ) -> None:
        if message is not None:
            self.message = message

        if http_status is not None:
            self.http_status = int(http_status)

        self.args = tuple(
            [
                self.message,
                self.http_status,
                self.detail,
            ]
        )

    @property
    def json(self) -> Dict[str, Any]:
        return {
            "type": self.__class__.__name__,
            "message": self.message,
            "status": self.http_status,
            "detail": self.detail,
        }

    def __str__(self) -> str:
        return f"{super().__str__()}: {json.dumps(self.json)}"


# TrafficLightExceptions
class TrafficLightValidationException(TrafficLightBaseException):
    http_status = 400
    detail = "Traffic Light Validation Exception"


class HTTPTrafficLightValidationException(HTTPException):
    def __init__(self, message: str = TrafficLightValidationException.detail):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=message)


class TrafficLightNotFoundException(TrafficLightBaseException):
    http_status = 404
    detail = "TrafficLight not found"


class HTTPTrafficLightNotFoundException(HTTPException):
    def __init__(self, message: str = TrafficLightNotFoundException.detail):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=message)
