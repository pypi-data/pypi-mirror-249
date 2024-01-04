from . import controller
from . import options as options


class LiveCode(controller.Controller):
    def get_list(self, *opt: options.Options):
        val = {}
        for o in opt:
            o(val)

        data, _ = self.c.send_get_requests("/api/v1/user/livecode/list", val)
        return data

    def get_info(self, *opt: options.Options):
        val = {}
        for o in opt:
            o(val)

        data, _ = self.c.send_get_requests("/api/v1/user/livecode", val)
        return data

    def create(self, *opt: options.Options, **req_data):
        for o in opt:
            o(req_data)

        resp_data, _ = self.c.send_post_requests(req_data, "/api/v1/user/livecode/create")
        return resp_data

    def create_by_dict(self, req_data: dict, *opt: options.Options):
        for o in opt:
            o(req_data)

        resp_data, _ = self.c.send_post_requests(req_data, "/api/v1/user/livecode/create")
        return resp_data

    def update(self, *opt: options.Options, **req_data):
        for o in opt:
            o(req_data)

        resp_data, _ = self.c.send_post_requests(req_data, "/api/v1/user/livecode/update")
        return resp_data

    def update_by_dict(self, req_data: dict, *opt: options.Options):
        for o in opt:
            o(req_data)

        resp_data, _ = self.c.send_post_requests(req_data, "/api/v1/user/livecode/update")
        return resp_data

    def delete(self, project_id: str, *opt: options.Options):
        req_data = {
            "id": project_id,
        }

        for o in opt:
            o(req_data)

        resp_data, _ = self.c.send_post_requests(req_data, "/api/v1/user/livecode/delete")
        return resp_data
