class HttpException(Exception):
    pass

class BadRequest(HttpException):
    """*400* `Bad Request`

    Raise if the browser sends something to the application the application
    or server cannot handle.
    """
    code = 400
    description = (
        'The browser (or proxy) sent a request that this server could '
        'not understand.'
    )
