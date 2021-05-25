from __future__ import annotations
from typing import TypeVar
from validators import url as is_url

from actionpack import Action
from actionpack.action import K
from actionpack.action import T


Session = TypeVar('Session')
Request = TypeVar('Request')
Response = TypeVar('Response')


class MakeRequest(Action[T, K], requires=('requests',)):

    methods = ('CONNECT', 'GET', 'DELETE', 'HEAD', 'OPTIONS', 'PATCH', 'POST', 'PUT', 'TRACE')

    def __init__(self, method: str, url: str, data: dict = None, headers: dict = None, session: Session = None):
        self.method = method.upper()
        self.url = url
        self.method = method
        self.data = data
        self.headers = headers
        self.session = session

    def prepare(self, method: str, url: str, data: dict = None, headers=None) -> Request:
        return self.requests.Request(method, url, data=data, headers=headers).prepare()

    def instruction(self) -> Response:
        request = self.prepare(self.method, self.url, self.data, self.headers)
        return (self.session if self.session else self.requests.Session()).send(request)

    def validate(self) -> MakeRequest[T, K]:
        if self.method not in self.methods:
            raise ValueError(f'Invalid HTTP method: {self.method}')
        url_validation = is_url(self.url)
        if url_validation is not True:
            raise url_validation
        return self
