## Hashed Sharding

Sharding is dependent on host location in the server list.

```json
{
   "pools": {
     "A": {
       "servers": [
         // your destination memcached boxes here, e.g.:
         "127.0.0.1:12345",
         "[::1]:12346"
       ]
     }
   },
   "route": "PoolRoute|A"
 }

```

## Replicated Pools

```json

 {
   "pools": {
      "A": {
         "servers": [
            // hosts of replicated pool, e.g.:
           "127.0.0.1:12345",
           "[::1]:12346"
         ]
      }
   },
   "route": {
     "type": "OperationSelectorRoute",
     "operation_policies": {
       "delete": "AllSyncRoute|Pool|A",
       "add": "AllSyncRoute|Pool|A",
       "get": "LatestRoute|Pool|A",
       "set": "AllSyncRoute|Pool|A"
     }
   }
 }

```

## Prefix Routing

```json
 {
   "pools": {
     "workload1": { "servers": [ /* list of cache hosts for workload1 */ ] },
     "workload2": { "servers": [ /* list of cache hosts for workload2 */ ] },
     "common_cache": { "servers": [ /* list of cache hosts for common use */ ] }
   },
   "route": {
     "type": "PrefixSelectorRoute",
     "policies": {
       "a": "PoolRoute|workload1",
       "b": "PoolRoute|workload2"
     },
     "wildcard": "PoolRoute|common_cache"
   }
 }
```

Explanation: requests with key prefix "a" will be sent to pool 'workload1', requests with key prefix "b" will be sent to pool 'workload2'. Other requests will be sent to pool 'common_cache'. So key "abcd" will be sent to 'workload1'; "bar" to 'workload2'; "zzz" to 'common_cache'.



## Shadowing
```

{
  "pools": {
    "production": {
      "servers": [ /* production hosts */ ]
    },
    "test": {
      "servers": [ /* test hosts */ ]
    }
  },
  "route": {
    "type": "PoolRoute",
    "pool": "production",
    "shadows": [
      {
        "target": "PoolRoute|test",
        // shadow traffic that would go to first and second hosts in 'production' pool
        // note that the endpoint is non-inclusive
        "index_range": [0, 2],
        // shadow requests for 10% of keys based on key hash
        "key_fraction_range": [0, 0.1]
      }
    ]
  }
}

```

## Cold Cache Warm Up

```json

 {
   "pools": {
     "cold": { "servers": [ /* cold hosts */ ] },
     "warm": { "servers": [ /* warm hosts */ ] }
   },
   "route": {
     "type": "WarmUpRoute",
     "cold": "PoolRoute|cold",
     "warm": "PoolRoute|warm"
   }
 }

```

## Multi-Cluster Broadcasting


```JavaScript
{
  "pools": {
    "A": {
      "servers": [ /* hosts of pool A */ ]
    },
    "B": {
      "servers": [ /* hosts of pool B */ ]
    }
  },
  "routes": [
    {
      "aliases": [
        "/a/a/",
        "/A/A/"
      ],
      "route": "PoolRoute|A"
    },
    {
      "aliases": [
        "/b/b/"
      ],
      "route": "PoolRoute|B"
    }
  ]
}
```


_Explanation_: routing prefixes allow organizing pools into distinct clusters, and multiple clusters into datacenters. More about routing prefix concept [here](Routing-Prefix). In this example, commands sent to mcrouter `get /a/a/key` and `get /A/A/other_key` are served by servers in pool A (as `get key` and `get other_key` respectively), while `get /b/b/yet_another_key` will be served by servers in pool B (which will see `get yet_another_key`). Broadcast request `delete /*/*/one_more_key` will be sent to both pool A and pool B (as `delete one_more_key`).

