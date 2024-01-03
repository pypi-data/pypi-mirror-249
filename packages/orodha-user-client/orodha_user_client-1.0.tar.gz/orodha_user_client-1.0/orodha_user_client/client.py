"""
The main module of the Orodha User Client. Contains UserClient class
which is used to connect to and communicate with the Orodha User Service on behalf
of other Orodha services.
"""
import os
from http import HTTPStatus
import requests
from orodha_user_client.exceptions import (
    UrlNotFound,
    RequestError,
    UnexpectedRequestType
)
import orodha_keycloak


BULK_USER_URL = "get-bulk-users"

def _request_factory(request_type: str):
    """
    Factory function which accepts a request_type string, and
    returns the correct method from the requests module.

    Args:
        request_type(str): The string representation of the type of HTTP request
            we want to make.

    Raises:
        SomeError: If the request_type is not PUT, POST, GET, or DELETE.

    Returns:
        request_method: The method from the requests library that matches the request_type
            argument.
    """
    if not hasattr(requests, request_type.lower()):
        raise UnexpectedRequestType(
            message=f"{request_type.lower()} is not an accepted request type."
        )

    return getattr(requests, request_type.lower())

class OrodhaUserClient:
    """
    The main class for the orodha_user_client package. Allows services
    to interact with the Orodha User Service programmatically.
    """
    def __init__(self, credentials: orodha_keycloak.OrodhaCredentials):
        self.credentials = credentials
        self.keycloak_client = orodha_keycloak.OrodhaKeycloakClient(credentials_object=self.credentials)
        self.base_url = self._get_base_url()


    def bulk_get(self, request_args: dict):
        """
        Function that calls the user service get-bulk-users route on
        behalf of other services in the Orodha namespace.

        Args:
            request_args(dict): A dictionary of request arguments to be
                packaged and sent to the Orodha user service.

        Returns:
            response(dict): A dictionary containing our new token info.
        """
        target_user = request_args.get("target_user")
        if not target_user:
            target_user = self.credentials.client_id

        token_data = self.keycloak_client.exchange_token(target_user=target_user)

        body = {
            "pageSize": request_args.get("pageSize"),
            "pageNum": request_args.get("pageNum"),
            "targets": request_args.get("targets")
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization" : f"Bearer {token_data.get('access_token')}"
        }
        return_value = self._make_raw_request(
            BULK_USER_URL,
            "post",
            body=body,
            headers=headers
        )

        return return_value


    def _get_base_url(self):
        base_url = os.environ.get("ORODHA_USER_SERVICE_BASE_URL")
        if not base_url:
            raise UrlNotFound(
                message="\"ORODHA_USER_SERVICE_BASE_URL\" must be present in environment"
            )
        return base_url.rstrip("/")


    def _make_raw_request(
            self,
            route: str,
            request_type: str,
            **request_args
        ):
        desired_request = _request_factory(request_type)

        response = desired_request(
            f"{self.base_url}/{route.lower()}",
            headers=request_args.get("headers"),
            data=request_args.get("body")
        )

        if response.status_code != HTTPStatus.OK:
            raise RequestError(
                message="A problem was encountered during execution.",
                status_code=response.status_code
            )
        try:
            return_value = response.json()
        except ValueError:
            return_value = response.content
        return return_value
