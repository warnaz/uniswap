import re
from enum import Enum


class Proxy:
    def __init__(self, proxy: str):
        self.proxy = proxy
        self.validate()

    @property
    def session_proxy(self):
        if self.proxy:
            return {
                'http': f'http://{self.proxy}',
                'https': f'http://{self.proxy}'
            }

    @property
    def w3_proxy(self):
        if self.proxy:
            return f'http://{self.proxy}'

    def __getattr__(self, item):
        return self.__dict__[item] if self.__dict__['proxy'] else None

    def validate(self):
        if self.proxy:
            pattern = r'^.+:.+@.+:\d+$'
            if not re.fullmatch(pattern, self.proxy):
                raise ValueError('Proxy format is not valid', self.proxy)

    def __repr__(self):
        return f'Proxy <{self.proxy}>' if self.proxy else 'No proxy found'

