from . import client


class Controller:
    def __init__(self, c: client.Client):
        self.c = c
