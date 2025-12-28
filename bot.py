import os
import subprocess
import json
import time
import random
from datetime import datetime, timedelta
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, ChallengeRequired, ClientError
import logging

# === MODULE CHECK FUNCTION === # → This function checks if a module is installed
#   name  module_name   debug (print)
def libcheck(module="pip", debug=True) -> None:
    #result                command list
    result = subprocess.run(['pip', 'list'], capture_output=True, text=True)
    # module name result.module → installed module name
    if module in result.stdout:
        match debug:
            case True:
                print("Module present")
            case _:
                return
        return
    else:
        # install the module
        os.system(f'pip install {module}')
        print(f'Module "{module}" installed')

# === CHECK MODULES === # → Put this before importing instagrapi
# libcheck(module='instagrapi')


class InstaBot:
    def __init__(self, username, password, session_file="session.json"):
        self.username = username
        self.password = password
        self.session_file = session_file
        self.cl = Client()
        self.setup_logging()
        self.setup_limits()
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
    def setup_limits(self):
        self.daily_limits = {
            'likes': 120,
            'follows': 25,
            'unfollows': 25,
            'comments': 15,
            'stories_views': 150,
            'dm_sent': 10
        }
        
        self.hourly_limits = {
            'likes': 15,
            'follows': 5,
            'unfollows': 5,
            'comments': 3,
            'stories_views': 20,
            'dm_sent': 2
        }
        
        self.action_counters = {
            'daily': {key: 0 for key in self.daily_limits},
            'hourly': {key: 0 for key in self.hourly_limits},
            'last_reset_daily': datetime.now(),
            'last_reset_hourly': datetime.now()
        }
        
        self.load_action_counters()
        
    def load_action_counters(self):
        try:
            with open('action_counters.json', 'r') as f:
                data = json.load(f)
                self.action_counters.update(data)
                
                # Check if a day has passed
                last_reset = datetime.fromisoformat(self.action_counters['last_reset_daily'])
                if datetime.now() - last_reset > timedelta(days=1):
                    self.reset_daily_counters()
                    
        except FileNotFoundError:
            self.save_action_counters()
            
    def save_action_counters(self):
        self.action_counters['last_reset_daily'] = datetime.now().isoformat()
        self.action_counters['last_reset_hourly'] = datetime.now().isoformat()
        
        with open('action_counters.json', 'w') as f:
            json.dump(self.action_counters, f, indent=4)
            
    def reset_daily_counters(self):
        for key in self.daily_limits:
            self.action_counters['daily'][key] = 0
        self.save_action_counters()
        
    def reset_hourly_counters(self):
        for key in self.hourly_limits:
            self.action_counters['hourly'][key] = 0
        self.action_counters['last_reset_hourly'] = datetime.now().isoformat()
        self.save_action_counters()
        
    def can_perform_action(self, action_type):
        # Reset hourly counters if needed
        if datetime.now() - datetime.fromisoformat(self.action_counters['last_reset_hourly']) > timedelta(hours=1):
            self.reset_hourly_counters()
            
        daily_count = self.action_counters['daily'][action_type]
        hourly_count = self.action_counters['hourly'][action_type]
        
        if daily_count >= self.daily_limits[action_type]:
            self.logger.warning(f"Daily limit reached for {action_type}")
            return False
            
        if hourly_count >= self.hourly_limits[action_type]:
            self.logger.warning(f"Hourly limit reached for {action_type}")
            return False
            
        return True
        
    def record_action(self, action_type):
        self.action_counters['daily'][action_type] += 1
        self.action_counters['hourly'][action_type] += 1
        self.save_action_counters()
        
    def human_delay(self, min_seconds=2, max_seconds=8):
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
        
    def setup_client(self):
        # Configure realistic user agent
        user_agents = [
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Mobile Safari/537.36"
        ]
        
        self.cl.set_user_agent(random.choice(user_agents))
        
        # Disable some features to reduce detection
        self.cl.set_locale('it_IT')
        self.cl.set_country('IT')
        self.cl.set_country_code(39)
        self.cl.set_timezone_offset(3600)
        
    def login(self):
        try:
            # Try to load existing session
            if os.path.exists(self.session_file):
                self.cl.load_settings(self.session_file)
                self.cl.login(self.username, self.password)
                self.logger.info("Logged in with existing session")
            else:
                # Fresh login
                self.setup_client()
                self.cl.login(self.username, self.password)
                self.cl.dump_settings(self.session_file)
                self.logger.info("New login performed")
                
            # Verify login is valid
            self.cl.get_timeline_feed()
            self.logger.info("Login verified successfully")
            return True
            
        except (LoginRequired, ChallengeRequired) as e:
            self.logger.error(f"Login problem: {e}")
            # Remove corrupted session
            if os.path.exists(self.session_file):
                os.remove(self.session_file)
            return False
        except Exception as e:
            self.logger.error(f"Error during login: {e}")
            return False
            
    def safe_like(self, media_id):
        if not self.can_perform_action('likes'):
            return False
            
        try:
            self.human_delay(3, 7)
            result = self.cl.media_like(media_id)
            self.record_action('likes')
            self.logger.info(f"Liked post {media_id}")
            return True
        except Exception as e:
            self.logger.error(f"Error in like: {e}")
            return False
            
    def safe_follow(self, user_id):
        if not self.can_perform_action('follows'):
            return False
            
        try:
            self.human_delay(5, 12)
            result = self.cl.user_follow(user_id)
            self.record_action('follows')
            self.logger.info(f"Followed user {user_id}")
            return True
        except Exception as e:
            self.logger.error(f"Error in follow: {e}")
            return False
            
    def safe_unfollow(self, user_id):
        if not self.can_perform_action('unfollows'):
            return False
            
        try:
            self.human_delay(5, 12)
            result = self.cl.user_unfollow(user_id)
            self.record_action('unfollows')
            self.logger.info(f"Unfollowed user {user_id}")
            return True
        except Exception as e:
            self.logger.error(f"Error in unfollow: {e}")
            return False
            
    def safe_comment(self, media_id, text):
        if not self.can_perform_action('comments'):
            return False
            
        try:
            self.human_delay(8, 15)
            result = self.cl.media_comment(media_id, text)
            self.record_action('comments')
            self.logger.info(f"Comment added to post {media_id}")
            return True
        except Exception as e:
            self.logger.error(f"Error in comment: {e}")
            return False
            
    def view_story(self, story_id):
        if not self.can_perform_action('stories_views'):
            return False
            
        try:
            self.human_delay(2, 5)
            result = self.cl.story_seen([story_id])
            self.record_action('stories_views')
            self.logger.info(f"Story viewed: {story_id}")
            return True
        except Exception as e:
            self.logger.error(f"Error in story viewing: {e}")
            return False
            
    def get_smart_feed(self, hashtag=None, user_id=None, limit=10):
        """Get feed intelligently"""
        try:
            if hashtag:
                medias = self.cl.hashtag_medias_top(hashtag, amount=limit)
            elif user_id:
                medias = self.cl.user_medias(user_id, amount=limit)
            else:
                medias = self.cl.get_timeline_feed()[:limit]
                
            return medias
        except Exception as e:
            self.logger.error(f"Error retrieving feed: {e}")
            return []
            
    def smart_engagement_session(self, hashtags=None, duration_minutes=30):
        """Intelligent engagement session"""
        if not hashtags:
            hashtags = ['travel', 'photography', 'food', 'fitness']
            
        start_time = time.time()
        max_duration = duration_minutes * 60
        
        hashtag = random.choice(hashtags)
        self.logger.info(f"Starting engagement session with hashtag: #{hashtag}")
        
        medias = self.get_smart_feed(hashtag=hashtag, limit=15)
        
        for media in medias:
            if time.time() - start_time > max_duration:
                break
                
            # Like
            if random.random() < 0.7:  # 70% probability to like
                self.safe_like(media.id)
                
            # Follow (low probability)
            if random.random() < 0.1:  # 10% probability to follow
                self.safe_follow(media.user.pk)
                
            # Comment (even rarer)
            if random.random() < 0.05:  # 5% probability to comment
                comments = ["Nice!", "Great content 👍", "Awesome shot!"]
                self.safe_comment(media.id, random.choice(comments))
                
            # Pause between actions
            self.human_delay(15, 45)
            
        self.logger.info("Engagement session completed")
        
    def is_safe_time(self):
        """Check if it's a safe time to interact"""
        now = datetime.now()
        hour = now.hour
        
        # Avoid night hours (2AM - 6AM)
        if 2 <= hour <= 6:
            return False
            
        # Weekends: more relaxed hours
        if now.weekday() >= 5:  # Saturday or Sunday
            if hour < 9 or hour > 23:
                return False
                
        return True
        
    def run_safe_operations(self):
        """Execute operations safely"""
        if not self.is_safe_time():
            self.logger.info("Not a safe time for operations")
            return
            
        # Random sessions during the day
        session_types = [
            ('hashtag_engagement', 20),
            ('story_viewing', 10),
            ('feed_browsing', 15)
        ]
        
        session_type, duration = random.choice(session_types)
        
        if session_type == 'hashtag_engagement':
            self.smart_engagement_session(duration_minutes=duration)
        elif session_type == 'story_viewing':
            self.view_random_stories(limit=10)
        elif session_type == 'feed_browsing':
            self.browse_timeline(limit=20)
            
    def view_random_stories(self, limit=10):
        """View random stories"""
        try:
            stories = self.cl.get_timeline_stories()[:limit]
            for story in stories:
                self.view_story(story.id)
                self.human_delay(3, 8)
        except Exception as e:
            self.logger.error(f"Error viewing stories: {e}")
            
    def browse_timeline(self, limit=20):
        """Browse timeline without interacting"""
        try:
            feed = self.cl.get_timeline_feed()[:limit]
            for media in feed:
                # Only viewing, no interaction
                self.human_delay(2, 5)
        except Exception as e:
            self.logger.error(f"Error browsing timeline: {e}")

# Bot usage
def main():
    # Configuration
    USERNAME = "YOUR USERNAME"
    PASSWORD = "YOUR PASSWORD"
    
    bot = InstaBot(USERNAME, PASSWORD)
    
    if bot.login():
        # Execute safe operations
        bot.run_safe_operations()
        
        # Show statistics
        print("\n--- Daily Statistics ---")
        for action, count in bot.action_counters['daily'].items():
            print(f"{action}: {count}/{bot.daily_limits[action]}")
            
    else:
        print("Login failed. Check credentials.")

if __name__ == "__main__":
    main()