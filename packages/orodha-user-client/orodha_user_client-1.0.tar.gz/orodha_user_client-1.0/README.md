# orodha-user-sdk

## Description

The Orodha User SDK is a Software Development Kit used in
order to interact with the Orodha User Service.

## Usage

In order to use the SDK you need to have an environment variable that contains the base url for the running user service. This variable is named

`ORODHA_USER_SERVICE_BASE_URL`

To use the SDK you must import the client class from the orodha_user_client module, like so:

`from orodha_user_client import OrodhaUserClient`

After importing the module, you simply instantiate the client with a special credentials object which you can create using [orodha-keycloak](https://pypi.org/project/orodha-keycloak/).

The credentials object is called `OrodhaCredentials` and is an object containing the information needed to communicate with keycloak via orodha-keycloak.

### Methods

The only available method currently is the `bulk_get` method.
This method will return a list of objects with the following structure:

```
{
    "_id": str,
    "keycloak_id": str,
    "username": str,
}
```

It accepts a dictionary called request_args that contains the arguments for the request to the Orodha User Service.

The expected shape of the dictionary is as so:

```
{
    "pageSize": int,
    "pageNum": int,
    "targets": list[str]
}
```

The `targets` list is used to query only for specific usernames and their values; if the targets list is empty, the query will be for all users in the database.

A dictionary is required to be passed into the function, but the dictionary need not contain any values; this is because the user service contains default values for this call.
