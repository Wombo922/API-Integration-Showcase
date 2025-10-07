import requests

class QuoteAPI:
    """Client for Quotable API (no key required)"""

    def __init__(self):
        self.base_url = "https://api.quotable.io"

    def get_random_quote(self):
        """
        Get random inspirational quote

        Returns:
            dict: Quote data or None if error
        """
        try:
            url = f"{self.base_url}/random"

            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                data = response.json()

                return {
                    'text': data.get('content', ''),
                    'author': data.get('author', 'Unknown'),
                    'tags': data.get('tags', [])
                }
            else:
                return None

        except Exception as e:
            print(f"Error getting quote: {str(e)}")
            return None

    def get_quote_by_tag(self, tag='inspirational'):
        """Get quote by specific tag"""
        try:
            url = f"{self.base_url}/random"
            params = {'tags': tag}

            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                return {
                    'text': data.get('content'),
                    'author': data.get('author')
                }
            else:
                return None

        except Exception as e:
            print(f"Error: {str(e)}")
            return None


# Test
if __name__ == '__main__':
    quotes = QuoteAPI()

    print("Testing Quote API...")
    quote = quotes.get_random_quote()

    if quote:
        print(f"\nQuote of the Day:")
        print(f'"{quote["text"]}"')
        print(f"- {quote['author']}")
    else:
        print("Failed to get quote")
