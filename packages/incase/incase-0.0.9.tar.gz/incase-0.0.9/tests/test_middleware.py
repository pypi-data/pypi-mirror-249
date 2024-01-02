from unittest import TestCase, main

from incase.middleware import JSONCaseTranslatorMiddleware
from starlette.applications import Starlette
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route
from starlette.testclient import TestClient

CORS_HEADERS = {
    "access-control-allow-origin": "*",  # Allows any origin
    "access-control-allow-methods": "POST, GET, OPTIONS, PUT, DELETE",  # Allowed methods
    "access-control-allow-headers": "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With",  # Allowed headers
}


def plain_text_endpoint(request):
    return PlainTextResponse("hello world!")


def generic_get(request):
    if request.headers["camelCase"] != "yes":
        raise ValueError("Where did my header go?")
    return JSONResponse({"first_thing": 1, "second_thing": 2})


async def greeting(request):
    data = await request.json()
    first_name = data["first_name"]
    last_name = data["last_name"]
    message = {"hello": f"{first_name} {last_name}"}
    return JSONResponse(message, headers=CORS_HEADERS)


routes = [
    Route("/", plain_text_endpoint),
    Route("/json", generic_get),
    Route("/greeting", endpoint=greeting, methods=["POST"]),
]

app = Starlette(debug=True, routes=routes)

app.add_middleware(JSONCaseTranslatorMiddleware)

client = TestClient(app)


class TestCaseTranslateMiddleware(TestCase):
    def test_plain_text(self):
        response = client.get("/", headers={"camelCase": "yes"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "hello world!")

    def test_get(self):
        response = client.get("/json", headers={"camelCase": "yes"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"firstThing": 1, "secondThing": 2})

    def test_post(self):
        response = client.post(
            "/greeting",
            json={"firstName": "Patrick", "lastName": "Shechet"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"hello": "Patrick Shechet"})
        for key, value in CORS_HEADERS.items():
            self.assertEqual(value, response.headers[key])


if __name__ == "__main__":
    main()
