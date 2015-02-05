# ZK Adapter
This is a simple app that watches a given path in zookeeper and updates
a specified configuration file with the data found at that path whenever
it changes.

## Environment Variables
The following environment variables are required:

* `ZK_HOSTS` - a string of hosts to connect to
* `ZK_CONFIG_PATH` - the paht in zookeeper to watch for changes
* `ZK_CONFIG_OUTPUT` - the file location to update on path change

## Local Development
An example is provided using fig to bootstrap zookeeper, mcrouter, 3
memcached servers and a single zkwatcher instance.

Type `fig up` to launch everything up, then navigate to `http://<boot2docker ip>:8080/exhibitor/v1/ui/index.html` 
to view mcrouter. Update the path `/us-east-1/mcrouter` to some proper
JSON text and you should see mcrouter reload configuration locally. You
should also see the config file updated under the
`$(pwd)/etc/mcrouter.json` directory.

## TODO
* Super generic - not coupled to mcrouter
* pluggable configuration validators
