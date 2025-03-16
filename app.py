from flask import Flask, render_template, request, jsonify
import requests
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)

# Example API Key (replace with your own)
API_KEY = 'your_alpha_vantage_api_key'

# Fetch real-time market data
def get_market_data(symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    return data

# AI-driven trade signal generation
def generate_trade_signal(data):
    df = pd.DataFrame(data['Time Series (5min)']).T
    df = df.astype(float)
    df['signal'] = RandomForestClassifier().fit_predict(df[['1. open', '2. high', '3. low', '4. close']])
    return df['signal'].iloc[-1]

# Execute trade (mock function)
def execute_trade(symbol, action, quantity):
    # Integration with trading platform API (e.g., Binance, Interactive Brokers)
    return f"{action} {quantity} shares of {symbol}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/trade', methods=['POST'])
def trade():
    data = request.json
    symbol = data['symbol']
    quantity = data['quantity']
    
    market_data = get_market_data(symbol)
    signal = generate_trade_signal(market_data)
    
    if signal == 1:
        result = execute_trade(symbol, 'BUY', quantity)
    elif signal == -1:
        result = execute_trade(symbol, 'SELL', quantity)
    else:
        result = "No trade signal generated"
    
    return jsonify({'status': 'success', 'signal': int(signal), 'result': result})

if __name__ == '__main__':
    app.run(debug=True)
