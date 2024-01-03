# compute_api_client.ReservationsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_reservation_reservations_post**](ReservationsApi.md#create_reservation_reservations_post) | **POST** /reservations | Create reservation
[**read_reservation_reservations_id_get**](ReservationsApi.md#read_reservation_reservations_id_get) | **GET** /reservations/{id} | Retrieve reservation
[**read_reservations_reservations_get**](ReservationsApi.md#read_reservations_reservations_get) | **GET** /reservations | List reservations
[**terminate_reservation_reservations_id_terminate_patch**](ReservationsApi.md#terminate_reservation_reservations_id_terminate_patch) | **PATCH** /reservations/{id}/terminate | Terminate reservation


# **create_reservation_reservations_post**
> Reservation create_reservation_reservations_post(reservation_in)

Create reservation

Create new reservation.

### Example

* Api Key Authentication (user):
```python
import time
import os
import compute_api_client
from compute_api_client.models.reservation import Reservation
from compute_api_client.models.reservation_in import ReservationIn
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
    api_instance = compute_api_client.ReservationsApi(api_client)
    reservation_in = compute_api_client.ReservationIn() # ReservationIn | 

    try:
        # Create reservation
        api_response = await api_instance.create_reservation_reservations_post(reservation_in)
        print("The response of ReservationsApi->create_reservation_reservations_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReservationsApi->create_reservation_reservations_post: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **reservation_in** | [**ReservationIn**](ReservationIn.md)|  | 

### Return type

[**Reservation**](Reservation.md)

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

# **read_reservation_reservations_id_get**
> Reservation read_reservation_reservations_id_get(id)

Retrieve reservation

Get reservation by ID.

### Example

* Api Key Authentication (user):
```python
import time
import os
import compute_api_client
from compute_api_client.models.reservation import Reservation
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
    api_instance = compute_api_client.ReservationsApi(api_client)
    id = 56 # int | 

    try:
        # Retrieve reservation
        api_response = await api_instance.read_reservation_reservations_id_get(id)
        print("The response of ReservationsApi->read_reservation_reservations_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReservationsApi->read_reservation_reservations_id_get: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 

### Return type

[**Reservation**](Reservation.md)

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

# **read_reservations_reservations_get**
> List[Reservation] read_reservations_reservations_get(latest=latest, id=id, member_id=member_id, start_time=start_time, end_time=end_time, backend_type_id=backend_type_id, backend_id__isnull=backend_id__isnull, backend_id=backend_id, is_terminated=is_terminated)

List reservations

Read reservations.

### Example

* Api Key Authentication (user):
```python
import time
import os
import compute_api_client
from compute_api_client.models.reservation import Reservation
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
    api_instance = compute_api_client.ReservationsApi(api_client)
    latest = True # bool |  (optional)
    id = 56 # int |  (optional)
    member_id = 56 # int |  (optional)
    start_time = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
    end_time = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
    backend_type_id = 56 # int |  (optional)
    backend_id__isnull = True # bool |  (optional)
    backend_id = 56 # int |  (optional)
    is_terminated = True # bool |  (optional)

    try:
        # List reservations
        api_response = await api_instance.read_reservations_reservations_get(latest=latest, id=id, member_id=member_id, start_time=start_time, end_time=end_time, backend_type_id=backend_type_id, backend_id__isnull=backend_id__isnull, backend_id=backend_id, is_terminated=is_terminated)
        print("The response of ReservationsApi->read_reservations_reservations_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReservationsApi->read_reservations_reservations_get: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **latest** | **bool**|  | [optional] 
 **id** | **int**|  | [optional] 
 **member_id** | **int**|  | [optional] 
 **start_time** | **datetime**|  | [optional] 
 **end_time** | **datetime**|  | [optional] 
 **backend_type_id** | **int**|  | [optional] 
 **backend_id__isnull** | **bool**|  | [optional] 
 **backend_id** | **int**|  | [optional] 
 **is_terminated** | **bool**|  | [optional] 

### Return type

[**List[Reservation]**](Reservation.md)

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

# **terminate_reservation_reservations_id_terminate_patch**
> Reservation terminate_reservation_reservations_id_terminate_patch(id)

Terminate reservation

Terminate reservation by ID.

### Example

* Api Key Authentication (user):
```python
import time
import os
import compute_api_client
from compute_api_client.models.reservation import Reservation
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
    api_instance = compute_api_client.ReservationsApi(api_client)
    id = 56 # int | 

    try:
        # Terminate reservation
        api_response = await api_instance.terminate_reservation_reservations_id_terminate_patch(id)
        print("The response of ReservationsApi->terminate_reservation_reservations_id_terminate_patch:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReservationsApi->terminate_reservation_reservations_id_terminate_patch: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 

### Return type

[**Reservation**](Reservation.md)

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

