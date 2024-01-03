import pytest
import requests_mock
from orodha_user_client import OrodhaUserClient
from tests.fixtures.mock_credentials import MOCK_BASE_URL
from tests.fixtures.mock_request_args import MOCK_BULK_REQUEST_ARGS, MOCK_BULK_RESPONSE_ARGS
from tests.conftest import MockEnvironment
from orodha_user_client.exceptions import UrlNotFound, RequestError


def test_bulk_get(mock_credentials_object, mock_orodha_keycloak):
    with MockEnvironment(ORODHA_USER_SERVICE_BASE_URL=MOCK_BASE_URL):
        user_client = OrodhaUserClient(mock_credentials_object)

    with requests_mock.Mocker() as mock_request:
        mock_request.post(f"{MOCK_BASE_URL}/get-bulk-users", json=MOCK_BULK_RESPONSE_ARGS)

        response = user_client.bulk_get(MOCK_BULK_REQUEST_ARGS)
        assert response == MOCK_BULK_RESPONSE_ARGS


def test_user_client_bad_url(mock_credentials_object, mock_orodha_keycloak):
    with MockEnvironment(ORODHA_USER_SERVICE_BASE_URL=""):
        with pytest.raises(UrlNotFound):
            OrodhaUserClient(mock_credentials_object)


def test_bulk_get_request_error(mock_credentials_object, mock_orodha_keycloak):
    with MockEnvironment(ORODHA_USER_SERVICE_BASE_URL=MOCK_BASE_URL):
        user_client = OrodhaUserClient(mock_credentials_object)

    with requests_mock.Mocker() as mock_request:
        mock_request.register_uri(
            'POST',
            f"{MOCK_BASE_URL}/get-bulk-users",
            text='Not Found',
            status_code=404
        )
        with pytest.raises(RequestError):
            user_client.bulk_get(MOCK_BULK_REQUEST_ARGS)
