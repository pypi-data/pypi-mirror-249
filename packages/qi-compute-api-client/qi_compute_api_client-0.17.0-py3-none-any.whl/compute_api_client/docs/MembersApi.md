# compute_api_client.MembersApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_member_members_post**](MembersApi.md#create_member_members_post) | **POST** /members | Create member
[**delete_member_members_id_delete**](MembersApi.md#delete_member_members_id_delete) | **DELETE** /members/{id} | Destroy member
[**read_member_members_id_get**](MembersApi.md#read_member_members_id_get) | **GET** /members/{id} | Retrieve member
[**read_members_members_get**](MembersApi.md#read_members_members_get) | **GET** /members | List members


# **create_member_members_post**
> Member create_member_members_post(member_in)

Create member

Create new member.

### Example

* Api Key Authentication (user):
```python
import time
import os
import compute_api_client
from compute_api_client.models.member import Member
from compute_api_client.models.member_in import MemberIn
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
    api_instance = compute_api_client.MembersApi(api_client)
    member_in = compute_api_client.MemberIn() # MemberIn | 

    try:
        # Create member
        api_response = await api_instance.create_member_members_post(member_in)
        print("The response of MembersApi->create_member_members_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MembersApi->create_member_members_post: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **member_in** | [**MemberIn**](MemberIn.md)|  | 

### Return type

[**Member**](Member.md)

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

# **delete_member_members_id_delete**
> delete_member_members_id_delete(id)

Destroy member

Delete a member.

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
    api_instance = compute_api_client.MembersApi(api_client)
    id = 56 # int | 

    try:
        # Destroy member
        await api_instance.delete_member_members_id_delete(id)
    except Exception as e:
        print("Exception when calling MembersApi->delete_member_members_id_delete: %s\n" % e)
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

# **read_member_members_id_get**
> Member read_member_members_id_get(id)

Retrieve member

Get member by ID.

### Example

* Api Key Authentication (user):
```python
import time
import os
import compute_api_client
from compute_api_client.models.member import Member
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
    api_instance = compute_api_client.MembersApi(api_client)
    id = 56 # int | 

    try:
        # Retrieve member
        api_response = await api_instance.read_member_members_id_get(id)
        print("The response of MembersApi->read_member_members_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MembersApi->read_member_members_id_get: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 

### Return type

[**Member**](Member.md)

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

# **read_members_members_get**
> List[Member] read_members_members_get(latest=latest, id=id, team_id=team_id, user_id=user_id, role=role, is_active=is_active)

List members

Read members.

### Example

* Api Key Authentication (user):
```python
import time
import os
import compute_api_client
from compute_api_client.models.member import Member
from compute_api_client.models.role import Role
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
    api_instance = compute_api_client.MembersApi(api_client)
    latest = True # bool |  (optional)
    id = 56 # int |  (optional)
    team_id = 56 # int |  (optional)
    user_id = 56 # int |  (optional)
    role = compute_api_client.Role() # Role |  (optional)
    is_active = True # bool |  (optional)

    try:
        # List members
        api_response = await api_instance.read_members_members_get(latest=latest, id=id, team_id=team_id, user_id=user_id, role=role, is_active=is_active)
        print("The response of MembersApi->read_members_members_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MembersApi->read_members_members_get: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **latest** | **bool**|  | [optional] 
 **id** | **int**|  | [optional] 
 **team_id** | **int**|  | [optional] 
 **user_id** | **int**|  | [optional] 
 **role** | [**Role**](.md)|  | [optional] 
 **is_active** | **bool**|  | [optional] 

### Return type

[**List[Member]**](Member.md)

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

