import base64

from . import controller
from . import options as options


class LiveCode(controller.Controller):
    def get_list(self, *opt: options.Options):
        val = {}
        for o in opt:
            o(val)

        data, _ = self.c.send_get_requests("/api/v1/user/livecode/file/list", val)
        return data

    def get_url(self, file_id: str, *opt: options.Options):
        val = {}
        for o in opt:
            o(val)

        val["id"] = file_id

        _, resp = self.c.send_get_requests("/api/v1/user/livecode/file", val)

        return resp.headers.get("Location")

    def create(self, file: bytes, name: str, *opt: options.Options):
        req_data = {
            "file": f"base64:{base64.b64encode(file)}",
            "name": name,
        }

        for o in opt:
            o(req_data)

        resp_data, _ = self.c.send_post_requests(req_data, "/api/v1/user/livecode/file/update")
        return resp_data

    def create_by_file(self, file_path: bytes, name: str, *opt: options.Options):
        with open(file_path, "rb") as f:
            file = f.read()

        return self.create(file, name, *opt)

    def update_file_name(self, file_id: str, name: str, *opt: options.Options):
        req_data = {
            "fid": file_id,
            "name": name,
        }

        for o in opt:
            o(req_data)

        resp_data, _ = self.c.send_post_requests(req_data, "/api/v1/user/livecode/file/name/update")
        return resp_data

    def delete(self, file_id: str, *opt: options.Options):
        req_data = {
            "id": file_id,
        }

        for o in opt:
            o(req_data)

        resp_data, _ = self.c.send_post_requests(req_data, "/api/v1/user/livecode/file/delete")
        return resp_data
