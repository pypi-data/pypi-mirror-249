import typing_extensions

from spryngtime_analytics_sdk.paths import PathValues
from spryngtime_analytics_sdk.apis.paths.track_usage import TrackUsage
from spryngtime_analytics_sdk.apis.paths.root import Root
from spryngtime_analytics_sdk.apis.paths.users import Users

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.TRACK_USAGE: TrackUsage,
        PathValues._: Root,
        PathValues.USERS: Users,
    }
)

path_to_api = PathToApi(
    {
        PathValues.TRACK_USAGE: TrackUsage,
        PathValues._: Root,
        PathValues.USERS: Users,
    }
)
