import openai
import tweepy
import os
import schedule
import time
import random
import json
from loguru import logger
from dotenv import load_dotenv

# Load API keys from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

# Load AI Agent Profile from JSON file
def load_agent_profile(profile_path="agent_profile.json"):
    """Loads the AI agent's profile from a JSON file."""
    with open(profile_path, "r", encoding="utf-8") as file:
        return json.load(file)

AGENT_PROFILE = load_agent_profile()

def generate_tweet(topic):
    """Generates a tweet using OpenAI GPT based on the agent's style."""
    openai.api_key = OPENAI_API_KEY
    style = random.choice(AGENT_PROFILE["style"]["post"])
    response = openai.ChatCompletion.create(
        model=AGENT_PROFILE["modelProvider"],
        messages=[
            {"role": "system", "content": "You are a bot that generates tweets following a specific personality."},
            {"role": "user", "content": f"Generate a tweet about {topic}. Style: {style}. Max 280 characters."}
        ]
    )
    tweet = response["choices"][0]["message"]["content"]
    return tweet[:280]  # Limit to 280 characters

def post_tweet(tweet):
    """Posts a tweet on Twitter with error handling and retries."""
    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
    api = tweepy.API(auth)
    try:
        api.update_status(tweet)
        logger.info(f"Tweet posted: {tweet}")
    except tweepy.TweepError as e:
        logger.error(f"Failed to post tweet: {e}")

def interact_with_followers():
    """Likes and replies to recent mentions using the agent's personality."""
    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
    api = tweepy.API(auth)
    mentions = api.mentions_timeline(count=5)
    for mention in mentions:
        try:
            api.create_favorite(mention.id)
            logger.info(f"Liked tweet: {mention.text}")
            response_template = random.choice(AGENT_PROFILE["messageExamples"])
            response = response_template["response"].replace("{{user1}}", f"@{mention.user.screen_name}")
            api.update_status(response, in_reply_to_status_id=mention.id)
            logger.info(f"Replied with: {response}")
        except tweepy.TweepError as e:
            logger.error(f"Error interacting with mentions: {e}")

def scheduled_tweet():
    """Generates and posts a tweet on a schedule."""
    topic = random.choice(AGENT_PROFILE["knowledge"])
    tweet = generate_tweet(topic)
    post_tweet(tweet)
    interact_with_followers()

# Schedule the AI agent to tweet and interact every hour
schedule.every().hour.do(scheduled_tweet)
schedule.every(2).hours.do(interact_with_followers)

if __name__ == "__main__":
    logger.info(f"AI Twitter bot '{AGENT_PROFILE['name']}' started.")
    while True:
        schedule.run_pending()
        time.sleep(60)
