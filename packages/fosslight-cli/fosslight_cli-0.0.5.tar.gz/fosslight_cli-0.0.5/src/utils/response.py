from requests import Response


def check_response(response: Response):
    assert response.ok, f"Response error\n- url: {response.url} ({response.request.method})\n- status: {response.status_code}\n- content: {response.text}"
