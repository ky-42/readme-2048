"""Module to load environment variables from .env file."""

import os

from dotenv import load_dotenv

load_dotenv()


def PRODUCTION() -> bool:
    if (production := os.getenv("PRODUCTION")) is not None:
        if production == "False":
            return False
        elif production == "True":
            return True
        raise Exception("PRODUCTION must be either 'True' or 'False'")
    raise Exception("PRODUCTION not set")


def SECRET_KEY() -> str:
    if (key := os.getenv("SECRET_KEY")) is not None:
        return key
    raise Exception("SECRET_KEY not set")


def DATABASE_URI() -> str:
    if (uri := os.getenv("DATABASE_URI")) is not None:
        return uri
    raise Exception("DATABASE_URI not set")


def GITHUB_URL() -> str:
    if (github := os.getenv("GITHUB_URL")) is not None:
        return github
    raise Exception("GITHUB_URL not set")


def UPDATE_FILE_PATH() -> str:
    if (file_path := os.getenv("UPDATE_FILE_PATH")) is not None:
        return file_path
    raise Exception("UPDATE_FILE_PATH not set")


def UPDATE_FILE_NAME() -> str:
    if (file_name := os.getenv("UPDATE_FILE_NAME")) is not None:
        return file_name
    raise Exception("UPDATE_FILE_NAME not set")
