import base64
import re
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel, validator, ValidationError

from apiclient import (
    HeaderAuthentication,
    JsonResponseHandler,
    JsonRequestFormatter
)

from .extensions import (
    LoginRequestFormatter,
    SFCCErrorHandler
)

from .client import APIConnector


class AppConfig(BaseModel):
    # TODO extend validation / constraints on these values
    domain: str
    ocapi_version: Optional[str] = "v21_3"
    site_id: Optional[str] = "-"
    use_ssl: Optional[bool] = False
    is_production: Optional[bool] = False
    username: str
    password: str
    client_id: str
    client_password: str

    @property
    def base_url(self):
        protocol = "https://" if self.use_ssl else "http://"
        site_id_url = "/s/{}".format(self.site_id)
        prod_url = "{}".format(site_id_url if not self.is_production else "")
        return "{}{}{}/dw".format(protocol, self.domain, prod_url)
        # http(s)://public_domain[/s/site_id]/dw/api_type/ PROD
        # http(s)://sub_domain.demandware.net/s/site_id/dw/api_type/ NOT-prod

    @property
    def base_domain(self):
        protocol = "https://" if self.use_ssl else "http://"
        return "{}{}".format(protocol, self.domain)

    @property
    def auth_header(self):
        ret_val = "{0}:{1}:{2}".format(
            self.username,
            self.password,
            self.client_password).encode('utf-8')
        return base64.b64encode(ret_val)

    @validator("ocapi_version")
    def validate_ocapi_version(cls, v):
        pattern = re.compile("^v[0-9]{1,2}_[0-9]{1,2}$")
        if not pattern.match(v):
            raise ValueError("Unknown format of OCAPI Version. Supported format \
                is v<year>_<consecutive number> (e.g. 'v13_1')")
        return v


class SFCCClient(object):
    """This class will handle authentication and API calls towards SFCC.

       Initialization may raise APIRequestError and other exception
    """
    @property
    def configuration(self):
        return self._configuration

    @configuration.setter
    def configuration(self, new_configuration):
        self._configuration = new_configuration

    @property
    def expiration(self):
        return self._expiration

    @expiration.setter
    def expiration(self, new_expiration):
        self._expiration = datetime.now() + timedelta(seconds=new_expiration)

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, new_token):
        self._token = new_token

    def authenticate(self):
        """ 1. Perform authentication against SFCC
            2. Set token and its expiration
        """
        # Instantiate a client for authentication
        oauth_client = APIConnector(
            config=self.configuration,
            authentication_method=HeaderAuthentication(
                token=self.configuration.auth_header.decode(),
                parameter="Authorization",
                scheme="Basic",
            ),
            response_handler=JsonResponseHandler,
            error_handler=SFCCErrorHandler,
            request_formatter=LoginRequestFormatter
        )

        # This call may raise APIRequestError
        resp = oauth_client.authenticate()
        self.token = resp["access_token"]
        self.expiration = resp["expires_in"]

        return resp

    def __init__(self, cfg: dict):
        try:
            self.configuration = AppConfig(**cfg)
        except ValidationError as e:
            raise ValueError("Configuration initialization failed with error {}".format(e))

    def __getattr__(self, attr):
        """ Route calls to the client object
        """
        # Instantiate a client for all other calls
        if hasattr(APIConnector, attr):
            def wrapper(*args, **kw):
                try:
                    if datetime.now() >= self.expiration:
                        print("Token expired. Authenticating before executing '{}'".format(attr))
                        self.authenticate()
                except AttributeError as e:
                    print("Token not found. Authenticating before executing '{}' [Error: {}]".format(attr, e))
                    self.authenticate()

                return getattr(
                    APIConnector(
                        authentication_method=HeaderAuthentication(token=self.token),
                        response_handler=JsonResponseHandler,
                        error_handler=SFCCErrorHandler,
                        request_formatter=JsonRequestFormatter
                    ), attr)(*args, **kw)
            return wrapper
        raise AttributeError(attr)

    def __format__(self, format_str):
        """ Format message to be printed out
        """
        if self.token and datetime.now() < self.expiration:
            return "Authenticated. Token {} is still valid".format(self.token)
        else:
            return "Token expired or not found. Please authenticate again."
