import json

import allure
from requests import Session


class ApiSession:
    def __init__(self, session: Session):
        self.session = session

    def _send(self, method: str, url: str, **kwargs):
        response = self.session.request(method=method, url=url, **kwargs)
        if isinstance(response.request.body, bytes):
            body = response.request.body.decode(encoding="utf-8")
        else:
            body = response.request.body
        allure.attach(
            body=f"Request: \n"
                 f"URL: {response.request.url}\n"
                 f"Headers: {json.dumps(dict(response.request.headers), indent=4, ensure_ascii=False)}\n"
                 f"Body: {json.dumps(body, indent=4, ensure_ascii=False)}\n"
                 f"Response: \n"
                 f"Status code: {response.status_code}\n"
                 f"Headers: {json.dumps(dict(response.headers), indent=4, ensure_ascii=False)}\n"
                 f"Body: {json.dumps(response.json(), indent=4, ensure_ascii=False)}\n",
            name="Детальная информация о запросе и ответе",
            attachment_type=allure.attachment_type.TEXT,
        )
        return response

    @allure.step("GET-запрос к адресу {url}")
    def get(self, url: str, params: dict | None = None):
        return self._send("GET", url=url, params=params)

    @allure.step("POST-запрос к адресу {url}")
    def post(self, url: str, params: dict | None = None, json: dict | None = None):
        return self._send("POST", url=url, params=params, json=json)

    @allure.step("PATCH-запрос к адресу {url}")
    def patch(self, url: str, params: dict | None = None, json: dict | None = None):
        return self._send("PATCH", url=url, params=params, json=json)

    @allure.step("PUT-запрос к адресу {url}")
    def put(self, url: str, params: dict | None = None, json: dict | None = None):
        return self._send("PUT", url=url, params=params, json=json)
