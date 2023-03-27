# Proxy Port Python `requests` wrapper
About <a href="https://proxy-port.com/en/scraping-proxy" target="_blank">Proxy Port</a>
## Prerequisites
To use this package you will need a free API key. Get your AIP key <a href="https://account.proxy-port.com/scraping" target="_blank">here</a>.
Detailed instructions <a href="https://proxy-port.com/en/scraping-proxy/getting-started" target="_blank">here</a>.
## Installation
Install via <a href="https://pip.pypa.io/" target="_blank">pip</a>:
```shell
$ pip install requests-proxyport
```
## Getting Started
Before you get your first proxy, you need to assign an API key.
This can be done either through an environment variable
```shell
$ export PROXY_PORT_API_KEY=<API_KEY>
```
or directly in the code.
```python
from requests_proxyport import Session

session = Session(proxyport_api_key='<API_KEY>') # here
r = session.get('https://example.com/')
print(r.text)

```
