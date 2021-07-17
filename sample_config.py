import os
import logging
logger = logging.getLogger(__name__)


class Config:
    API_ID = int(os.environ.get("API_ID", 12345))
    API_HASH = os.environ.get("API_HASH")
    AUTH_USERS = [int(i) for i in os.environ.get("AUTH_USERS", "").split(" ")].append(OWNER_ID) if os.environ.get("AUTH_USERS", "") else [OWNER_ID]
    BANNED_USERS = [int(i) for i in os.environ.get("BANNED_USERS", "").split(" ")] if os.environ.get("BANNED_USERS", "") else None
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    BOT_PASSWORD = os.environ.get("BOT_PASSWORD", "") if os.environ.get("BOT_PASSWORD", "") else None
    CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION") if os.environ.get("CUSTOM_CAPTION", "") else None
    FORCE_SUB = os.environ.get("FORCE_SUB", "") if os.environ.get("FORCE_SUB", "") else None
    DATABASE_URL = os.environ.get("DATABASE_URL", "")
    DOWNLOAD_LOCATION = "./DOWNLOADS"
    try:
        TIME_GAP = int(os.environ.get("TIME_GAP", "")) if os.environ.get("TIME_GAP", "") else None
    except:
        TIME_GAP = None
        logger.warning("Give the timegap in seconds. Dont use letters 😑")
    TIME_GAP_STORE = {}
    try:
        TRACE_CHANNEL = int(os.environ.get("TRACE_CHANNEL")) if os.environ.get("TRACE_CHANNEL", "") else None
    except:
        TRACE_CHANNEL = None
        logger.warning("Trace channel id was invalid")