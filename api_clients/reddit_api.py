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

    def get_trending_posts(self, subreddit_name='all', num_posts=5, time_filter='day'):
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
            return None

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
