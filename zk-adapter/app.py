from kazoo.client import KazooClient, KazooState
from kazoo.retry import KazooRetry

from time import sleep
import logging
import settings

zk = None

log = logging.getLogger('zk.watcher')

def watcher(hosts, config_path, output):
    zk = KazooClient(connection_retry=settings.ZK_RETRY,
            command_retry=settings.ZK_RETRY,
            logger=log,
            hosts=hosts,
            read_only=True)
    zk.start()

    @zk.DataWatch(config_path)
    def watch_node(data, stat):
        if data is not None:
            data = data.decode("utf-8")
            if validate(data):
                update_config(data, output)

def validate(data):
    # simple json verifier, could make this clever later
    try:
        json.loads(data)
        return True
    except Error:
        return False

def update_config(data, output):
    f = open(output, 'w')
    f.write(data)
    f.close()
    log.info("Wrote output to {}".format(output), extra={'content':data})


if __name__ == '__main__':
    import signal
    import time
    from os import environ as env

    def shutdown():
        client.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)

    try:
        settings.init()
        log.info("app started!")
        watcher(env['ZK_HOSTS'], env['ZK_CONFIG_PATH'], env['ZK_CONFIG_OUTPUT'])
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        shutdown()
