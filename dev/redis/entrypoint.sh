#!/bin/sh
redis-server --daemonize yes
redis-cli < /data/data.redis
redis-cli shutdown
redis-server
echo "Sample data loaded"