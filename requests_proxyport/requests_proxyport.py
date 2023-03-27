from collections import OrderedDict

import requests
from proxyport2 import get_proxy, set_api_key


class Session:
    current_session = None

    def __init__(self, proxyport_api_key=None):
        self.adapters = OrderedDict()
        if proxyport_api_key:
            set_api_key(proxyport_api_key)
        self.get_session()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        if self.current_session:
            self.current_session.close()

    def get_session(self, renew=False):
        if self.current_session and not renew:
            return self.current_session
        return self._get_session()

    def _get_session(self):
        s = requests.Session()
        for (prefix, adapter) in self.adapters.items():
            s.mount(prefix, adapter)
        proxy = get_proxy()
        proxies = {'http': f'http://{proxy}',
                   'https': f'http://{proxy}'}
        s.proxies.update(proxies)
        self.current_session = s
        return s

    def request(self, method, url, **kwargs):
        max_retries = 20
        retry = 0
        renew = False
        while retry < max_retries:
            try:
                kwargs.setdefault('timeout', 10)
                return self.get_session(renew).request(method, url, **kwargs)
            except Exception as e:
                print(e)
                retry += 1
                renew = True

    def get(self, url, **kwargs):
        kwargs.setdefault("allow_redirects", True)
        return self.request("GET", url, **kwargs)

    def options(self, url, **kwargs):
        kwargs.setdefault("allow_redirects", True)
        return self.request("OPTIONS", url, **kwargs)

    def head(self, url, **kwargs):
        kwargs.setdefault("allow_redirects", False)
        return self.request("HEAD", url, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        return self.request("POST", url, data=data, json=json, **kwargs)

    def put(self, url, data=None, **kwargs):
        return self.request("PUT", url, data=data, **kwargs)

    def patch(self, url, data=None, **kwargs):
        return self.request("PATCH", url, data=data, **kwargs)

    def delete(self, url, **kwargs):
        return self.request("DELETE", url, **kwargs)

    def mount(self, prefix, adapter):
        self.adapters[prefix] = adapter
        keys_to_move = [k for k in self.adapters if len(k) < len(prefix)]

        for key in keys_to_move:
            self.adapters[key] = self.adapters.pop(key)
        self.current_session.mount(prefix, adapter)

    def close(self):
        if self.current_session:
            self.current_session.close()

    def __getattribute__(self, item):
        if item in list(set(requests.Session.__attrs__) - {'adapters'}):
            return self.current_session.__getattribute__(item)
        return super().__getattribute__(item)

    def __setattr__(self, name, value):
        if name in list(set(requests.Session.__attrs__) - {'adapters'}):
            self.current_session.__setattr__(name, value)
            return
        super().__setattr__(name, value)
