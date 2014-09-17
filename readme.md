# mcrouter
This is a docker image for facebook's mcrouter, built with blood, sweat
and a glass of scotch. Enjoy. 

## Usage

For now we simply expose the mcrouter command for your enjoyment by
directly interacting with it. Not sugar here!

```
docker run -p 5000:5000 jamescarr/mcrouter:1.0 mcrouter --help

```

Or to run two memcache containers and proxy them with mcrouter!


```
$ sudo docker run --name memcached0 -d -p 11211 sylvainlasnier/memcached
$ sudo docker run --name memcached1 -d -p 11211 sylvainlasnier/memcached
$ sudo docker inspect -f "{{.NetworkSettings.IPAddress}}" memcached0

172.17.0.2

$ sudo docker inspect -f "{{.NetworkSettings.IPAddress}}" memcached1

172.17.0.3

$ sudo docker run -d -p 5000:5000     jamescarr/mcrouter:1.0     mcrouter 
      --config-str='{"pools":{"A":{"servers":["172.17.0.2:11211", "172.17.0.3:11211"]}},
                                           "route":"PoolRoute|A"}'                             
      -p 5000
      
```

Now we can use mcrouter as a regular memcache server!

```
agrant@vagrant-ubuntu-trusty-64:~/mcrouter$ telnet localhost 5000
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
stats
STAT version mcrouter 1.0
STAT commandargs --config-str={"pools":{"A":{"servers":["172.17.0.2:11211", "172.17.0.3:11211"]}},
                                           "route":"PoolRoute|A"} -p 5000
STAT child_pid 1
STAT parent_pid 0
STAT time 1410967072
STAT uptime 276
STAT num_servers 2
STAT num_servers_up 0
STAT num_servers_down 2
STAT num_clients 0
STAT server_up_events 0
STAT server_down_events 0
STAT closed_inactive_connections 0
STAT mcc_txbuf_reqs 0
STAT mcc_waiting_replies 0
STAT asynclog_requests 0
STAT sum_server_queue_length 0
STAT proxy_reqs_processing 1
STAT proxy_reqs_waiting 0
STAT rusage_system 0.162521
STAT rusage_user 0.103771
STAT ps_num_minor_faults 4159
STAT ps_num_major_faults 161
STAT ps_user_time_sec 0.1
STAT ps_system_time_sec 0.16
STAT ps_vsize 315949056
STAT ps_rss 13934592
STAT ps_open_fd 0
STAT fibers_allocated 0
STAT fibers_pool_size 0
STAT fibers_stack_high_watermark 0
STAT successful_client_connections 2
STAT duration_us 0
STAT cmd_delete_count 0
STAT cmd_get_count 0
STAT cmd_set_count 0
STAT cmd_delete_outlier_count 0
STAT cmd_delete_outlier_failover_count 0
STAT cmd_delete_outlier_shadow_count 0
STAT cmd_delete_outlier_all_count 0
STAT cmd_get_outlier_count 0
STAT cmd_get_outlier_failover_count 0
STAT cmd_get_outlier_shadow_count 0
STAT cmd_get_outlier_all_count 0
STAT cmd_set_outlier_count 0
STAT cmd_set_outlier_failover_count 0
STAT cmd_set_outlier_shadow_count 0
STAT cmd_set_outlier_all_count 0
STAT cmd_other_outlier_count 0
STAT cmd_other_outlier_failover_count 0
STAT cmd_other_outlier_shadow_count 0
STAT cmd_other_outlier_all_count 0
STAT cmd_delete 0
STAT cmd_get 0
STAT cmd_set 0
STAT cmd_delete_outlier 0
STAT cmd_delete_outlier_failover 0
STAT cmd_delete_outlier_shadow 0
STAT cmd_delete_outlier_all 0
STAT cmd_get_outlier 0
STAT cmd_get_outlier_failover 0
STAT cmd_get_outlier_shadow 0
STAT cmd_get_outlier_all 0
STAT cmd_set_outlier 0
STAT cmd_set_outlier_failover 0
STAT cmd_set_outlier_shadow 0
STAT cmd_set_outlier_all 0
STAT cmd_other_outlier 0
STAT cmd_other_outlier_failover 0
STAT cmd_other_outlier_shadow 0
STAT cmd_other_outlier_all 0
END

```

## Wish List

Here's somethings that would be nice to add if possible!

- etcd support
- more fine grained configuration options
- easy access to debug commands

