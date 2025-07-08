import os
from dotenv import load_dotenv

load_dotenv()

HUMAN_AGENT_EMAIL = os.getenv("HUMAN_AGENT_EMAIL")
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")