"""Module to load environment variables from .env file."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def PRODUCTION() -> bool:
    """Flag to indicate if the app is running in production mode"""
    if (production := os.getenv("PRODUCTION")) is not None:
        if production == "False":
            return False
        elif production == "True":
            return True
        raise Exception("PRODUCTION must be either 'True' or 'False'")
    raise Exception("PRODUCTION not set")


def SECRET_KEY() -> str:
    """Secret key for the Flask application"""
    if (key := os.getenv("SECRET_KEY")) is not None:
        return key
    raise Exception("SECRET_KEY not set")


def DATABASE_URI() -> str:
    """Database connection URI"""
    if (uri := os.getenv("DATABASE_URI")) is not None:
        return uri
    raise Exception("DATABASE_URI not set")


def REDIRECT_URL() -> str:
    """URL to redirect to after a click action"""
    if (redirect_url := os.getenv("REDIRECT_URL")) is not None:
        return redirect_url
    raise Exception("REDIRECT_URL not set")


def REPO_CLONE_URL() -> str:
    """URL of the repo to clone"""
    if (url := os.getenv("REPO_CLONE_URL")) is not None:
        return url
    raise Exception("REPO_CLONE_URL not set")


def UPDATE_FILE_PATH() -> Path:
    """Name of the file in the repo to update"""
    if (file_path := os.getenv("UPDATE_FILE_PATH")) is not None:
        return Path(file_path)
    raise Exception("UPDATE_FILE_PATH not set")


def WORKING_DIR() -> Path:
    """Working directory for cloning the repo"""
    if (working_dir := os.getenv("WORKING_DIR")) is not None:
        working_dir = Path(working_dir)

        if not working_dir.exists():
            working_dir.mkdir(parents=True, exist_ok=True)

        return working_dir
    raise Exception("WORKING_DIR not set")


def GIT_NAME() -> str:
    """Git user name for commits"""
    if (name := os.getenv("GIT_NAME")) is not None:
        return name
    raise Exception("GIT_NAME not set")


def GIT_EMAIL() -> str:
    """Git user email for commits"""
    if (email := os.getenv("GIT_EMAIL")) is not None:
        return email
    raise Exception("GIT_EMAIL not set")


def SSH_DIR() -> Path:
    """SSH directory should hold the private key and known_hosts file"""
    if (ssh_dir := os.getenv("SSH_DIR")) is not None:
        ssh_dir = Path(ssh_dir)

        if not ssh_dir.exists():
            ssh_dir.mkdir(parents=True, exist_ok=True)

        return ssh_dir
    raise Exception("SSH_DIR not set")
