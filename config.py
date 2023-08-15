# Part of PyroMan - 2022
# Kang by DarkPyro - 2023

from os import getenv

from dotenv import load_dotenv

load_dotenv("config.env")


API_HASH = getenv("API_HASH", "b18441a1ff607e10a989891a5462e627")
API_ID = int(getenv("API_ID", "2040"))
BOTLOG_CHATID = int(getenv("BOTLOG_CHATID") or 0)
BOT_VER = "1.0.0"
BRANCH = getenv("BRANCH", "master")
CHANNEL = getenv("CHANNEL", "fuckdvck")
CMD_HANDLER = getenv("CMD_HANDLER", ".")
DB_URL = getenv("DATABASE_URL", "postgresql://user:password@db:5432/pyrodark")
GIT_TOKEN = getenv("GIT_TOKEN", "")
GROUP = getenv("GROUP", "DarkPyroREV")
REPO_URL = getenv("REPO_URL", "https://github.com/2R-Dark-Kanger-Pro/DarkPyro-REV")
STRING_SESSION = getenv("STRING_SESSION1", "")
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "").split()))
