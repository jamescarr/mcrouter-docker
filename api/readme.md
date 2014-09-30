# mcrouter API

## Endpoints


* `POST /config` - put a configuration wholesale. This will overwrite
any existing config.

Example:

```
POST /config
{
  "pools": {
    "A": {
      "servers": [
        "172.17.0.2:11211",
        "172.17.0.3:11211"
      ]
    }
  },
  "route": "PoolRoute|A"
}
```

* `GET /config` - gets the entire configuration!

### The following are unimplemented

* `POST /config/pool` - creates a new pool

Example 

```
POST /config/pool
{
    "A": {
      "servers": [
        "172.17.0.2:11211",
        "172.17.0.3:11211"
      ]
    }
}
```


* `PUT /config/pool/A` - update a pool

Example

```
PUT /config/pool/A

"172.17.0.4:11211"

```


* `DELETE /config/pool/A` - delete a pool
* `DELETE /config/pool/A/172.17.0.4:11211` - remove a backend from a pool


### Routes

* `POST /config/route` - adds a route
```
PUT /config/route

{
    "type": "PoolRoute",
    "pool": "production",
    "shadows": [
      {
        "target": "PoolRoute|test",
        "index_range": [0, 2],
        "key_fraction_range": [0, 0.1]
      }
    ]
  }

```

* `GET /config/route` - list all routes





