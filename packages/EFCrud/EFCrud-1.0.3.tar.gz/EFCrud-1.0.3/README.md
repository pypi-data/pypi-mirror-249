# EFCrud

- API version: 1.0
- Package version: 1.0.2
- Build package: org.openapitools.codegen.languages.PythonClientCodegen

## Requirements.

Python 3.7+

## Installation & Usage
### pip install

From Pypi:

```sh
pip install EFCrud
```

If the python package is hosted on a repository, you can install directly using:

```sh
pip install git+https://github.com/dprakash2101/EFCrudPython.git
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com/dprakash2101/EFCrudPython.git`)

Then import the package:
```python
import EFCrud
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import EFCrud
```

### Tests

Execute `pytest` to run the tests.

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

```python

import time
import EFCrud
from EFCrud.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://localhost:7217
# See configuration.py for a list of all supported configuration parameters.
configuration = EFCrud.Configuration(
    host = "https://localhost:7217"
)



# Enter a context with an instance of the API client
with EFCrud.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = EFCrud.AuthApi(api_client)
    userdto = EFCrud.Userdto() # Userdto |  (optional)

    try:
        api_response = api_instance.api_auth_login_post(userdto=userdto)
        print("The response of AuthApi->api_auth_login_post:\n")
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling AuthApi->api_auth_login_post: %s\n" % e)

```

## Documentation for API Endpoints

All URIs are relative to *https://localhost:7217*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*AuthApi* | [**api_auth_login_post**](docs/AuthApi.md#api_auth_login_post) | **POST** /api/Auth/login | 
*AuthApi* | [**api_auth_register_post**](docs/AuthApi.md#api_auth_register_post) | **POST** /api/Auth/register | 
*EmployeesApi* | [**api_employees_get**](docs/EmployeesApi.md#api_employees_get) | **GET** /api/Employees | 
*EmployeesApi* | [**api_employees_id_delete**](docs/EmployeesApi.md#api_employees_id_delete) | **DELETE** /api/Employees/{id} | 
*EmployeesApi* | [**api_employees_id_get**](docs/EmployeesApi.md#api_employees_id_get) | **GET** /api/Employees/{id} | 
*EmployeesApi* | [**api_employees_id_put**](docs/EmployeesApi.md#api_employees_id_put) | **PUT** /api/Employees/{id} | 
*EmployeesApi* | [**api_employees_post**](docs/EmployeesApi.md#api_employees_post) | **POST** /api/Employees | 
*FeaturesApi* | [**api_features_id_delete**](docs/FeaturesApi.md#api_features_id_delete) | **DELETE** /api/Features/{id} | 
*FeaturesApi* | [**api_features_id_put**](docs/FeaturesApi.md#api_features_id_put) | **PUT** /api/Features/{id} | 
*RolesApi* | [**api_roles_add_employee_role_post**](docs/RolesApi.md#api_roles_add_employee_role_post) | **POST** /api/Roles/Add-EmployeeRole | 
*RolesApi* | [**api_roles_add_roles_post**](docs/RolesApi.md#api_roles_add_roles_post) | **POST** /api/Roles/Add-roles | 
*RolesApi* | [**api_roles_delete_emp_role_delete**](docs/RolesApi.md#api_roles_delete_emp_role_delete) | **DELETE** /api/Roles/Delete-EmpRole | 
*RolesApi* | [**api_roles_show_employee_roles_get**](docs/RolesApi.md#api_roles_show_employee_roles_get) | **GET** /api/Roles/Show-EmployeeRoles | 
*RolesApi* | [**api_roles_show_roles_get**](docs/RolesApi.md#api_roles_show_roles_get) | **GET** /api/Roles/Show-roles | 


## Documentation For Models

 - [Employee](docs/Employee.md)
 - [Roles](docs/Roles.md)
 - [User](docs/User.md)
 - [UserRoles](docs/UserRoles.md)
 - [Userdto](docs/Userdto.md)


<a id="documentation-for-authorization"></a>
## Documentation For Authorization


Authentication schemes defined for the API:
<a id="oauth2"></a>
### oauth2

- **Type**: API key
- **API key parameter name**: Authorization
- **Location**: HTTP header


## Author

- [Devi Prakash](https://github.com/dprakash2101)
- Email: dprakash2101@gmail.com




