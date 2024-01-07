# RawHTTPy

RawHTTPy is a Python package to parse raw HTTP requests into an object, ready to be used to send HTTP requests with web python libraries such as requests or httpx.

This library is very useful when you have to replicate an HTTP request inside your python code but it takes too long to write down all the headers and body parameters (plus all the lines of code it takes).

With RawHTTPy you can pass the raw request as a string to the RawHTTPy class. You will get back an object with the following properties:

- url
- host
- headers
- body
- path (url path)
- method
- http_version
- ssl (bool)

## NOTE

At the moment RawHTTPy only supports JSON and raw data bodies. It's not functional for file upload requests.

## Usage

### Python project

Let's assume we have captured a request with a web proxy (e.g. BurpSuite) and we pasted the HTTP request inside the file *raw_http_req.txt*.

```text
POST /login HTTP/2
Host: example.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0
Cookie: session=qwerty123456
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://duckduckgo.com/
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: cross-site
Sec-Fetch-User: ?1
If-Modified-Since: Sat, 30 Dec 2023 15:44:33 GMT
If-None-Match: "65903ae1-83ac"
Te: trailers

username=admin&password=pass
```

```python
from rawhttpy import RawHTTPy
import requests

# read the raw http request from a text file
with open("raw_http_req.txt", "r") as f:
    raw_req = f.read()

# initialize the RawHTTPy object
rh = RawHTTPy(raw_req)

# you can change all the fields before sending the request
rh.headers['User-Agent'] = 'RawHTTPy Mozilla/5.0'
rh.body['username'] = 'superadmin'
rh.body['password'] = 'securepass'

# add a new item to the body property
rh.body['login'] = '1'

# add a new header
rh.headers['X-MyHeader'] = 'xyz'

# send the request
res = requests.post(rh.url, headers=rh.headers, data=rh.body)
```

### CLI

You can run `rawhttpy {req_file}` from your CLI to check how the HTTP request will be parsed.
