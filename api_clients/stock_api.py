import requests
import os
from dotenv import load_dotenv

load_dotenv()

class StockAPI:
    """Client for Alpha Vantage Stock API with Polygon.io fallback"""

    def __init__(self):
        self.alpha_vantage_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        self.polygon_key = os.getenv('POLYGON_API_KEY')
        self.alpha_vantage_url = "https://www.alphavantage.co/query"
        self.polygon_url = "https://api.polygon.io/v2"

    def get_quote_polygon(self, symbol):
        """Get stock quote from Polygon.io"""
        try:
            # Get previous day's close
            url = f"{self.polygon_url}/aggs/ticker/{symbol}/prev"
            params = {'apiKey': self.polygon_key}

            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()

                if data.get('results') and len(data['results']) > 0:
                    result = data['results'][0]

                    open_price = result.get('o', 0)
                    close_price = result.get('c', 0)
                    change = close_price - open_price
                    change_percent = (change / open_price * 100) if open_price > 0 else 0

                    return {
                        'symbol': symbol,
                        'price': close_price,
                        'change': change,
                        'change_percent': change_percent,
                        'volume': result.get('v', 0),
                        'latest_trading_day': 'Previous Day',
                        'is_up': change >= 0
                    }

            return None

        except Exception as e:
            print(f"Polygon.io error for {symbol}: {str(e)}")
            return None

    def get_quote(self, symbol):
        """
        Get current stock quote (tries Alpha Vantage, falls back to Polygon.io)

        Args:
            symbol (str): Stock symbol (e.g., 'AAPL', 'MSFT')

        Returns:
            dict: Stock data or None if error
        """
        # Try Alpha Vantage first if key is available
        if self.alpha_vantage_key and self.alpha_vantage_key not in ['your_alphavantage_api_key', '', None]:
            try:
                params = {
                    'function': 'GLOBAL_QUOTE',
                    'symbol': symbol,
                    'apikey': self.alpha_vantage_key
                }

                response = requests.get(self.alpha_vantage_url, params=params, timeout=10)

                if response.status_code == 200:
                    data = response.json()

                    # Check if we got valid data
                    if 'Global Quote' in data and data['Global Quote']:
                        quote = data['Global Quote']

                        # Calculate if price is up or down
                        change = float(quote.get('09. change', 0))
                        change_percent = quote.get('10. change percent', '0%').replace('%', '')

                        return {
                            'symbol': quote.get('01. symbol', symbol),
                            'price': float(quote.get('05. price', 0)),
                            'change': change,
                            'change_percent': float(change_percent),
                            'volume': int(quote.get('06. volume', 0)),
                            'latest_trading_day': quote.get('07. latest trading day', ''),
                            'is_up': change >= 0
                        }
            except Exception as e:
                print(f"Alpha Vantage error, trying Polygon.io: {str(e)}")

        # Fall back to Polygon.io
        if self.polygon_key:
            return self.get_quote_polygon(symbol)

        print(f"No valid API keys available for {symbol}")
        return None

    def get_multiple_quotes(self, symbols):
        """Get quotes for multiple stocks"""
        quotes = {}

        for symbol in symbols:
            quote = self.get_quote(symbol)
            if quote:
                quotes[symbol] = quote

            # Only sleep if using Alpha Vantage (rate limit: 5 calls/min)
            # Polygon.io has higher limits
            if self.alpha_vantage_key and self.alpha_vantage_key not in ['your_alphavantage_api_key', '', None]:
                import time
                time.sleep(12)  # Wait 12 seconds between calls

        return quotes


# Test
if __name__ == '__main__':
    stocks = StockAPI()

    print("Testing Stock API...")

    # Test single stock
    aapl = stocks.get_quote('AAPL')
    if aapl:
        print(f"\nApple (AAPL):")
        print(f"Price: ${aapl['price']:.2f}")
        print(f"Change: {'+' if aapl['is_up'] else ''}{aapl['change']:.2f} ({aapl['change_percent']:.2f}%)")
        print(f"Volume: {aapl['volume']:,}")
    else:
        print("Failed to get stock data")
