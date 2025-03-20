from starlette import status

from app.api.v1.exceptions.api_error import APIError


class InvalidPaymentAmountError(APIError):
    status_code = status.HTTP_400_BAD_REQUEST
