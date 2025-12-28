Instagram Automation Bot 🤖

A sophisticated Python-based Instagram automation tool with built-in safety features and human-like behavior simulation.
⚠️ Important Disclaimer

This tool is for educational purposes only. Using automation tools with Instagram may violate their Terms of Service and could result in:

• Account suspension or permanent banning

• IP address blocking

• Legal consequences

Use at your own risk. Always:

• Respect Instagram's Terms of Service

• Use responsibly and ethically

• Consider using Instagram's official API for legitimate business purposes

🚀 Features
🤖 Core Functionality

• Session Management: Save and load login sessions

• Rate Limiting: Daily and hourly limits for all actions

• Human Simulation: Random delays and realistic interaction patterns

• Error Handling: Comprehensive error recovery mechanisms

• Logging: Detailed activity logging for monitoring

🔒 Safety Features

• Smart Timing: Avoids suspicious hours (2AM-6AM)

• Progressive Limits: Lower limits on weekends

• Anti-Detection: Realistic user agents and device settings

• Action Validation: Checks limits before performing actions

📊 Engagement Modes

• Hashtag Engagement: Interacts with posts from specific hashtags

• Story Viewing: Views stories from your timeline

• Feed Browsing: Browses timeline without interaction

• Smart Sessions: Randomly selects engagement modes

📋 Requirements
Python Version

Python 3.8 or higher

Dependencies

Install required packages:


```bash
pip install instagrapi
```

Or let the script auto-install them using the built-in libcheck() function.
🛠️ Installation

Clone or download the script

```bash
git clone <repository-url>
cd instagram-bot
```


Configure your credentials

Open insta_bot.py

Replace "YOUR USERNAME" and "YOUR PASSWORD" with your Instagram credentials

Run the bot


```bash
python insta_bot.py
```


⚙️ Configuration
-Rate        Limits-

Action	    Daily Limit	    Hourly Limit

Likes	    120 DL - 15 HL

Follows	    25 DL - 5 HL

Unfollows	25 DL - 5 HL

Comments	15 DL - 3 HL

Story Views	150 DL - 20 HL

DMs	        10 DL - 2 HL

Time Restrictions

• Weekdays: Avoids 2AM-6AM

• Weekends: 9AM-11PM only

• Session Duration: 10-30 minutes per session

Hashtags (Default)

• travel

• photography

• food

• fitness

📝 Usage
Basic Usage

```bash
from insta_bot import InstaBot

# Initialize bot
bot = InstaBot("your_username", "your_password")

# Login
if bot.login():
    # Run safe operations
    bot.run_safe_operations()
    
    # Show statistics
    print("\n--- Daily Statistics ---")
    for action, count in bot.action_counters['daily'].items():
        print(f"{action}: {count}/{bot.daily_limits[action]}")
```

Manual Actions


```bash
# Like a post
bot.safe_like("media_id_here")

# Follow a user
bot.safe_follow("user_id_here")

# Comment on a post
bot.safe_comment("media_id_here", "Great content!")

# View a story
bot.view_story("story_id_here")
```

Custom Engagement

```bash
# Run a hashtag engagement session
hashtags = ['python', 'coding', 'programming']
bot.smart_engagement_session(hashtags=hashtags, duration_minutes=20)

# View random stories
bot.view_random_stories(limit=15)

# Browse timeline
bot.browse_timeline(limit=25)
```

📁 File Structure

```bash
instagram-bot/
│
├── insta_bot.py          # Main bot script
├── session.json          # Saved login session (auto-generated)
├── action_counters.json  # Action statistics (auto-generated)
├── README.md             # This file
└── logs/                 # Log directory (auto-generated)
```

🔍 How It Works
1. Initialization

• Sets up logging and rate limits

• Loads previous action counters

• Configures client with realistic settings

2. Login Process

• Tries to load existing session

• Falls back to fresh login if needed

• Saves session for future use

• Verifies login with timeline fetch

3. Action Execution

• Checks if action is allowed (limits not exceeded)

• Adds human-like delay

• Executes the action

• Records the action

• Saves updated counters

4. Safety Checks

• Time-based restrictions

• Rate limit validation

• Error handling and recovery

• Session validation

⚡ Performance Tips

• Start Slow: Begin with lower limits to test

• Vary Activities: Mix different types of interactions

• Use Proxies: Consider using residential proxies (not included)

• Monitor Logs: Regularly check logs for errors

• Take Breaks: Don't run 24/7 - simulate human patterns

🚨 Common Issues & Solutions
Login Issues

• Problem: "LoginRequired" or "ChallengeRequired"

• Solution: Delete session.json and try fresh login

• Prevention: Enable 2FA on your account

Rate Limiting

• Problem: Actions stop working

• Solution: Check action_counters.json and wait for reset

• Adjustment: Lower the limits in setup_limits()

Account Safety

• Warning: Unusual activity detected

• Response: Stop bot immediately and wait 24-48 hours

• Prevention: Use conservative limits and normal hours

📈 Statistics Tracking

The bot automatically tracks:

• Daily action counts

• Hourly action counts

• Last reset times

• Session history

View statistics:

```bash
print(bot.action_counters['daily'])
print(bot.action_counters['hourly'])
```

🔧 Customization
Adjust Limits

```bash
def setup_limits(self):
    self.daily_limits = {
        'likes': 100,      # Reduced from 120
        'follows': 20,     # Reduced from 25
        # ... other limits
    }
```
Change Hashtags

```bash
def smart_engagement_session(self, hashtags=None, duration_minutes=30):
    if not hashtags:
        hashtags = ['your', 'custom', 'hashtags', 'here']
```

Modify Timing
```bash
def is_safe_time(self):
    # Custom time restrictions
    hour = datetime.now().hour
    # Allow 8AM-10PM only
    return 8 <= hour <= 22
```

🤝 Contributing

• Fork the repository

• Create a feature branch

• Make your changes

• Test thoroughly

• Submit a pull request

📄 License

This project is for educational purposes only. Users are responsible for complying with Instagram's Terms of Service and all applicable laws.
🙏 Acknowledgments

• instagrapi - Instagram API wrapper

• Contributors and testers

📞 Support

For issues and questions:

• Check the Common Issues section

• Review the code comments

• Create a GitHub issue

Remember: Automation should complement, not replace, genuine human interaction. Use responsibly!

