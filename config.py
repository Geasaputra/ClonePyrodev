# Part of PyroMan - 2022
# Kang by DarkPyro - 2023

from os import getenv
from dotenv import load_dotenv


load_dotenv("config.env")


API_HASH = getenv("API_HASH", "b18441a1ff607e10a989891a5462e627")
API_ID = int(getenv("API_ID", "2040"))

BOTLOG_CHATID = int(getenv("BOTLOG_CHATID", ""))
STRING_SESSION = getenv("STRING_SESSION1", "")

CMD_HANDLER = getenv("CMD_HANDLER", ".")

DB_URL = getenv("DATABASE_URL", "postgresql://user:password@db:5432/pyrodark")

REPO_URL = getenv("REPO_URL", "https://github.com/2R-Dark-Kanger-Pro/DarkPyro-REV")
BRANCH = getenv("BRANCH", "master")
GIT_TOKEN = getenv("GIT_TOKEN", "")

BOT_VER = "1.0.2"