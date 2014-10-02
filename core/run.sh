#!/bin/bash

main() {
  PORT=${MCROUTER_PORT-5000}
  LOG_PATH=${MCROUTER_LOG_PATH-/var/mcrouter}
  
  /usr/local/bin/mcrouter --config-file /etc/mcrouter/mcrouter.json -p $PORT -L $LOG_PATH

}

main
