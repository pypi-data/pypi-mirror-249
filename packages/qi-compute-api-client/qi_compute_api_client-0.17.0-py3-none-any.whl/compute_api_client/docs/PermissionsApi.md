# compute_api_client.PermissionsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**read_permission_group_permission_groups_id_get**](PermissionsApi.md#read_permission_group_permission_groups_id_get) | **GET** /permission_groups/{id} | Retrieve permission groups
[**read_permission_groups_permission_groups_get**](PermissionsApi.md#read_permission_groups_permission_groups_get) | **GET** /permission_groups/ | List permission groups
[**read_permission_permissions_id_get**](PermissionsApi.md#read_permission_permissions_id_get) | **GET** /permissions/{id} | Retrieve permissions
[**read_permissions_permissions_get**](PermissionsApi.md#read_permissions_permissions_get) | **GET** /permissions/ | List permissions


# **read_permission_group_permission_groups_id_get**
> PermissionGroup read_permission_group_permission_groups_id_get(id)

Retrieve permission groups

Get permission group by ID.

### Example

* Api Key Authentication (user):
```python
import time
import os
import compute_api_client
from compute_api_client.models.permission_group import PermissionGroup
from compute_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = compute_api_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: user
configuration.api_key['user'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['user'] = 'Bearer'

# Enter a context with an instance of the API client
async with compute_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = compute_api_client.PermissionsApi(api_client)
    id = 56 # int | 

    try:
        # Retrieve permission groups
        api_response = await api_instance.read_permission_group_permission_groups_id_get(id)
        print("The response of PermissionsApi->read_permission_group_permission_groups_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PermissionsApi->read_permission_group_permission_groups_id_get: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 

### Return type

[**PermissionGroup**](PermissionGroup.md)

### Authorization

[user](../README.md#user)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**404** | Not Found |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **read_permission_groups_permission_groups_get**
> List[PermissionGroup] read_permission_groups_permission_groups_get(latest=latest, id=id, name=name)

List permission groups

Read permissions groups.

### Example

* Api Key Authentication (user):
```python
import time
import os
import compute_api_client
from compute_api_client.models.permission_group import PermissionGroup
from compute_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = compute_api_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: user
configuration.api_key['user'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['user'] = 'Bearer'

# Enter a context with an instance of the API client
async with compute_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = compute_api_client.PermissionsApi(api_client)
    latest = True # bool |  (optional)
    id = 56 # int |  (optional)
    name = 'name_example' # str |  (optional)

    try:
        # List permission groups
        api_response = await api_instance.read_permission_groups_permission_groups_get(latest=latest, id=id, name=name)
        print("The response of PermissionsApi->read_permission_groups_permission_groups_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PermissionsApi->read_permission_groups_permission_groups_get: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **latest** | **bool**|  | [optional] 
 **id** | **int**|  | [optional] 
 **name** | **str**|  | [optional] 

### Return type

[**List[PermissionGroup]**](PermissionGroup.md)

### Authorization

[user](../README.md#user)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **read_permission_permissions_id_get**
> Permission read_permission_permissions_id_get(id)

Retrieve permissions

Get permission by ID.

### Example

* Api Key Authentication (user):
```python
import time
import os
import compute_api_client
from compute_api_client.models.permission import Permission
from compute_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = compute_api_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: user
configuration.api_key['user'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['user'] = 'Bearer'

# Enter a context with an instance of the API client
async with compute_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = compute_api_client.PermissionsApi(api_client)
    id = 56 # int | 

    try:
        # Retrieve permissions
        api_response = await api_instance.read_permission_permissions_id_get(id)
        print("The response of PermissionsApi->read_permission_permissions_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PermissionsApi->read_permission_permissions_id_get: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 

### Return type

[**Permission**](Permission.md)

### Authorization

[user](../README.md#user)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**404** | Not Found |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **read_permissions_permissions_get**
> List[Permission] read_permissions_permissions_get(latest=latest, id=id, permission=permission, name=name)

List permissions

Read permissions.

### Example

* Api Key Authentication (user):
```python
import time
import os
import compute_api_client
from compute_api_client.models.permission import Permission
from compute_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = compute_api_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: user
configuration.api_key['user'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['user'] = 'Bearer'

# Enter a context with an instance of the API client
async with compute_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = compute_api_client.PermissionsApi(api_client)
    latest = True # bool |  (optional)
    id = 56 # int |  (optional)
    permission = 'permission_example' # str |  (optional)
    name = 'name_example' # str |  (optional)

    try:
        # List permissions
        api_response = await api_instance.read_permissions_permissions_get(latest=latest, id=id, permission=permission, name=name)
        print("The response of PermissionsApi->read_permissions_permissions_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PermissionsApi->read_permissions_permissions_get: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **latest** | **bool**|  | [optional] 
 **id** | **int**|  | [optional] 
 **permission** | **str**|  | [optional] 
 **name** | **str**|  | [optional] 

### Return type

[**List[Permission]**](Permission.md)

### Authorization

[user](../README.md#user)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

