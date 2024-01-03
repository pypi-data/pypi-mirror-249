# compute_api_client.BackendTypesApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**read_backend_type_backend_types_id_get**](BackendTypesApi.md#read_backend_type_backend_types_id_get) | **GET** /backend_types/{id} | Retrieve backend type
[**read_backend_types_backend_types_get**](BackendTypesApi.md#read_backend_types_backend_types_get) | **GET** /backend_types/ | List backend types


# **read_backend_type_backend_types_id_get**
> BackendType read_backend_type_backend_types_id_get(id)

Retrieve backend type

Get backend type by ID.

### Example

* Api Key Authentication (user):
```python
import time
import os
import compute_api_client
from compute_api_client.models.backend_type import BackendType
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
    api_instance = compute_api_client.BackendTypesApi(api_client)
    id = 56 # int | 

    try:
        # Retrieve backend type
        api_response = await api_instance.read_backend_type_backend_types_id_get(id)
        print("The response of BackendTypesApi->read_backend_type_backend_types_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BackendTypesApi->read_backend_type_backend_types_id_get: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 

### Return type

[**BackendType**](BackendType.md)

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

# **read_backend_types_backend_types_get**
> List[BackendType] read_backend_types_backend_types_get(latest=latest, id=id, name=name, infrastructure=infrastructure, description=description, image_id=image_id, is_hardware=is_hardware)

List backend types

Read backend types.

### Example

* Api Key Authentication (user):
```python
import time
import os
import compute_api_client
from compute_api_client.models.backend_type import BackendType
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
    api_instance = compute_api_client.BackendTypesApi(api_client)
    latest = True # bool |  (optional)
    id = 56 # int |  (optional)
    name = 'name_example' # str |  (optional)
    infrastructure = 'infrastructure_example' # str |  (optional)
    description = 'description_example' # str |  (optional)
    image_id = 'image_id_example' # str |  (optional)
    is_hardware = True # bool |  (optional)

    try:
        # List backend types
        api_response = await api_instance.read_backend_types_backend_types_get(latest=latest, id=id, name=name, infrastructure=infrastructure, description=description, image_id=image_id, is_hardware=is_hardware)
        print("The response of BackendTypesApi->read_backend_types_backend_types_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BackendTypesApi->read_backend_types_backend_types_get: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **latest** | **bool**|  | [optional] 
 **id** | **int**|  | [optional] 
 **name** | **str**|  | [optional] 
 **infrastructure** | **str**|  | [optional] 
 **description** | **str**|  | [optional] 
 **image_id** | **str**|  | [optional] 
 **is_hardware** | **bool**|  | [optional] 

### Return type

[**List[BackendType]**](BackendType.md)

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

