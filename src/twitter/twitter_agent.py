import openai
import tweepy
import os

# Set OpenAI and Twitter API keys
OPENAI_API_KEY = "your_openai_api_key"
TWITTER_API_KEY = "your_twitter_api_key"
TWITTER_API_SECRET = "your_twitter_api_secret"
TWITTER_ACCESS_TOKEN = "your_twitter_access_token"
TWITTER_ACCESS_SECRET = "your_twitter_access_secret"

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
    print("Tweet posted:", tweet)

if __name__ == "__main__":
    topic = "artificial intelligence and the future"
    tweet = generate_tweet(topic)
    post_tweet(tweet)
