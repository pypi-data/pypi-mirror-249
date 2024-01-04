import abc

from . import ulist


class Options(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __call__(self, data):
        pass


class Status(Options):
    def __init__(self, *status: int):
        super().__init__()
        self.status = list(status)

    def __call__(self, data):
        if len(self.status) == 0:
            return

        if not isinstance(data, dict):
            return

        data["status"] = f"[{ulist.join(self.status, ',', True)}]"


class MediaType(Options):
    def __init__(self, *media_type: str):
        super().__init__()
        self.media_type = list(media_type)

    def __call__(self, data):
        if len(self.media_type) == 0:
            return

        if not isinstance(data, dict):
            return

        data["mediaType"] = f"[{ulist.join(self.media_type, ',', True)}]"


class Page(Options):
    def __init__(self, page: int, page_size: int):
        super().__init__()
        self.page = page
        self.page_size = page_size

    def __call__(self, data):
        if self.page <= 0:
            return

        if self.page_size <= 0:
            return

        if not isinstance(data, dict):
            return

        data["page"] = self.page
        data["pagesize"] = self.page_size


class Src(Options):
    def __init__(self, src: str):
        super().__init__()
        self.src = src

    def __call__(self, data):
        if len(self.src) <= 0:
            return

        if not isinstance(data, dict):
            return

        data["src"] = self.src


class Name(Options):
    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def __call__(self, data):
        if len(self.name) <= 0:
            return

        if not isinstance(data, dict):
            return

        data["name"] = self.name
