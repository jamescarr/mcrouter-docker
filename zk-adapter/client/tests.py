from unittest import TestCase
from time import sleep
from pymemcache.client import Client
from kazoo.client import KazooClient, KazooState
from os import environ as E
import json
import logging

log = logging.getLogger('mc.test')


log.info("host is {}".format(E['ZK_HOSTS']))
mc = Client((E['MC_HOST'], int(E['MC_PORT'])))
zk = KazooClient(hosts=E['ZK_HOSTS'])
zk.start()
PATH = E['ZK_CONFIG_PATH']

## additional caches
caches = [
    Client(('memcache0', 11211)),
    Client(('memcache1', 11211)),
    Client(('memcache2', 11211)),
    Client(('memcache3', 11211))
]

def set_safely(node, val):
    log.info("Setting it")
    if zk.exists(node):
        log.info("it exists")
        zk.set(node, json.dumps(val))
    else:
        zk.create(node, json.dumps(val), makepath=True)


def route(key):
    return mc.get('__mcrouter__.route(set,{})'.format(key))

class MCRouterSettingSwapperTestCase(TestCase):
    def tearDownClass():
        configuration = {
           "pools": {
             "A": {
               "servers": [
                   "memcache0:11211",
                   "memcache1:11211"
               ]
             }
           },
           "route": "PoolRoute|A"
         }

        set_safely(PATH, configuration)

    def test_sharding(self):
        configuration = {
           "pools": {
             "A": {
               "servers": [
                   "memcache0:11211",
                   "memcache1:11211"
               ]
             }
           },
           "route": "PoolRoute|A"
         }

        set_safely(PATH, configuration)
        sleep(2) # unfortunate :-(

        mc.delete_many(["b", "a"])
        sleep(0.5)
        mc.set("a", 22)
        mc.set("b", 44)

        sleep(0.5)

        self.assertEquals('22', caches[1].get('a')) # no serialization :-/
        self.assertEquals('44', caches[0].get('b'))

        ## cleanup
        mc.delete_many(["b", "a"])

        self.assertEquals({}, mc.get_many(['a', 'b']))

    def test_replication(self):
        return

    def test_multi_cluster_broadcasting(self):
        configuration = {
           "pools": {
             "A": {
               "servers": [
                   "memcache0:11211"
               ]
             },
             "B": {
               "servers": [
                   "memcache1:11211"
               ]
             },
             "C": {
                "servers": [
                   "memcache2:11211"
                ]
            }
           },
           "route": {
                 "type": "PrefixSelectorRoute",
                 "policies": {
                   "/a": "PoolRoute|A",
                   "/b": "PoolRoute|B",
                   "/c": "PoolRoute|C"
                 }
             }
         }

        set_safely(PATH, configuration)
        sleep(2)

        mc.set("/a/skaro", "foo")
        mc.set("/b/skaro", "bar")
        mc.set("/c/skaro", "baz")
        sleep(0.5)

        # alright, let's read from each backend!
        self.assertEquals('foo', caches[0].get('/a/skaro'))
        self.assertEquals('bar', caches[1].get('/b/skaro'))
        self.assertEquals('baz', caches[2].get('/c/skaro'))

        mc.delete_many(['/a/skaro', '/b/skaro', '/c/skaro'])


    def test_warming(self):
        configuration = {
           "pools": {
             "A": {
               "servers": [
                   "memcache0:11211",
                   "memcache1:11211"
               ]
             },
             "B": {
                "servers": [
                   "memcache2:11211"
                ]
            }
           },
           "routes": [{
             "type": "WarmUpRoute",
             "warm": "PoolRoute|A",
             "cold": "PoolRoute|B"
           }]
         }

        set_safely(PATH, configuration)
        sleep(2)

        mc.set("a", 22)
        mc.set("b", 44)

        print(route("a"))
        print(route("b"))
        sleep(1)

        self.assertEquals('22', caches[1].get('a')) # no serialization :-/
        self.assertEquals('44', caches[0].get('b'))
        self.assertEquals({'a': '22', 'b': '44'}, caches[2].get_many(['a','b']))
        
        mc.delete_many(["b", "a"])
        self.assertEquals({}, mc.get_many(['a', 'b']))

        # the warm up cache should retain the values stored
        self.assertEquals({'a': '22', 'b': '44'}, caches[2].get_many(['a','b']))

        # now lets clear them out for the next test!
        caches[2].delete_many(['a','b'])





