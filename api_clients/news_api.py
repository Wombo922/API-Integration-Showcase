import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class NewsAPI:
    """Client for NewsAPI.org"""

    def __init__(self):
        self.api_key = os.getenv('NEWS_API_KEY')
        self.base_url = "https://newsapi.org/v2"

    def get_top_headlines(self, country='us', category=None, num_articles=5):
        """
        Get top news headlines

        Args:
            country (str): Country code (us, gb, etc.)
            category (str): Category (business, technology, sports, etc.)
            num_articles (int): Number of articles to return

        Returns:
            list: News articles or None if error
        """
        try:
            url = f"{self.base_url}/top-headlines"
            params = {
                'apiKey': self.api_key,
                'country': country,
                'pageSize': num_articles
            }

            if category:
                params['category'] = category

            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()

                articles = []
                for article in data.get('articles', []):
                    # Parse published date
                    pub_date = article.get('publishedAt', '')
                    if pub_date:
                        try:
                            pub_date = datetime.fromisoformat(pub_date.replace('Z', '+00:00'))
                            pub_date = pub_date.strftime('%b %d, %Y %I:%M %p')
                        except:
                            pass

                    articles.append({
                        'title': article.get('title', 'No title'),
                        'source': article.get('source', {}).get('name', 'Unknown'),
                        'description': article.get('description', 'No description'),
                        'url': article.get('url', ''),
                        'published_at': pub_date
                    })

                return articles

            elif response.status_code == 401:
                print("Error: Invalid News API key")
                return None
            elif response.status_code == 429:
                print("Error: Rate limit exceeded (100 requests/day)")
                return None
            else:
                print(f"Error: API returned status code {response.status_code}")
                return None

        except Exception as e:
            print(f"Error getting news: {str(e)}")
            return None

    def search_news(self, query, num_articles=5):
        """Search for news articles by keyword"""
        try:
            url = f"{self.base_url}/everything"
            params = {
                'apiKey': self.api_key,
                'q': query,
                'sortBy': 'publishedAt',
                'pageSize': num_articles
            }

            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()

                articles = []
                for article in data.get('articles', []):
                    articles.append({
                        'title': article.get('title'),
                        'source': article.get('source', {}).get('name'),
                        'url': article.get('url')
                    })

                return articles
            else:
                return None

        except Exception as e:
            print(f"Error searching news: {str(e)}")
            return None


# Test
if __name__ == '__main__':
    news = NewsAPI()

    print("Testing News API...")
    headlines = news.get_top_headlines(category='technology', num_articles=3)

    if headlines:
        print("\nTop Tech Headlines:")
        for i, article in enumerate(headlines, 1):
            print(f"\n{i}. {article['title']}")
            print(f"   Source: {article['source']}")
            print(f"   Published: {article['published_at']}")
    else:
        print("Failed to get news")
