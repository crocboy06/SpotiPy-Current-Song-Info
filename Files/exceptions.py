class CurrentlyPlayingType(Exception):
    pass
class NoTrack(Exception):
    pass
class RateLimitExceeded(Exception):
    pass
class TokenExpired(Exception):
    #"The access token expired", "Invalid access token"
    pass
class TimestampInvalid(Exception):
    pass
class DJPlaying(Exception):
    pass
class TokenRefreshFailed(Exception):
    pass
class NoReply(Exception):
    pass
class ConnectionBad(Exception):
    pass
class OtherAPIError(Exception):
    pass
class ResponseCodeInvalid(Exception):
    pass
class NullID(Exception):
    pass
class JsonResponseError(Exception):
    pass
class TransferringPlayback(Exception):
    pass
class NoItem(Exception):
    pass