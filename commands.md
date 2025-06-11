# limit time of keepimg data in kafka (1 day)
kafka-configs.sh --bootstrap-server localhost:9092 \
  --entity-type topics \
  --entity-name stream_stock \
  --alter \
  --add-config retention.ms=86400000

# get wsl ip for advertised listeners
ip addr show eth0

# get kakfa broker messages
bin/kafka-console-consumer.sh --bootstrap-server 172.20.15.243:9092 --topic stock_stream --from-beginning