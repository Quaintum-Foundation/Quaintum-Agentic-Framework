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
from qiskit import Aer, transpile, assemble
from qiskit.circuit import QuantumCircuit
from qiskit.providers.aer import AerSimulator

class QuantumTwitterAgent(BaseAgent):
    def __init__(self, profile_path="agent_profile.json"):
        super().__init__(name="QuantumTwitterBot")
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

    def quantum_decision(self) -> bool:
        """Make a quantum-based decision (e.g., whether to post a tweet or not)."""
        # Create a simple quantum circuit that simulates a coin flip to decide whether to tweet
        circuit = QuantumCircuit(1, 1)
        circuit.h(0)  # Hadamard gate to create superposition
        circuit.measure(0, 0)  # Measure the qubit to collapse the state
        
        # Use Qiskit’s AerSimulator to simulate the quantum circuit
        simulator = AerSimulator()
        transpiled_circuit = transpile(circuit, simulator)
        qobj = assemble(transpiled_circuit)
        result = simulator.run(qobj).result()
        counts = result.get_counts()
        
        # If the result is 1, decide to post a tweet (true), else don't post (false)
        if '1' in counts:
            logger.info("Quantum decision: Tweeting!")
            return True
        else:
            logger.info("Quantum decision: Not tweeting.")
            return False

    def scheduled_tweet(self):
        """Generates and posts a tweet on a schedule, using quantum decision."""
        # Make a quantum decision to tweet
        if self.quantum_decision():
            topic = random.choice(self.agent_profile["knowledge"])
            tweet = self.generate_tweet(topic)
            self.post_tweet(tweet)
            self.interact_with_followers()

    def run(self):
        """Schedule tasks and start the agent."""
        schedule.every().hour.do(self.scheduled_tweet)
        schedule.every(2).hours.do(self.interact_with_followers)
        logger.info(f"Quantum Twitter bot '{self.agent_profile['name']}' started.")
        
        while True:
            schedule.run_pending()
            time.sleep(60)

# Example Usage
if __name__ == "__main__":
    quantum_twitter_agent = QuantumTwitterAgent(profile_path="agent_profile.json")
    quantum_twitter_agent.run()
