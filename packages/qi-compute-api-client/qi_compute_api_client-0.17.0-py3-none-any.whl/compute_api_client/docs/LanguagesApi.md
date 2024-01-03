# compute_api_client.LanguagesApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**read_language_languages_id_get**](LanguagesApi.md#read_language_languages_id_get) | **GET** /languages/{id} | Retrieve language
[**read_languages_languages_get**](LanguagesApi.md#read_languages_languages_get) | **GET** /languages | List languages


# **read_language_languages_id_get**
> Language read_language_languages_id_get(id)

Retrieve language

Get language by ID.

### Example

* Api Key Authentication (user):
```python
import time
import os
import compute_api_client
from compute_api_client.models.language import Language
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
    api_instance = compute_api_client.LanguagesApi(api_client)
    id = 56 # int | 

    try:
        # Retrieve language
        api_response = await api_instance.read_language_languages_id_get(id)
        print("The response of LanguagesApi->read_language_languages_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LanguagesApi->read_language_languages_id_get: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 

### Return type

[**Language**](Language.md)

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

# **read_languages_languages_get**
> List[Language] read_languages_languages_get(q=q, latest=latest, id=id, name=name, version=version)

List languages

List languages.

### Example

* Api Key Authentication (user):
```python
import time
import os
import compute_api_client
from compute_api_client.models.language import Language
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
    api_instance = compute_api_client.LanguagesApi(api_client)
    q = 'q_example' # str |  (optional)
    latest = True # bool |  (optional)
    id = 56 # int |  (optional)
    name = 'name_example' # str |  (optional)
    version = 'version_example' # str |  (optional)

    try:
        # List languages
        api_response = await api_instance.read_languages_languages_get(q=q, latest=latest, id=id, name=name, version=version)
        print("The response of LanguagesApi->read_languages_languages_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LanguagesApi->read_languages_languages_get: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **q** | **str**|  | [optional] 
 **latest** | **bool**|  | [optional] 
 **id** | **int**|  | [optional] 
 **name** | **str**|  | [optional] 
 **version** | **str**|  | [optional] 

### Return type

[**List[Language]**](Language.md)

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

