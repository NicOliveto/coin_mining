from urllib.parse import urlencode

class ApiRequestBuilder:
    def __init__(self):
        self.base_url = None
        self.endpoint = None
        self.path_params = {}
        self.query_params = {}
        self.headers = {}

    def set_base_url(self, base_url):
        self.base_url = base_url
        return self

    def set_endpoint(self, endpoint):
        self.endpoint = endpoint
        return self

    def set_path_param(self, key, value):
        self.path_params[key] = value
        return self

    def add_query_param(self, key, value):
        self.query_params[key] = value
        return self

    def add_header(self, key, value):
        self.headers[key] = value
        return self

    def build(self):
        if not self.base_url:
            raise ValueError("Not base url defined")

        if self.endpoint:
            self.base_url = f"{self.base_url}{self.endpoint}"

        url = self.base_url.format(**self.path_params)

        query_string = urlencode(self.query_params)
        if query_string:
            url = f"{url}?{query_string}"

        return {"url": url, "headers": self.headers}
