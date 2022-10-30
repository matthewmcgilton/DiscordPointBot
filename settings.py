from dotenv import load_dotenv
from pathlib import Path
import os

#Path to env file
path = Path('DiscordPointBotDev')/'.env'
load_dotenv(dotenv_path=path)

class Settings:
    MESSAGE_REWARD_WEIGHT = int(os.getenv('MESSAGE_REWARD_WEIGHT'))
    JACKPOT_AMOUNT = int(os.getenv('JACKPOT_AMOUNT'))
    JACKPOT_ODDS = int(os.getenv('JACKPOT_ODDS'))
    MONGO_ADDRESS = str(os.getenv('MONGO_ADDRESS'))
    BOT_TOKEN = str(os.getenv('BOT_TOKEN'))