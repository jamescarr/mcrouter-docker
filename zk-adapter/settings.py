import logging

def init():
    # logging configuration
    watcher = logging.getLogger('zk.watcher')

    watcher.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    watcher.addHandler(ch)


ZK_RETRY = {
    'max_tries': -1
}
