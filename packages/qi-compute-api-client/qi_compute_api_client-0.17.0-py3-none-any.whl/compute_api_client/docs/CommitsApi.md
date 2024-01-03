# compute_api_client.CommitsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_commit_commits_post**](CommitsApi.md#create_commit_commits_post) | **POST** /commits | Create commit
[**delete_commit_commits_id_delete**](CommitsApi.md#delete_commit_commits_id_delete) | **DELETE** /commits/{id} | Destroy commit
[**read_commit_commits_id_get**](CommitsApi.md#read_commit_commits_id_get) | **GET** /commits/{id} | Get commit by ID
[**read_commits_commits_get**](CommitsApi.md#read_commits_commits_get) | **GET** /commits | List commits


# **create_commit_commits_post**
> Commit create_commit_commits_post(commit_in)

Create commit

Create new commit.

### Example

* Api Key Authentication (user):
```python
import time
import os
import compute_api_client
from compute_api_client.models.commit import Commit
from compute_api_client.models.commit_in import CommitIn
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
    api_instance = compute_api_client.CommitsApi(api_client)
    commit_in = compute_api_client.CommitIn() # CommitIn | 

    try:
        # Create commit
        api_response = await api_instance.create_commit_commits_post(commit_in)
        print("The response of CommitsApi->create_commit_commits_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CommitsApi->create_commit_commits_post: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **commit_in** | [**CommitIn**](CommitIn.md)|  | 

### Return type

[**Commit**](Commit.md)

### Authorization

[user](../README.md#user)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_commit_commits_id_delete**
> delete_commit_commits_id_delete(id)

Destroy commit

Delete a commit.

### Example

* Api Key Authentication (user):
```python
import time
import os
import compute_api_client
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
    api_instance = compute_api_client.CommitsApi(api_client)
    id = 56 # int | 

    try:
        # Destroy commit
        await api_instance.delete_commit_commits_id_delete(id)
    except Exception as e:
        print("Exception when calling CommitsApi->delete_commit_commits_id_delete: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 

### Return type

void (empty response body)

### Authorization

[user](../README.md#user)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successful Response |  -  |
**404** | Not Found |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **read_commit_commits_id_get**
> Commit read_commit_commits_id_get(id)

Get commit by ID

Get commit by ID.

### Example

* Api Key Authentication (backend):
* Api Key Authentication (user):
```python
import time
import os
import compute_api_client
from compute_api_client.models.commit import Commit
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

# Configure API key authorization: backend
configuration.api_key['backend'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['backend'] = 'Bearer'

# Configure API key authorization: user
configuration.api_key['user'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['user'] = 'Bearer'

# Enter a context with an instance of the API client
async with compute_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = compute_api_client.CommitsApi(api_client)
    id = 56 # int | 

    try:
        # Get commit by ID
        api_response = await api_instance.read_commit_commits_id_get(id)
        print("The response of CommitsApi->read_commit_commits_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CommitsApi->read_commit_commits_id_get: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 

### Return type

[**Commit**](Commit.md)

### Authorization

[backend](../README.md#backend), [user](../README.md#user)

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

# **read_commits_commits_get**
> List[Commit] read_commits_commits_get(latest=latest, id=id, created_on=created_on, hash=hash, description=description, algorithm_id=algorithm_id)

List commits

List commits.

### Example

* Api Key Authentication (user):
```python
import time
import os
import compute_api_client
from compute_api_client.models.commit import Commit
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
    api_instance = compute_api_client.CommitsApi(api_client)
    latest = True # bool |  (optional)
    id = 56 # int |  (optional)
    created_on = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
    hash = 'hash_example' # str |  (optional)
    description = 'description_example' # str |  (optional)
    algorithm_id = 56 # int |  (optional)

    try:
        # List commits
        api_response = await api_instance.read_commits_commits_get(latest=latest, id=id, created_on=created_on, hash=hash, description=description, algorithm_id=algorithm_id)
        print("The response of CommitsApi->read_commits_commits_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CommitsApi->read_commits_commits_get: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **latest** | **bool**|  | [optional] 
 **id** | **int**|  | [optional] 
 **created_on** | **datetime**|  | [optional] 
 **hash** | **str**|  | [optional] 
 **description** | **str**|  | [optional] 
 **algorithm_id** | **int**|  | [optional] 

### Return type

[**List[Commit]**](Commit.md)

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

