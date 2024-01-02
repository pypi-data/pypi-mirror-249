import json
import typing

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from incase import Case, Caseless, keys_case

RequestResponseEndpoint = typing.Callable[[Request], typing.Awaitable[Response]]


class camelJsonResponse(JSONResponse):
    def render(self, content: typing.Any) -> bytes:
        return json.dumps(keys_case(content, Case.CAMEL)).encode("utf-8")


async def make_camel_json(response: Response) -> Response:
    header = response.headers
    del header["content-length"]
    content = None
    async for chunk in response.body_iterator:
        if content is not None:  # Already have some content
            raise NotImplementedError("Streaming the response body isn't supported yet")
        if isinstance(chunk, bytes):
            content = chunk.decode("utf-8")
        else:
            content = chunk
    return camelJsonResponse(
        content=json.loads(content),
        status_code=response.status_code,
        headers=header,
        media_type=response.media_type,
        background=response.background,
    )


class JSONCaseTranslatorMiddleware(BaseHTTPMiddleware):
    """This middleware translates the case of json keys recieved and sent by the
    asgi app. It is helpful for allowing a python back-end to use snake_case
    while allowing a javascript front end to use camelCase."""

    def __init__(self, app, handle_response: bool = True):
        super().__init__(app)
        self.handle_response = handle_response

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        try:
            body = await request.body()
            data = json.loads(body)
            request._body = json.dumps(keys_case(data, Case.SNAKE)).encode(
                encoding="utf-8"
            )
            request.content_length = len(request._body)
        except json.JSONDecodeError:
            pass  # guess it wasn't json

        response = await call_next(request)
        if (
            self.handle_response
            and response.headers.get("content-type") == "application/json"
        ):
            new_response = await make_camel_json(response)
            return new_response
        else:
            return response
