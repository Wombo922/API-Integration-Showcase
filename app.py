import os
from datetime import datetime, timedelta
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from api_clients.weather_api import WeatherAPI
from api_clients.news_api import NewsAPI
from api_clients.stock_api import StockAPI
from api_clients.quote_api import QuoteAPI
from api_clients.twitter_api import TwitterAPI
from api_clients.reddit_api import RedditAPI

class Dashboard:
    """Main dashboard that aggregates all API data"""

    def __init__(self):
        self.weather = WeatherAPI()
        self.news = NewsAPI()
        self.stocks = StockAPI()
        self.quotes = QuoteAPI()
        self.twitter = TwitterAPI()
        self.reddit = RedditAPI()

        self.cache_file = 'dashboard_cache.json'
        self.cache_duration = 300  # 5 minutes in seconds

    def load_cache(self):
        """Load cached data if fresh enough"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r') as f:
                    cache = json.load(f)

                # Check if cache is still fresh
                cache_time = datetime.fromisoformat(cache['timestamp'])
                age = (datetime.now() - cache_time).total_seconds()

                if age < self.cache_duration:
                    print(f"Using cached data ({int(age)} seconds old)")
                    return cache['data']
        except Exception as e:
            print(f"Could not load cache: {e}")

        return None

    def save_cache(self, data):
        """Save data to cache"""
        try:
            cache = {
                'timestamp': datetime.now().isoformat(),
                'data': data
            }
            with open(self.cache_file, 'w') as f:
                json.dump(cache, f, indent=2)
        except Exception as e:
            print(f"Could not save cache: {e}")

    def fetch_all_data(self, use_cache=True, news_category='technology'):
        """
        Fetch data from all APIs

        Args:
            use_cache (bool): Whether to use cached data
            news_category (str): News category to fetch (technology, business, general, entertainment, health, science, sports)

        Returns:
            dict: All dashboard data
        """
        # Try cache first
        if use_cache:
            cached = self.load_cache()
            if cached:
                return cached

        print("Fetching fresh data from APIs in parallel...")

        dashboard_data = {
            'generated_at': datetime.now().isoformat(),
            'weather': None,
            'forecast': None,
            'hourly': None,
            'news': None,
            'stocks': {},
            'etfs': {},
            'quote': None,
            'twitter': None,
            'reddit': None
        }

        # Define fetch functions
        def fetch_weather():
            print("  - Getting weather...")
            return ('weather', self.weather.get_current_weather("Chicago"))

        def fetch_forecast():
            print("  - Getting 7-day forecast...")
            return ('forecast', self.weather.get_7day_forecast("Chicago"))

        def fetch_hourly():
            print("  - Getting hourly forecast...")
            return ('hourly', self.weather.get_hourly_forecast("Chicago", 24))

        def fetch_news():
            print(f"  - Getting {news_category} news...")
            return ('news', self.news.get_top_headlines(category=news_category, num_articles=5))

        def fetch_most_active_stocks():
            print("  - Getting most active stocks...")
            return ('stocks', self.stocks.get_most_active_stocks())

        def fetch_popular_etfs():
            print("  - Getting popular ETFs...")
            return ('etfs', self.stocks.get_popular_etfs())

        def fetch_quote():
            print("  - Getting quote...")
            return ('quote', self.quotes.get_random_quote())

        def fetch_twitter():
            print(f"  - Getting {news_category} tweets...")
            return ('twitter', self.twitter.get_tweets_by_category(category=news_category, num_tweets=3))

        def fetch_reddit():
            print(f"  - Getting {news_category} Reddit posts...")
            return ('reddit', self.reddit.get_trending_posts(subreddit_name='technology', num_posts=3, category=news_category))

        # Fetch all data in parallel using ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = []

            # Submit all API calls
            futures.append(executor.submit(fetch_weather))
            futures.append(executor.submit(fetch_forecast))
            futures.append(executor.submit(fetch_hourly))
            futures.append(executor.submit(fetch_news))
            futures.append(executor.submit(fetch_quote))
            futures.append(executor.submit(fetch_twitter))
            futures.append(executor.submit(fetch_reddit))
            futures.append(executor.submit(fetch_most_active_stocks))
            futures.append(executor.submit(fetch_popular_etfs))

            # Collect results as they complete
            for future in as_completed(futures):
                try:
                    key, value = future.result()
                    dashboard_data[key] = value
                except Exception as e:
                    print(f"Error fetching data: {str(e)}")

        print("All data fetched!")

        # Save to cache
        self.save_cache(dashboard_data)

        return dashboard_data

    def display_dashboard(self, data):
        """Display dashboard data in terminal"""

        # Header
        print("\n" + "="*70)
        print(f"{'PERSONAL DASHBOARD':^70}")
        print(f"{'Generated at ' + datetime.now().strftime('%I:%M %p on %B %d, %Y'):^70}")
        print("="*70 + "\n")

        # Weather Section
        if data['weather']:
            w = data['weather']
            print(f"WEATHER - {w['city']}")
            print("-" * 70)
            print(f"Temperature: {w['temperature']}°F (feels like {w['feels_like']}°F)")
            print(f"Conditions: {w['description'].title()}")
            print(f"Humidity: {w['humidity']}% | Wind: {w['wind_speed']} mph")
            print()

        # Stocks Section
        if data['stocks']:
            print("STOCKS")
            print("-" * 70)
            for symbol, stock in data['stocks'].items():
                arrow = "↑" if stock['is_up'] else "↓"
                color = "+" if stock['is_up'] else ""
                print(f"{symbol:6s} ${stock['price']:8.2f}  {arrow} {color}{stock['change']:6.2f} ({color}{stock['change_percent']:5.2f}%)")
            print()

        # News Section
        if data['news']:
            print("TOP TECH NEWS")
            print("-" * 70)
            for i, article in enumerate(data['news'], 1):
                print(f"\n{i}. {article['title']}")
                print(f"   {article['source']} - {article['published_at']}")
                if article['description']:
                    # Truncate long descriptions
                    desc = article['description']
                    if len(desc) > 100:
                        desc = desc[:97] + "..."
                    print(f"   {desc}")
            print()

        # Quote Section
        if data['quote']:
            q = data['quote']
            print("QUOTE OF THE DAY")
            print("-" * 70)
            print(f'"{q["text"]}"')
            print(f"- {q['author']}")
            print()

        print("="*70 + "\n")


def main():
    """Main function"""
    print("Personal Dashboard - Aggregating data from multiple APIs")

    dashboard = Dashboard()

    # Fetch and display data
    data = dashboard.fetch_all_data(use_cache=True)
    dashboard.display_dashboard(data)

    # Show cache info
    print("Note: Data is cached for 5 minutes to avoid excessive API calls")
    print("Run with --no-cache flag to force refresh")


if __name__ == '__main__':
    import sys

    # Check for --no-cache flag
    use_cache = '--no-cache' not in sys.argv

    dashboard = Dashboard()
    data = dashboard.fetch_all_data(use_cache=use_cache)
    dashboard.display_dashboard(data)
