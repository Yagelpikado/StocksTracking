import os, json, finnhub, sys
import pandas as pd
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(project_root)
from env import FINNHUB_API_KEY, SYMBOLS, KAFKA_BOOTSTRAP_SERVER, KAFKA_STREAMING_TOPIC

# Setup client
finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)

print(json.dumps(finnhub_client.stock_symbols('US')[:10], indent=3))
exit()

stock_basic_info = finnhub_client.company_basic_financials('AAPL', 'all') # basic company info such as  as margin, P/E ratio, 52-week high/low etc
#stock_quote = finnhub_client.quote('AAPL') # current prices and changes
stock_recommendation = finnhub_client.recommendation_trends('AAPL') # analyst recommendation trends for a company
print('Basic company info:\n',pd.DataFrame(stock_basic_info), '\n')
print('analysts recommendations:\n', pd.DataFrame(stock_recommendation), '\n')
exit()
