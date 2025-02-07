import openai
import tweepy
import os
import schedule
import time
from loguru import logger
from dotenv import load_dotenv

# Load API keys from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

def generate_tweet(topic):
    """Generates a tweet using OpenAI GPT"""
    openai.api_key = OPENAI_API_KEY
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a bot that generates creative and interesting tweets."},
            {"role": "user", "content": f"Generate a tweet about {topic}, max 280 characters."}
        ]
    )
    tweet = response["choices"][0]["message"]["content"]
    return tweet[:280]  # Limit to 280 characters

def post_tweet(tweet):
    """Posts a tweet on Twitter."""
    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
    api = tweepy.API(auth)
    api.update_status(tweet)
    logger.info(f"Tweet posted: {tweet}")

def scheduled_tweet():
    """Generates and posts a tweet on a schedule."""
    topics = ["AI advancements", "Future of technology", "Machine learning", "Blockchain and AI"]
    topic = topics[int(time.time()) % len(topics)]  # Rotate topics
    tweet = generate_tweet(topic)
    post_tweet(tweet)

# Schedule the AI agent to tweet every hour
schedule.every().hour.do(scheduled_tweet)

if __name__ == "__main__":
    logger.info("AI Twitter bot started.")
    while True:
        schedule.run_pending()
        time.sleep(60)
