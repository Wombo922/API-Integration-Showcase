import requests
import os
from dotenv import load_dotenv

load_dotenv()

class TwitterAPI:
    """Client for Twitter/X API"""

    def __init__(self):
        self.bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
        self.base_url = "https://api.twitter.com/2"

    def get_tweets_by_category(self, category="technology", num_tweets=5):
        """
        Get tweets based on subject category

        Args:
            category (str): Category to search for (technology, business, science, entertainment, etc.)
            num_tweets (int): Number of tweets to return

        Returns:
            list: Category-relevant tweets or None if error
        """
        try:
            # Map categories to search queries
            category_queries = {
                'technology': 'tech OR technology OR AI OR software OR programming OR cybersecurity',
                'business': 'business OR finance OR startup OR entrepreneur OR investing OR economy',
                'science': 'science OR research OR discovery OR space OR climate OR medical',
                'health': 'health OR medical OR medicine OR healthcare OR wellness OR fitness',
                'sports': 'sports OR football OR basketball OR baseball OR soccer OR olympics',
                'entertainment': 'entertainment OR movie OR music OR celebrity OR gaming OR streaming',
                'general': 'breaking OR news OR trending OR important OR update'
            }

            query = category_queries.get(category.lower(), category_queries['technology'])

            url = f"{self.base_url}/tweets/search/recent"
            headers = {"Authorization": f"Bearer {self.bearer_token}"}
            params = {
                "query": f"({query}) -is:retweet lang:en",
                "max_results": num_tweets,
                "tweet.fields": "created_at,public_metrics,author_id",
                "expansions": "author_id",
                "user.fields": "username,name,verified",
                "sort_order": "relevancy"
            }

            response = requests.get(url, headers=headers, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()

                if not data.get('data'):
                    return []

                # Map user IDs to usernames
                users = {}
                if 'includes' in data and 'users' in data['includes']:
                    for user in data['includes']['users']:
                        users[user['id']] = user

                tweets = []
                for tweet in data.get('data', []):
                    author = users.get(tweet.get('author_id'), {})
                    metrics = tweet.get('public_metrics', {})

                    tweets.append({
                        'text': tweet.get('text', ''),
                        'author': author.get('username', 'Unknown'),
                        'author_name': author.get('name', 'Unknown'),
                        'verified': author.get('verified', False),
                        'likes': metrics.get('like_count', 0),
                        'retweets': metrics.get('retweet_count', 0),
                        'replies': metrics.get('reply_count', 0),
                        'created_at': tweet.get('created_at', ''),
                        'category': category.title()
                    })

                return tweets

            elif response.status_code == 401:
                print("Error: Invalid Twitter Bearer Token - using mock data")
                return self.get_mock_tweets(category, num_tweets)
            elif response.status_code == 429:
                print("Error: Twitter rate limit exceeded - using mock data")
                return self.get_mock_tweets(category, num_tweets)
            else:
                print(f"Error: Twitter API returned status code {response.status_code} - using mock data")
                return self.get_mock_tweets(category, num_tweets)

        except Exception as e:
            print(f"Error getting Twitter trends: {str(e)}")
            return self.get_mock_tweets(category, num_tweets)

    def get_mock_tweets(self, category="technology", num_tweets=5):
        """Provide mock tweets when API is unavailable"""
        mock_tweets = {
            'technology': [
                {'text': 'Breaking: New AI breakthrough in machine learning algorithms shows 40% improvement in processing speed', 'author': 'TechNews', 'author_name': 'Tech News Daily', 'verified': True, 'likes': 1234, 'retweets': 567, 'replies': 89, 'created_at': '2024-10-07T10:30:00Z', 'category': 'Technology'},
                {'text': 'Apple announces revolutionary new chip architecture for next-generation devices', 'author': 'AppleInsider', 'author_name': 'Apple Insider', 'verified': True, 'likes': 2156, 'retweets': 892, 'replies': 234, 'created_at': '2024-10-07T09:15:00Z', 'category': 'Technology'},
                {'text': 'Quantum computing milestone: Scientists achieve 99.9% fidelity in quantum error correction', 'author': 'QuantumDaily', 'author_name': 'Quantum Computing Daily', 'verified': True, 'likes': 987, 'retweets': 445, 'replies': 67, 'created_at': '2024-10-07T08:45:00Z', 'category': 'Technology'},
            ],
            'business': [
                {'text': 'BREAKING: Major tech acquisition valued at $15B announced, reshaping the cloud computing landscape', 'author': 'BusinessWire', 'author_name': 'Business Wire', 'verified': True, 'likes': 1876, 'retweets': 743, 'replies': 156, 'created_at': '2024-10-07T10:20:00Z', 'category': 'Business'},
                {'text': 'Federal Reserve signals potential rate changes following latest economic indicators', 'author': 'FinancialTimes', 'author_name': 'Financial Times', 'verified': True, 'likes': 2341, 'retweets': 923, 'replies': 287, 'created_at': '2024-10-07T09:30:00Z', 'category': 'Business'},
                {'text': 'Cryptocurrency market sees significant movement as institutional adoption accelerates', 'author': 'CryptoNews', 'author_name': 'Crypto News Network', 'verified': True, 'likes': 1564, 'retweets': 678, 'replies': 134, 'created_at': '2024-10-07T08:55:00Z', 'category': 'Business'},
            ],
            'general': [
                {'text': 'BREAKING: Global climate summit reaches historic agreement on carbon emissions reduction', 'author': 'WorldNews', 'author_name': 'World News Network', 'verified': True, 'likes': 3245, 'retweets': 1456, 'replies': 423, 'created_at': '2024-10-07T11:15:00Z', 'category': 'General'},
                {'text': 'Election results show unprecedented voter turnout in major democratic process', 'author': 'NewsUpdate', 'author_name': 'News Update Daily', 'verified': True, 'likes': 2876, 'retweets': 987, 'replies': 345, 'created_at': '2024-10-07T10:45:00Z', 'category': 'General'},
                {'text': 'International peace talks yield promising developments in ongoing diplomatic efforts', 'author': 'GlobalNews', 'author_name': 'Global News Wire', 'verified': True, 'likes': 1987, 'retweets': 654, 'replies': 234, 'created_at': '2024-10-07T09:20:00Z', 'category': 'General'},
            ],
            'entertainment': [
                {'text': 'Hollywood blockbuster breaks opening weekend records with $200M global box office', 'author': 'EntertainmentTonight', 'author_name': 'Entertainment Tonight', 'verified': True, 'likes': 4321, 'retweets': 1876, 'replies': 567, 'created_at': '2024-10-07T12:30:00Z', 'category': 'Entertainment'},
                {'text': 'Music industry celebrates as streaming platforms reach new milestone of global users', 'author': 'MusicNews', 'author_name': 'Music News Daily', 'verified': True, 'likes': 2654, 'retweets': 892, 'replies': 234, 'created_at': '2024-10-07T11:15:00Z', 'category': 'Entertainment'},
                {'text': 'Award-winning series announces final season with exclusive behind-the-scenes content', 'author': 'TVGuide', 'author_name': 'TV Guide Magazine', 'verified': True, 'likes': 3456, 'retweets': 1234, 'replies': 445, 'created_at': '2024-10-07T10:00:00Z', 'category': 'Entertainment'},
            ],
            'health': [
                {'text': 'New medical study shows promising results for breakthrough cancer treatment therapy', 'author': 'HealthDaily', 'author_name': 'Health Daily News', 'verified': True, 'likes': 2876, 'retweets': 1234, 'replies': 345, 'created_at': '2024-10-07T10:30:00Z', 'category': 'Health'},
                {'text': 'Researchers discover innovative approach to mental health treatment with 85% success rate', 'author': 'MedicalNews', 'author_name': 'Medical News Today', 'verified': True, 'likes': 1987, 'retweets': 765, 'replies': 234, 'created_at': '2024-10-07T09:45:00Z', 'category': 'Health'},
                {'text': 'WHO announces new guidelines for preventive healthcare in response to global health trends', 'author': 'WHONews', 'author_name': 'World Health Organization', 'verified': True, 'likes': 3456, 'retweets': 1456, 'replies': 456, 'created_at': '2024-10-07T08:30:00Z', 'category': 'Health'},
            ],
            'science': [
                {'text': 'Astronomers detect potentially habitable exoplanet 100 light-years from Earth', 'author': 'SpaceNews', 'author_name': 'Space News Network', 'verified': True, 'likes': 5432, 'retweets': 2345, 'replies': 678, 'created_at': '2024-10-07T11:00:00Z', 'category': 'Science'},
                {'text': 'Scientists achieve nuclear fusion breakthrough with net energy gain for third consecutive test', 'author': 'ScienceDaily', 'author_name': 'Science Daily', 'verified': True, 'likes': 4321, 'retweets': 1987, 'replies': 543, 'created_at': '2024-10-07T10:15:00Z', 'category': 'Science'},
                {'text': 'Climate researchers unveil revolutionary carbon capture technology capable of large-scale deployment', 'author': 'ClimateScience', 'author_name': 'Climate Science Today', 'verified': True, 'likes': 3654, 'retweets': 1456, 'replies': 432, 'created_at': '2024-10-07T09:30:00Z', 'category': 'Science'},
            ],
            'sports': [
                {'text': 'Historic championship game goes into triple overtime with record-breaking final score', 'author': 'ESPN', 'author_name': 'ESPN Sports', 'verified': True, 'likes': 6543, 'retweets': 3456, 'replies': 892, 'created_at': '2024-10-07T12:00:00Z', 'category': 'Sports'},
                {'text': 'Olympic committee announces new venues and events for upcoming international games', 'author': 'Olympics', 'author_name': 'Olympic Games', 'verified': True, 'likes': 4567, 'retweets': 2134, 'replies': 567, 'created_at': '2024-10-07T11:30:00Z', 'category': 'Sports'},
                {'text': 'Star athlete breaks long-standing world record in stunning performance at championship', 'author': 'SportsCenter', 'author_name': 'Sports Center', 'verified': True, 'likes': 5678, 'retweets': 2876, 'replies': 734, 'created_at': '2024-10-07T10:45:00Z', 'category': 'Sports'},
            ]
        }

        category_tweets = mock_tweets.get(category.lower(), mock_tweets['technology'])
        return category_tweets[:num_tweets]

    def get_trending_topics(self, num_topics=5):
        """Backward compatibility method"""
        return self.get_tweets_by_category("technology", num_topics)


# Test
if __name__ == '__main__':
    twitter = TwitterAPI()

    print("Testing Twitter API...")
    trends = twitter.get_trending_topics(num_topics=3)

    if trends:
        print(f"\nTrending Tech/Crypto Tweets:")
        for i, tweet in enumerate(trends, 1):
            print(f"\n{i}. @{tweet['author']}: {tweet['text'][:100]}...")
            print(f"   ❤️ {tweet['likes']} | 🔄 {tweet['retweets']}")
    else:
        print("Failed to get Twitter trends")
