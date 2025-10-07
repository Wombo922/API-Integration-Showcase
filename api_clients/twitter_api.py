import requests
import os
from dotenv import load_dotenv

load_dotenv()

class TwitterAPI:
    """Client for Twitter/X API"""

    def __init__(self):
        self.bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
        self.base_url = "https://api.twitter.com/2"

    def get_trending_topics(self, num_topics=5):
        """
        Get trending topics/tweets

        Args:
            num_topics (int): Number of trending items to return

        Returns:
            list: Trending topics or None if error
        """
        try:
            # Search for recent popular crypto/tech tweets
            url = f"{self.base_url}/tweets/search/recent"
            headers = {"Authorization": f"Bearer {self.bearer_token}"}
            params = {
                "query": "(tech OR technology OR AI OR crypto) -is:retweet",
                "max_results": num_topics,
                "tweet.fields": "created_at,public_metrics,author_id",
                "expansions": "author_id",
                "user.fields": "username,name"
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

                trending = []
                for tweet in data.get('data', []):
                    author = users.get(tweet.get('author_id'), {})
                    metrics = tweet.get('public_metrics', {})

                    trending.append({
                        'text': tweet.get('text', ''),
                        'author': author.get('username', 'Unknown'),
                        'author_name': author.get('name', 'Unknown'),
                        'likes': metrics.get('like_count', 0),
                        'retweets': metrics.get('retweet_count', 0),
                        'created_at': tweet.get('created_at', '')
                    })

                return trending

            elif response.status_code == 401:
                print("Error: Invalid Twitter Bearer Token")
                return None
            elif response.status_code == 429:
                print("Error: Twitter rate limit exceeded")
                return None
            else:
                print(f"Error: Twitter API returned status code {response.status_code}")
                return None

        except Exception as e:
            print(f"Error getting Twitter trends: {str(e)}")
            return None


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
