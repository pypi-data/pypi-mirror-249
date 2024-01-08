# spryngtime-analytics-sdk-python-sdk<a id="spryngtime-analytics-sdk-python-sdk"></a>

Spryngtime Usage Analytics & Billing API


[![PyPI](https://img.shields.io/badge/PyPI-v1.0.1-blue)](https://pypi.org/project/spryngtime-analytics-sdk-python-sdk/1.0.1)
[![README.md](https://img.shields.io/badge/README-Click%20Here-green)](https://github.com/azianmike/spryngtime-analytics-sdk/tree/main/python#readme)

## Table of Contents<a id="table-of-contents"></a>

<!-- toc -->

- [Requirements](#requirements)
- [Installing](#installing)
- [Getting Started](#getting-started)
- [Async](#async)
- [Raw HTTP Response](#raw-http-response)
- [Reference](#reference)
  * [`spryngtimeanalyticssdk.usage_tracking.track_usage`](#spryngtimeanalyticssdkusage_trackingtrack_usage)
  * [`spryngtimeanalyticssdk.default.root_get`](#spryngtimeanalyticssdkdefaultroot_get)
  * [`spryngtimeanalyticssdk.default.users_post`](#spryngtimeanalyticssdkdefaultusers_post)

<!-- tocstop -->

## Requirements<a id="requirements"></a>

Python >=3.7

## Installing<a id="installing"></a>

```sh
pip install spryngtime-analytics-sdk-python-sdk==1.0.1
```

## Getting Started<a id="getting-started"></a>

```python
from pprint import pprint
from spryngtime_analytics_sdk import SpryngtimeAnalyticsSdk, ApiException

spryngtimeanalyticssdk = SpryngtimeAnalyticsSdk(
    api_key="YOUR_API_KEY",
)

try:
    # Track usage data
    spryngtimeanalyticssdk.usage_tracking.track_usage(
        key="string_example",
        open_ai_response={
            "id": "id_example",
            "object": "object_example",
            "created": 1,
            "model": "model_example",
            "choices": [
                {
                    "index": 1,
                    "message": {
                        "role": "role_example",
                        "content": "content_example",
                    },
                    "finish_reason": "finish_reason_example",
                }
            ],
            "usage": {
                "prompt_tokens": 1,
                "completion_tokens": 1,
                "total_tokens": 1,
            },
        },
        usage={
            "prompt_tokens": 1,
            "completion_tokens": 1,
            "total_tokens": 1,
        },
    )
except ApiException as e:
    print("Exception when calling UsageTrackingApi.track_usage: %s\n" % e)
    pprint(e.body)
    pprint(e.headers)
    pprint(e.status)
    pprint(e.reason)
    pprint(e.round_trip_time)
```

## Async<a id="async"></a>

`async` support is available by prepending `a` to any method.

```python
import asyncio
from pprint import pprint
from spryngtime_analytics_sdk import SpryngtimeAnalyticsSdk, ApiException

spryngtimeanalyticssdk = SpryngtimeAnalyticsSdk(
    api_key="YOUR_API_KEY",
)


async def main():
    try:
        # Track usage data
        await spryngtimeanalyticssdk.usage_tracking.atrack_usage(
            key="string_example",
            open_ai_response={
                "id": "id_example",
                "object": "object_example",
                "created": 1,
                "model": "model_example",
                "choices": [
                    {
                        "index": 1,
                        "message": {
                            "role": "role_example",
                            "content": "content_example",
                        },
                        "finish_reason": "finish_reason_example",
                    }
                ],
                "usage": {
                    "prompt_tokens": 1,
                    "completion_tokens": 1,
                    "total_tokens": 1,
                },
            },
            usage={
                "prompt_tokens": 1,
                "completion_tokens": 1,
                "total_tokens": 1,
            },
        )
    except ApiException as e:
        print("Exception when calling UsageTrackingApi.track_usage: %s\n" % e)
        pprint(e.body)
        pprint(e.headers)
        pprint(e.status)
        pprint(e.reason)
        pprint(e.round_trip_time)


asyncio.run(main())
```

## Raw HTTP Response<a id="raw-http-response"></a>

To access raw HTTP response values, use the `.raw` namespace.

```python
from pprint import pprint
from spryngtime_analytics_sdk import SpryngtimeAnalyticsSdk, ApiException

spryngtimeanalyticssdk = SpryngtimeAnalyticsSdk(
    api_key="YOUR_API_KEY",
)

try:
    # Track usage data
    track_usage_response = spryngtimeanalyticssdk.usage_tracking.raw.track_usage(
        key="string_example",
        open_ai_response={
            "id": "id_example",
            "object": "object_example",
            "created": 1,
            "model": "model_example",
            "choices": [
                {
                    "index": 1,
                    "message": {
                        "role": "role_example",
                        "content": "content_example",
                    },
                    "finish_reason": "finish_reason_example",
                }
            ],
            "usage": {
                "prompt_tokens": 1,
                "completion_tokens": 1,
                "total_tokens": 1,
            },
        },
        usage={
            "prompt_tokens": 1,
            "completion_tokens": 1,
            "total_tokens": 1,
        },
    )
    pprint(track_usage_response.headers)
    pprint(track_usage_response.status)
    pprint(track_usage_response.round_trip_time)
except ApiException as e:
    print("Exception when calling UsageTrackingApi.track_usage: %s\n" % e)
    pprint(e.body)
    pprint(e.headers)
    pprint(e.status)
    pprint(e.reason)
    pprint(e.round_trip_time)
```


## Reference<a id="reference"></a>
### `spryngtimeanalyticssdk.usage_tracking.track_usage`<a id="spryngtimeanalyticssdkusage_trackingtrack_usage"></a>

Track usage data

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
spryngtimeanalyticssdk.usage_tracking.track_usage(
    key="string_example",
    open_ai_response={
        "id": "id_example",
        "object": "object_example",
        "created": 1,
        "model": "model_example",
        "choices": [
            {
                "index": 1,
                "message": {
                    "role": "role_example",
                    "content": "content_example",
                },
                "finish_reason": "finish_reason_example",
            }
        ],
        "usage": {
            "prompt_tokens": 1,
            "completion_tokens": 1,
            "total_tokens": 1,
        },
    },
    usage={
        "prompt_tokens": 1,
        "completion_tokens": 1,
        "total_tokens": 1,
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### key: `str`<a id="key-str"></a>

##### open_ai_response: [`OpenAiResponse`](./spryngtime_analytics_sdk/type/open_ai_response.py)<a id="open_ai_response-openairesponsespryngtime_analytics_sdktypeopen_ai_responsepy"></a>


##### usage: [`UsageDetail`](./spryngtime_analytics_sdk/type/usage_detail.py)<a id="usage-usagedetailspryngtime_analytics_sdktypeusage_detailpy"></a>


#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`TrackUsageRequest`](./spryngtime_analytics_sdk/type/track_usage_request.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/trackUsage` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `spryngtimeanalyticssdk.default.root_get`<a id="spryngtimeanalyticssdkdefaultroot_get"></a>

Home

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
spryngtimeanalyticssdk.default.root_get()
```

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `spryngtimeanalyticssdk.default.users_post`<a id="spryngtimeanalyticssdkdefaultusers_post"></a>

Adds a new user

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
spryngtimeanalyticssdk.default.users_post(
    id=10,
    name="Jessica Smith",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `int`<a id="id-int"></a>

##### name: `str`<a id="name-str"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`Any`](./spryngtime_analytics_sdk/type/typing_any.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/users` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---


## Author<a id="author"></a>
This Python package is automatically generated by [Konfig](https://konfigthis.com)
