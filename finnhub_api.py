import websocket
import json
import finnhub
import pandas as pd

API_KEY = "d0tfuepr01qlvahbtb2gd0tfuepr01qlvahbtb30"

# Setup client
finnhub_client = finnhub.Client(api_key=API_KEY)

stock_basic_info = finnhub_client.company_basic_financials('AAPL', 'all') # basic company info such as  as margin, P/E ratio, 52-week high/low etc
#stock_quote = finnhub_client.quote('AAPL') # current prices and changes
stock_recommendation = finnhub_client.recommendation_trends('AAPL') # analyst recommendation trends for a company
print('Basic company info:\n',pd.DataFrame(stock_basic_info), '\n')
print('analysts recommendations:\n', pd.DataFrame(stock_recommendation), '\n')
exit()
