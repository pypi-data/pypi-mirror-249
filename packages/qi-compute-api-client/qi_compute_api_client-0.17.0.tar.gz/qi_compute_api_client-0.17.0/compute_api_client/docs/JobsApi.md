# compute_api_client.JobsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_job_jobs_post**](JobsApi.md#create_job_jobs_post) | **POST** /jobs | Create job
[**delete_job_jobs_id_delete**](JobsApi.md#delete_job_jobs_id_delete) | **DELETE** /jobs/{id} | Destroy job
[**read_job_jobs_id_get**](JobsApi.md#read_job_jobs_id_get) | **GET** /jobs/{id} | Retrieve job
[**read_jobs_jobs_get**](JobsApi.md#read_jobs_jobs_get) | **GET** /jobs | List jobs
[**update_job_status_jobs_id_patch**](JobsApi.md#update_job_status_jobs_id_patch) | **PATCH** /jobs/{id} | Update Job Status


# **create_job_jobs_post**
> Job create_job_jobs_post(job_in)

Create job

Create new job.

### Example

* Api Key Authentication (user):
```python
import time
import os
import compute_api_client
from compute_api_client.models.job import Job
from compute_api_client.models.job_in import JobIn
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
    api_instance = compute_api_client.JobsApi(api_client)
    job_in = compute_api_client.JobIn() # JobIn | 

    try:
        # Create job
        api_response = await api_instance.create_job_jobs_post(job_in)
        print("The response of JobsApi->create_job_jobs_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling JobsApi->create_job_jobs_post: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **job_in** | [**JobIn**](JobIn.md)|  | 

### Return type

[**Job**](Job.md)

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

# **delete_job_jobs_id_delete**
> delete_job_jobs_id_delete(id)

Destroy job

Delete a job.

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
    api_instance = compute_api_client.JobsApi(api_client)
    id = 56 # int | 

    try:
        # Destroy job
        await api_instance.delete_job_jobs_id_delete(id)
    except Exception as e:
        print("Exception when calling JobsApi->delete_job_jobs_id_delete: %s\n" % e)
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

# **read_job_jobs_id_get**
> Job read_job_jobs_id_get(id)

Retrieve job

Get job by ID.

### Example

* Api Key Authentication (user):
```python
import time
import os
import compute_api_client
from compute_api_client.models.job import Job
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
    api_instance = compute_api_client.JobsApi(api_client)
    id = 56 # int | 

    try:
        # Retrieve job
        api_response = await api_instance.read_job_jobs_id_get(id)
        print("The response of JobsApi->read_job_jobs_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling JobsApi->read_job_jobs_id_get: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 

### Return type

[**Job**](Job.md)

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

# **read_jobs_jobs_get**
> List[Job] read_jobs_jobs_get(latest=latest, id=id, created_on=created_on, file_id=file_id, algorithm_type=algorithm_type, status=status, batch_job_id=batch_job_id, queued_at__isnull=queued_at__isnull, queued_at=queued_at, finished_at__isnull=finished_at__isnull, finished_at=finished_at, number_of_shots__isnull=number_of_shots__isnull, number_of_shots=number_of_shots)

List jobs

List jobs.

### Example

* Api Key Authentication (user):
```python
import time
import os
import compute_api_client
from compute_api_client.models.algorithm_type import AlgorithmType
from compute_api_client.models.job import Job
from compute_api_client.models.job_status import JobStatus
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
    api_instance = compute_api_client.JobsApi(api_client)
    latest = True # bool |  (optional)
    id = 56 # int |  (optional)
    created_on = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
    file_id = 56 # int |  (optional)
    algorithm_type = compute_api_client.AlgorithmType() # AlgorithmType |  (optional)
    status = compute_api_client.JobStatus() # JobStatus |  (optional)
    batch_job_id = 56 # int |  (optional)
    queued_at__isnull = True # bool |  (optional)
    queued_at = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
    finished_at__isnull = True # bool |  (optional)
    finished_at = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
    number_of_shots__isnull = True # bool |  (optional)
    number_of_shots = 56 # int |  (optional)

    try:
        # List jobs
        api_response = await api_instance.read_jobs_jobs_get(latest=latest, id=id, created_on=created_on, file_id=file_id, algorithm_type=algorithm_type, status=status, batch_job_id=batch_job_id, queued_at__isnull=queued_at__isnull, queued_at=queued_at, finished_at__isnull=finished_at__isnull, finished_at=finished_at, number_of_shots__isnull=number_of_shots__isnull, number_of_shots=number_of_shots)
        print("The response of JobsApi->read_jobs_jobs_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling JobsApi->read_jobs_jobs_get: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **latest** | **bool**|  | [optional] 
 **id** | **int**|  | [optional] 
 **created_on** | **datetime**|  | [optional] 
 **file_id** | **int**|  | [optional] 
 **algorithm_type** | [**AlgorithmType**](.md)|  | [optional] 
 **status** | [**JobStatus**](.md)|  | [optional] 
 **batch_job_id** | **int**|  | [optional] 
 **queued_at__isnull** | **bool**|  | [optional] 
 **queued_at** | **datetime**|  | [optional] 
 **finished_at__isnull** | **bool**|  | [optional] 
 **finished_at** | **datetime**|  | [optional] 
 **number_of_shots__isnull** | **bool**|  | [optional] 
 **number_of_shots** | **int**|  | [optional] 

### Return type

[**List[Job]**](Job.md)

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

# **update_job_status_jobs_id_patch**
> Job update_job_status_jobs_id_patch(id, job_patch)

Update Job Status

Update status of a job.

### Example

* Api Key Authentication (backend):
* Api Key Authentication (user):
```python
import time
import os
import compute_api_client
from compute_api_client.models.job import Job
from compute_api_client.models.job_patch import JobPatch
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
    api_instance = compute_api_client.JobsApi(api_client)
    id = 56 # int | 
    job_patch = compute_api_client.JobPatch() # JobPatch | 

    try:
        # Update Job Status
        api_response = await api_instance.update_job_status_jobs_id_patch(id, job_patch)
        print("The response of JobsApi->update_job_status_jobs_id_patch:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling JobsApi->update_job_status_jobs_id_patch: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 
 **job_patch** | [**JobPatch**](JobPatch.md)|  | 

### Return type

[**Job**](Job.md)

### Authorization

[backend](../README.md#backend), [user](../README.md#user)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**404** | Not Found |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

