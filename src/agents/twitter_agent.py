import openai
import tweepy
import os
import random
import json
import time
from dotenv import load_dotenv
from loguru import logger
import schedule
from agents.base_agent import BaseAgent

class TwitterAgent(BaseAgent):
    def __init__(self, profile_path="agent_profile.json"):
        super().__init__()
        load_dotenv()
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.twitter_api_key = os.getenv("TWITTER_API_KEY")
        self.twitter_api_secret = os.getenv("TWITTER_API_SECRET")
        self.twitter_access_token = os.getenv("TWITTER_ACCESS_TOKEN")
        self.twitter_access_secret = os.getenv("TWITTER_ACCESS_SECRET")
        
        self.agent_profile = self.load_agent_profile(profile_path)
        openai.api_key = self.openai_api_key
        
    def load_agent_profile(self, profile_path):
        """Loads the AI agent's profile from a JSON file."""
        with open(profile_path, "r", encoding="utf-8") as file:
            return json.load(file)
    
    def generate_tweet(self, topic):
        """Generates a tweet using OpenAI GPT based on the agent's style."""
        style = random.choice(self.agent_profile["style"]["post"])
        response = openai.ChatCompletion.create(
            model=self.agent_profile["modelProvider"],
            messages=[
                {"role": "system", "content": "You are a bot that generates tweets following a specific personality."},
                {"role": "user", "content": f"Generate a tweet about {topic}. Style: {style}. Max 280 characters."}
            ]
        )
        tweet = response["choices"][0]["message"]["content"]
        return tweet[:280]  # Limit to 280 characters
    
    def post_tweet(self, tweet):
        """Posts a tweet on Twitter with error handling and retries."""
        auth = tweepy.OAuthHandler(self.twitter_api_key, self.twitter_api_secret)
        auth.set_access_token(self.twitter_access_token, self.twitter_access_secret)
        api = tweepy.API(auth)
        try:
            api.update_status(tweet)
            logger.info(f"Tweet posted: {tweet}")
        except tweepy.TweepError as e:
            logger.error(f"Failed to post tweet: {e}")
    
    def interact_with_followers(self):
        """Likes and replies to recent mentions using the agent's personality."""
        auth = tweepy.OAuthHandler(self.twitter_api_key, self.twitter_api_secret)
        auth.set_access_token(self.twitter_access_token, self.twitter_access_secret)
        api = tweepy.API(auth)
        mentions = api.mentions_timeline(count=5)
        for mention in mentions:
            try:
                api.create_favorite(mention.id)
                logger.info(f"Liked tweet: {mention.text}")
                response_template = random.choice(self.agent_profile["messageExamples"])
                response = response_template["response"].replace("{{user1}}", f"@{mention.user.screen_name}")
                api.update_status(response, in_reply_to_status_id=mention.id)
                logger.info(f"Replied with: {response}")
            except tweepy.TweepError as e:
                logger.error(f"Error interacting with mentions: {e}")
    
    def scheduled_tweet(self):
        """Generates and posts a tweet on a schedule."""
        topic = random.choice(self.agent_profile["knowledge"])
        tweet = self.generate_tweet(topic)
        self.post_tweet(tweet)
        self.interact_with_followers()

    def run(self):
        """Schedule tasks and start the agent."""
        schedule.every().hour.do(self.scheduled_tweet)
        schedule.every(2).hours.do(self.interact_with_followers)
        logger.info(f"Twitter bot '{self.agent_profile['name']}' started.")
        
        while True:
            schedule.run_pending()
            time.sleep(60)
