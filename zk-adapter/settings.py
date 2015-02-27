import logging

LOGGERS = {
    'zk.watcher':{
        'level':'DEBUG'
    },
    'kazoo.client':{
        'level':'DEBUG'
    },
    'kazoo.recipe.watchers': {
        'level':'DEBUG'
    },
}


def init():
    # logging configuration
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    for name, meta in LOGGERS.items():
        watcher = logging.getLogger(name)
        watcher.setLevel(getattr(logging, meta.get('level', 'ERROR')))
        watcher.addHandler(ch)


ZK_RETRY = {
    'max_tries': -1
}
