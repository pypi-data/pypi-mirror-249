# Webmin XML-RPC python package

This package provides a python interface to interact with the Webmin XML-RPC API.

## Usage

```python
from aiohttp.client import ClientSession
from webmin_xmlrpc.client import WebminInstance
from yarl import URL

base_url = URL.build(host="example.com", scheme="https")
session = Clientsession(base_url)
instance = WebminInstance(session)

async def get_data():
    data = await instance.update()
```

## Exposed data

- Load (1m, 5m, 15m)
- Network interfaces
- Memory information
- Uptime
- Local disk space information
