import typing_extensions

from spryngtime_analytics_sdk.apis.tags import TagValues
from spryngtime_analytics_sdk.apis.tags.usage_tracking_api import UsageTrackingApi
from spryngtime_analytics_sdk.apis.tags.default_api import DefaultApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.USAGE_TRACKING: UsageTrackingApi,
        TagValues.DEFAULT: DefaultApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.USAGE_TRACKING: UsageTrackingApi,
        TagValues.DEFAULT: DefaultApi,
    }
)
