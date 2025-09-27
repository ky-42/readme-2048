"""Module for running git commands."""

import os
import subprocess
from pathlib import Path

from .env import (
    GIT_EMAIL,
    GIT_NAME,
    REPO_CLONE_URL,
    SSH_DIR,
    UPDATE_FILE_PATH,
    WORKING_DIR,
)

ENV = os.environ.copy()
SSH_COMMAND = f"ssh -i {SSH_DIR()}/key -o IdentitiesOnly=yes -o UserKnownHostsFile={SSH_DIR()}/known_hosts -o StrictHostKeyChecking=yes"
ENV["GIT_SSH_COMMAND"] = SSH_COMMAND


def set_user_email() -> None:
    """Set the git user name and email for commits.

    Args:
        name (str): The name to set.
        email (str): The email to set.
    """
    subprocess.run(
        ["git", "config", "--global", "user.name", GIT_NAME()], cwd=WORKING_DIR()
    )
    subprocess.run(
        ["git", "config", "--global", "user.email", GIT_EMAIL()], cwd=WORKING_DIR()
    )


def clone() -> None:
    """Clone the git repository."""

    # Add github to known hosts
    with open(SSH_DIR() / "known_hosts", "a") as hosts_file:
        subprocess.run(["ssh-keyscan", "github.com"], stdout=hosts_file, check=True)

    subprocess.run(
        ["git", "clone", REPO_CLONE_URL()], cwd=WORKING_DIR(), env=ENV, check=True
    )


def update(update_string: str) -> None:
    """Update a file then push it to a git repository.

    Args:
        update_string (str): The string to write to the file.
    """

    update_path = WORKING_DIR() / Path(
        REPO_CLONE_URL().split("/")[-1].removesuffix(".git")
    )

    update_file = update_path / UPDATE_FILE_PATH()

    with open(update_file, "w") as f:
        f.write(update_string)

    subprocess.run(["git", "add", update_file], cwd=update_path)
    subprocess.run(
        ["git", "commit", "-m", f"Updated {update_file.name}"], cwd=update_path
    )

    subprocess.run(["git", "push", "-f"], cwd=update_path, env=ENV)
