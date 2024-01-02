"""Load all user defined config and env vars."""

import logging
import os
import sys
from typing import Dict, List, Optional, Union

from dotenv import load_dotenv
from pydantic import BaseModel, validator  # pylint: disable=no-name-in-module
from pymongo import MongoClient
from telethon import TelegramClient
from telethon.sessions import StringSession

from test_tele import storage as stg
from test_tele.const import BOT_CONFIG_FILE_NAME, TAGS
from test_tele.plugin_models import PluginConfig

pwd = os.getcwd()
env_file = os.path.join(pwd, ".env")

load_dotenv(env_file)


class UserBot(BaseModel):
    """Configuration for user that using bot"""

    user_id: int = 0
    status: int = 0 # 0: standby, 1: processing
    links: list[str] = []

    config_ignore: bool = True
    user_config_path: str = "config/config.json" # default permanen, tapi kalo bisa dibuat dinamis


class BotMessages(BaseModel):
    start: str = "Hi! I'm alive"
    bot_help: str = (
        """
        **HELP**

        -= Available Commands =-

        /start : Restart the bot
        /id  : Get details ID of a message
        /get  : Forward messages from public channel
        /report : Send a message to the bot Admin
        /help  : Show this message

        -= Inline Bot =-

        **Gelbooru**
        Show images from gelbooru website
        Command: `@ttloli_bot`
        Usage: TAGS
        Note: 
        - TAGS = replace "space" with underscore (_)

        **Pixiv**
        Show images from pixiv artworks
        Command: `@ttloli_bot .px`
        Usage: [OPTIONS].. [MODE]..
        Options: TAGS | id:USER_ID | ART_ID
        Mode: `-r18` | `-safe`, `-no_ai`

        **Furry e621**
        Show furry images from e621 or e6ai website
        Command: `@ttloli_bot .fur`
        Usage: [MODE].. TAGS
        Mode: `-ai` |
        Note: 
        - No autocomplete tag (exact accepted tags must be provided)
        - TAGS = replace "space" with underscore (_)

        **Real Person**
        Show collections of real models
        Command: `@ttloli_bot .rp`
        Usage: [OPTIONS]..
        Options: MODELS | id:GALLERY_ID | CATEGORIES
        
        **Manga / Doujins** __[BETA]__
        Show list of doujins
        Command: `@ttloli_bot .md`
        Usage: [OPTIONS].. TAGS..
        Options: `rating:N` (1-5) | `artist:NAME`
        
        **Example** 
        `@ttloli_bot highres one_piece`
        `@ttloli_bot .px id:99370414 -safe -no_ai`
        `@ttloli_bot .fur -ai my_little_pony`
        `@ttloli_bot .rp cosplay asia`
        `@ttloli_bot .md female rating:4`

        -= Other Functions =-

        **Media Downloader**
        Usage: Send media link
        Note: If no media has been sent to you, it means the website is not yet supported
        **'Advanced /get' Method**
        Usage: Send public channel message link
        """.replace("    ", "")
    )


class Telegraph(BaseModel):
    short_name: str = '1707'
    access_token: str = 'f12a95f380b4c79ae51d1d640bd8b43e5de5235fdb14b0073c4aaeac9168'
    auth_url: str = 'https://edit.telegra.ph/auth/4eD363oiSHV64zz3HWNI8qKrUOOcMACRMdSTfe97T5'
    prefix: str = ''
    description: str = ''


class APIs(BaseModel):
    pixiv_refresh_token: str = 'FY0E1IOR9NN-ls0O75IXs62QeZvv-CdxLJC6pAZDmfE'


class Tags(BaseModel):
    tags: dict = TAGS


class BotConfig(BaseModel):
    """The blueprint for Media Downloader live's bot"""
    # pylint: disable=too-few-public-
    bot_name: str = "@ttloli_bot"
    bot_messages: BotMessages = BotMessages()
    telegraph: Telegraph = Telegraph()
    apis: APIs = APIs()
    all_tags: Tags = Tags()
    user_cfg: List[UserBot] = []


def write_config_to_file(config: BotConfig):
    with open(BOT_CONFIG_FILE_NAME, "w", encoding="utf8") as file:
        file.write(config.json())


def detect_config_type() -> int:
    if os.getenv("MONGO_CON_STR"):
        if MONGO_CON_STR:
            logging.info("Using mongo db for storing config!")
            client = MongoClient(MONGO_CON_STR)
            stg.mycol = setup_mongo(client)
        return 2
    if BOT_CONFIG_FILE_NAME in os.listdir():
        logging.info(f"{BOT_CONFIG_FILE_NAME} detected!")
        return 1

    else:
        logging.info(
            "config file not found. mongo not found. creating local config file."
        )
        cfg = BotConfig()
        write_config_to_file(cfg)
        logging.info(f"{BOT_CONFIG_FILE_NAME} created!")
        return 1
    

def read_bot_config(count=1) -> BotConfig:
    """Load the configuration defined by user."""
    if count > 3:
        logging.warning("Failed to read config, returning default config")
        return BotConfig()
    if count != 1:
        logging.info(f"Trying to read config time:{count}")
    try:
        if stg.BOT_CONFIG_TYPE == 1:
            with open(BOT_CONFIG_FILE_NAME, encoding="utf8") as file:
                return BotConfig.parse_raw(file.read())
        elif stg.BOT_CONFIG_TYPE == 2:
            return read_db()
        else:
            return BotConfig()
    except Exception as err:
        logging.warning(err)
        stg.BOT_CONFIG_TYPE = detect_config_type()
        return read_bot_config(count=count + 1)


def write_bot_config(config: BotConfig, persist=True):
    """Write changes in config back to file."""
    if stg.BOT_CONFIG_TYPE == 1 or stg.BOT_CONFIG_TYPE == 0:
        write_config_to_file(config)
    elif stg.BOT_CONFIG_TYPE == 2:
        if persist:
            update_db(config)


def setup_mongo(client):

    mydb = client[MONGO_DB_NAME]
    mycol = mydb[MONGO_COL_NAME]
    if not mycol.find_one({"_id": 0}):
        mycol.insert_one({"_id": 0, "author": "tgcf", "config": BotConfig().dict()})

    return mycol


def update_db(cfg):
    stg.mycol.update_one({"_id": 0}, {"$set": {"config": cfg.dict()}})


def read_db():
    obj = stg.mycol.find_one({"_id": 0})
    cfg = BotConfig(**obj["config"])
    return cfg


stg.BOT_CONFIG_TYPE = detect_config_type()
BOT_CONFIG = read_bot_config()

MONGO_CON_STR = os.getenv("MONGO_CON_STR")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "tgcf-config")
MONGO_COL_NAME = os.getenv("MONGO_COL_NAME", "tgcf-instance-0")

SUPPORTED_URL = []

logging.info("config_bot.py got executed")
