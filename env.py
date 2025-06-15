import dotenv, os

dotenv.load_dotenv()

FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')
KAFKA_BOOTSTRAP_SERVER = os.getenv('KAFKA_BOOTSTRAP_SERVER')
SYMBOLS = os.getenv('SYMBOLS')
KAFKA_STREAMING_TOPIC = os.getenv('KAFKA_STREAMING_TOPIC')
