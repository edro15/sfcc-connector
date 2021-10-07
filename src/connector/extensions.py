
from apiclient.utils.typing import (
    OptionalJsonType,
    OptionalStr,
)

from apiclient.request_formatters import BaseRequestFormatter

from apiclient.error_handlers import BaseErrorHandler
from apiclient import exceptions
from apiclient.response import Response


class LoginRequestFormatter(BaseRequestFormatter):
    """Format the outgoing data as x-www-form-urlencoded
    """

    content_type = "application/x-www-form-urlencoded"

    @classmethod
    def format(cls, data: OptionalJsonType) -> OptionalStr:
        if data:
            return "{}={}".format(list(data.keys())[0], list(data.values())[0])


class SFCCErrorHandler(BaseErrorHandler):
    """Format the error messages according to SFCC definition
    """

    @staticmethod
    def get_exception(response: Response) -> exceptions.APIRequestError:
        """Parses client errors to extract bad request reasons."""
        json = response.get_json()
        err_args = json["fault"]["arguments"]
        err_msg = json["fault"]["message"]
        err_type = json["fault"]["type"]
        error = "{0}: {1} - {2}".format(err_type, err_msg, err_args)

        if 400 <= response.get_status_code() < 500:
            # json = response.get_json()
            return exceptions.ClientError(error, response.get_status_code())

        return exceptions.APIRequestError(error, response.get_status_code())
