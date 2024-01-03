# wikibase-rest-api-client
A client library for accessing Wikibase REST API generated automatically from the OpenAPI specification. See [the swagger UI](https://doc.wikimedia.org/Wikibase/master/js/rest-api/) for details of the API. Docs for the REST API can be at [doc.wikimedia.org](https://doc.wikimedia.org/Wikibase/master/php/repo_rest-api_README.html#autotoc_md670).

## Usage
First, create a client:

```python
from wikibase_rest_api_client import Client

# by default will connect to Wikidata at https://www.wikidata.org/w/rest.php/wikibase/v0/
client = Client()
# specify some other url to connect to
other_client = Client(base_url="https://api.example.com")
```

You probably should specify a User-Agent when constructing the client

```python
from wikibase_rest_api_client import Client
client = Client(headers={"User-Agent": "my-agent/1.0.0"})

```

If the endpoints you're going to hit require authentication, use `AuthenticatedClient` instead:

```python
from wikibase_rest_api_client import AuthenticatedClient

client = AuthenticatedClient(token="SuperSecretToken")
```

Now call your endpoint and use your models:

```python
from wikibase_rest_api_client.models import Item
from wikibase_rest_api_client.api.items import get_item
from wikibase_rest_api_client.types import Response

with client as client:
    # it's detailed because it responds with need more info than just the Item (e.g. status_code / headers)
    response: Response[Item] = get_item.sync_detailed(client=client)
```

Or do the same thing with an async version:

```python
from wikibase_rest_api_client.models import Item
from wikibase_rest_api_client.api.items import get_item
from wikibase_rest_api_client.types import Response

async with client as client:
    response: Response[Item] = await get_item.asyncio_detailed(client=client)
```

By default, when you're calling an HTTPS API it will attempt to verify that SSL is working correctly. Using certificate verification is highly recommended most of the time, but sometimes you may need to authenticate to a server (especially an internal server) using a custom certificate bundle.

```python
client = AuthenticatedClient(
    base_url="https://internal_api.example.com", 
    token="SuperSecretToken",
    verify_ssl="/path/to/certificate_bundle.pem",
)
```

You can also disable certificate validation altogether, but beware that **this is a security risk**.

```python
client = AuthenticatedClient(
    base_url="https://internal_api.example.com", 
    token="SuperSecretToken", 
    verify_ssl=False
)
```


## Advanced customizations

There are more settings on the generated `Client` class which let you control more runtime behavior, check out the docstring on that class for more info. You can also customize the underlying `httpx.Client` or `httpx.AsyncClient` (depending on your use-case):

```python
from wikibase_rest_api_client import Client

def log_request(request):
    print(f"Request event hook: {request.method} {request.url} - Waiting for response")

def log_response(response):
    request = response.request
    print(f"Response event hook: {request.method} {request.url} - Status {response.status_code}")

client = Client(
    base_url="https://api.example.com",
    httpx_args={"event_hooks": {"request": [log_request], "response": [log_response]}},
)

# Or get the underlying httpx client to modify directly with client.get_httpx_client() or client.get_async_httpx_client()
```

You can even set the httpx client directly, but beware that this will override any existing settings (e.g., base_url):

```python
import httpx
from wikibase_rest_api_client import Client

client = Client(
    base_url="https://api.example.com",
)
# Note that base_url needs to be re-set, as would any shared cookies, headers, etc.
client.set_httpx_client(httpx.Client(base_url="https://api.example.com", proxies="http://localhost:8030"))
```
