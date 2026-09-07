import requests

class HotelAPIClient:
    def __init__(self, base_url='http://127.0.0.1:8000'):
        self.base_url = base_url.rstrip('/')

    def _url(self, service, path=''):
        return f"{self.base_url}/{service}{('/' + path.lstrip('/')) if path else ''}"

    def _json_or_error(self, response):
        if response.status_code >= 400:
            detail = None
            try:
                data = response.json()
                detail = data.get('detail') if isinstance(data, dict) else data
            except Exception:
                detail = response.text
            raise RuntimeError(str(detail or response.reason))
        if not response.content:
            return {}
        return response.json()

    def get(self, service, path='', **params):
        response = requests.get(self._url(service, path), params={k:v for k,v in params.items() if v not in (None, '')}, timeout=5)
        return self._json_or_error(response)

    def post(self, service, path='', data=None):
        response = requests.post(self._url(service, path), json=data or {}, timeout=5)
        return self._json_or_error(response)

    def put(self, service, path='', data=None):
        response = requests.put(self._url(service, path), json=data or {}, timeout=5)
        return self._json_or_error(response)

    def delete(self, service, path=''):
        response = requests.delete(self._url(service, path), timeout=5)
        return self._json_or_error(response)
