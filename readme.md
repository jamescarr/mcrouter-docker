# Facebook's mcrouter
This is a docker image for facebook's mcrouter, built with blood, sweat
and a glass of scotch. Enjoy. 

## Usage

For now we simply expose the mcrouter command for your enjoyment by
directly interacting with it. Not sugar here!

```
docker run -p 5000:5000 jamescarr/mcrouter mcrouter --help

```


```
docker run -p 5000:5000 \
    jamescarr/mcrouter \
    mcrouter --config-str='{"pools":{"A":{"servers":["127.0.0.1:5001"]}},
                                           "route":"PoolRoute|A"}' \
                            -p 5000
```


## Wish List

Here's somethings that would be nice to add if possible!

- etcd support
- more fine grained configuration options
- easy access to debug commands

