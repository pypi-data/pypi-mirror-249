"""
Module which contains mock request, as well as return arguments for the OrodhaUserClient class
"""

MOCK_BULK_REQUEST_ARGS = {
    "target_user": None,
    "pageSize": 10,
    "pageNum": 1,
    "targets": None
}

MOCK_BULK_RESPONSE_ARGS = [{
    "_id": "some_id",
    "keycloak_id": "some_keycloak_id",
    "username": "some_username",
}]

MOCK_TOKEN_EXCHANGE_RESPONSE = {
   "access_token" : "some_token_value",
   "refresh_token" : None,
   "expires_in" : "some_timestamp"
 }
