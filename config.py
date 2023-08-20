# Part of PyroMan - 2022
# Kang by DarkPyro - 2023

from os import getenv
from dotenv import load_dotenv


load_dotenv("config.env")


API_HASH = getenv("API_HASH", "b18441a1ff607e10a989891a5462e627")
API_ID = int(getenv("API_ID", "2040"))

BOTLOG_CHATID = int(getenv("LOGS_ID", ""))
STRING_SESSION = getenv("SESSION", "")

BROADCAST_ENABLED = getenv("BROADCAST", "False") == "True"

CMD_HANDLER = getenv("PREFIX", ".")

DB_URL = getenv("DATABASE_URL", "")

REPO_URL = getenv("REPO_URL", "https://github.com/2R-Dark-Kanger-Pro/DarkPyro-REV")
BRANCH = getenv("BRANCH", "master")
GIT_TOKEN = getenv("GIT_TOKEN", "")

BOT_VER = "1.0.2"