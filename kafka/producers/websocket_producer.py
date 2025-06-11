import json
import websocket
from confluent_kafka import Producer

# Your Finnhub API key
FINNHUB_API_KEY = 'd0tfuepr01qlvahbtb2gd0tfuepr01qlvahbtb30'
# List of finnhub's stock symbols
SYMBOLS =['AAPL', 'GOOG', 'MSFT', 'TSLA'] 

# Kafka configuration
KAFKA_BOOTSTRAP_SERVERS = '172.20.15.243:9092'
KAFKA_TOPIC = 'stock_stream'
producer = Producer({'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS})

def on_message(ws, message):
    msg = json.loads(message)
    if msg.get("type") == "ping":
        # Message to keep the connection to Finnhub's server
        print("Ping received")
        return
    for trade in msg["data"]:
        # Send to Kafka
        print("price update sent")
        producer.produce(KAFKA_TOPIC, json.dumps(trade, indent=4))
    producer.poll(0)

def on_error(ws, error):
    print("WebSocket error:", error)

def on_close(ws, close_status_code, close_msg):
    producer.flush()
    print(f"WebSocket closed: {close_msg}\n{close_status_code}")

def on_open(ws):
    for symbol in SYMBOLS:
        # Send info from each stock to kafka
        subscribe_message = json.dumps({
            "type": "subscribe",
            "symbol": symbol
        })
        ws.send(subscribe_message)

# Set up WebSocket connection to get real-time prices updates
if __name__ == "__main__":
    ws_url = f"wss://ws.finnhub.io?token={FINNHUB_API_KEY}"
    ws = websocket.WebSocketApp(
        ws_url,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.on_open = on_open
    ws.run_forever()
