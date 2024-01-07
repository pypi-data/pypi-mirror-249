import json

class RawHTTPy:
    def __init__(self, req:str, ssl:bool=True) -> None:
        self._req:str = req
        self.ssl:bool = ssl
        self.method:str = self._parse_method()
        self.headers:dict = self._parse_headers()
        self.host:str = self._parse_host()
        self.path:str = self._parse_path()
        self.http_version:str = self._parse_http_version()
        self.url:str = self._parse_url()
        self.body:dict = self._parse_body()

    def _parse_method(self):
        return self._req.split(' ')[0]
    
    def _parse_headers(self):
        headers = {}
        for l in self._req.split('\n')[1::]:
            if l != '':
                key, value = l.split(': ', 1)
                headers[key] = value
            else:
                return headers
        return headers

    def _parse_host(self):
        if 'Host' in self.headers:
            return self.headers['Host']
        else:
            return None

    def _parse_path(self):
        return self._req.split(' ')[1]
    
    def _parse_http_version(self):
        first_line = self._req.split('\n')[0]
        return first_line.split(' ')[2]
    
    def _parse_url(self):
        protocol = 'https://'
        if not self.ssl: 
            protocol = 'http://'
        url = protocol + self.host + self.path
        return url
    
    def _parse_body(self):
        lines = self._req.split('\n')
        empty_dict = {}
        try:
            empty_line = lines.index("")
        except Exception:
            return empty_dict
        if empty_line < (len(lines) -1):
            body_list = lines[empty_line +1::]
            body = '\n'.join(body_list)
            # tries JSON parsing
            try:
                json_body = json.loads(body)
                return json_body
            except ValueError:
                body_dict = {}
                # if it fails tries raw data parsing
                try:
                    key_values = body.split("&")
                    for kv in key_values:
                        k, v = kv.split("=")
                        body_dict[k] = v
                    return body_dict
                except Exception as e:
                    return empty_dict
        else:
            return empty_dict
        