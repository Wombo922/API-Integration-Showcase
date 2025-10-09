import praw
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class RedditAPI:
    """Client for Reddit API"""

    def __init__(self):
        self.client_id = os.getenv('REDDIT_CLIENT_ID')
        self.client_secret = os.getenv('REDDIT_CLIENT_SECRET')
        self.username = os.getenv('REDDIT_USERNAME')
        self.password = os.getenv('REDDIT_PASSWORD')

        self.reddit = praw.Reddit(
            client_id=self.client_id,
            client_secret=self.client_secret,
            username=self.username,
            password=self.password,
            user_agent='dashboard-app/0.1 by Legal-Mongoose414'
        )

    def get_trending_posts(self, subreddit_name='all', num_posts=5, time_filter='day', category=None):
        """
        Get trending posts from Reddit

        Args:
            subreddit_name (str): Subreddit to fetch from ('all', 'technology', 'worldnews', etc.)
            num_posts (int): Number of posts to return
            time_filter (str): Time filter ('hour', 'day', 'week', 'month', 'year', 'all')

        Returns:
            list: Trending posts or None if error
        """
        try:
            # Map categories to relevant subreddits
            if category:
                category_subreddits = {
                    'technology': 'technology',
                    'business': 'business',
                    'general': 'news',
                    'entertainment': 'entertainment',
                    'health': 'health',
                    'science': 'science',
                    'sports': 'sports'
                }
                subreddit_name = category_subreddits.get(category.lower(), subreddit_name)

            subreddit = self.reddit.subreddit(subreddit_name)
            posts = []

            for submission in subreddit.hot(limit=num_posts):
                # Calculate post age
                created_time = datetime.fromtimestamp(submission.created_utc)
                age = datetime.now() - created_time

                if age.days > 0:
                    age_str = f"{age.days}d ago"
                elif age.seconds >= 3600:
                    age_str = f"{age.seconds // 3600}h ago"
                else:
                    age_str = f"{age.seconds // 60}m ago"

                posts.append({
                    'title': submission.title,
                    'subreddit': submission.subreddit.display_name,
                    'author': str(submission.author),
                    'score': submission.score,
                    'num_comments': submission.num_comments,
                    'url': f"https://reddit.com{submission.permalink}",
                    'age': age_str,
                    'selftext': submission.selftext[:200] if submission.selftext else ''
                })

            return posts

        except Exception as e:
            print(f"Error getting Reddit posts: {str(e)}")
            return self.get_mock_posts(subreddit_name, num_posts, category)

    def get_mock_posts(self, subreddit_name="technology", num_posts=5, category=None):
        """Provide mock Reddit posts when API is unavailable"""
        mock_posts = {
            'technology': [
                {'title': 'New breakthrough in quantum computing achieves 99.9% fidelity in error correction', 'score': 4521, 'num_comments': 342, 'subreddit': 'technology', 'url': 'https://reddit.com/r/technology/mock1', 'age': '3 hours ago', 'selftext': ''},
                {'title': 'Apple announces major shift in chip architecture for next generation devices', 'score': 3876, 'num_comments': 289, 'subreddit': 'technology', 'url': 'https://reddit.com/r/technology/mock2', 'age': '5 hours ago', 'selftext': ''},
                {'title': 'AI model achieves human-level performance in complex reasoning tasks', 'score': 3241, 'num_comments': 198, 'subreddit': 'technology', 'url': 'https://reddit.com/r/technology/mock3', 'age': '7 hours ago', 'selftext': ''},
            ],
            'business': [
                {'title': 'Major tech acquisition reshapes cloud computing landscape in $15B deal', 'score': 2876, 'num_comments': 234, 'subreddit': 'business', 'url': 'https://reddit.com/r/business/mock1', 'age': '2 hours ago', 'selftext': ''},
                {'title': 'Federal Reserve hints at policy changes following economic indicators', 'score': 2543, 'num_comments': 187, 'subreddit': 'business', 'url': 'https://reddit.com/r/business/mock2', 'age': '4 hours ago', 'selftext': ''},
                {'title': 'Cryptocurrency market shows institutional adoption acceleration', 'score': 2198, 'num_comments': 156, 'subreddit': 'business', 'url': 'https://reddit.com/r/business/mock3', 'age': '6 hours ago', 'selftext': ''},
            ],
            'general': [
                {'title': 'Climate summit reaches historic agreement on global carbon emissions', 'score': 4567, 'num_comments': 892, 'subreddit': 'news', 'url': 'https://reddit.com/r/news/mock1', 'age': '1 hour ago', 'selftext': ''},
                {'title': 'Unprecedented voter turnout recorded in major democratic election', 'score': 3456, 'num_comments': 654, 'subreddit': 'news', 'url': 'https://reddit.com/r/news/mock2', 'age': '3 hours ago', 'selftext': ''},
                {'title': 'International peace talks show promising diplomatic developments', 'score': 2987, 'num_comments': 423, 'subreddit': 'worldnews', 'url': 'https://reddit.com/r/worldnews/mock3', 'age': '5 hours ago', 'selftext': ''},
            ],
            'entertainment': [
                {'title': 'Hollywood blockbuster breaks global box office records with $200M opening', 'score': 5432, 'num_comments': 1234, 'subreddit': 'entertainment', 'url': 'https://reddit.com/r/entertainment/mock1', 'age': '30 minutes ago', 'selftext': ''},
                {'title': 'Streaming platforms reach new user milestone as music industry evolves', 'score': 3876, 'num_comments': 567, 'subreddit': 'entertainment', 'url': 'https://reddit.com/r/entertainment/mock2', 'age': '2 hours ago', 'selftext': ''},
                {'title': 'Award-winning series announces final season with exclusive content', 'score': 4123, 'num_comments': 789, 'subreddit': 'television', 'url': 'https://reddit.com/r/television/mock3', 'age': '4 hours ago', 'selftext': ''},
            ]
        }

        # Use category if provided, otherwise use subreddit_name
        lookup_key = category.lower() if category else subreddit_name.lower()
        subreddit_posts = mock_posts.get(lookup_key, mock_posts['technology'])
        return subreddit_posts[:num_posts]

    def get_top_from_multiple_subs(self, subreddits=['technology', 'worldnews', 'news'], limit_per_sub=2):
        """Get top posts from multiple subreddits"""
        all_posts = []

        for sub in subreddits:
            posts = self.get_trending_posts(subreddit_name=sub, num_posts=limit_per_sub)
            if posts:
                all_posts.extend(posts)

        # Sort by score
        all_posts.sort(key=lambda x: x['score'], reverse=True)

        return all_posts[:limit_per_sub * len(subreddits)]


# Test
if __name__ == '__main__':
    reddit = RedditAPI()

    print("Testing Reddit API...")
    posts = reddit.get_trending_posts(subreddit_name='technology', num_posts=3)

    if posts:
        print(f"\nTop Posts from r/technology:")
        for i, post in enumerate(posts, 1):
            print(f"\n{i}. {post['title']}")
            print(f"   r/{post['subreddit']} • ⬆️ {post['score']} • 💬 {post['num_comments']} • {post['age']}")
    else:
        print("Failed to get Reddit posts")
