"""The XMLRPC client."""

import xmlrpc.client
from typing import Any

from aiohttp import ClientSession


class XMLRPCClient:
    """Represent a XMLRPC client."""

    def __init__(self, session: ClientSession, url: str = "/xmlrpc.cgi"):
        """Initialize the XMLRPC client."""
        self._session = session
        self._url = url

    async def call(self, method_name: str, params: tuple = ()) -> Any:
        """Call a XML-RPC method."""
        xmlrequest = xmlrpc.client.dumps(methodname=method_name, params=params)
        async with self._session.post(url=self._url, data=xmlrequest) as response:
            response.raise_for_status()
            xmlresponse = xmlrpc.client.loads((await response.read()).decode("utf-8"))
            return xmlresponse[0][0]
