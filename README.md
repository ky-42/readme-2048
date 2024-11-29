# Readme 2048

The game of 2048 but playable in a Github readme file! This is a Flask server that you send moves in a game of 2048 to and it loads, updates and stores the game. It also automatically updates the readme of your Github profile (or and any other file) with the updated game board. It's just a cool little thing to add to your profile!

## Customising

When the server update's the readme file it completely replaces the current file. With this in mind if you were to host this you would likely want to customise the non-game part of the readme. To do this you can simply edit the markdown files in `./src/templates`. There are currently 3 templates in this folder being `game.md`, `personal.md`, and `combined_readme.md`. The `game.md` file is where the game is rendered and you would likely not want to change this. What you would want to change is the `personal.md`. This is currently where all the non-game information is and where you would want to put your regular readme stuff. `combined_readme.md` is where the two previous files are combined and the only reason to change this is if you want to change the order of the two or add another file. All the files use [Jinja templating](https://jinja.palletsprojects.com/en/stable/).

## Routes

`/` Use to do initial setup.

`/click/<int>` Use to make move in the game. The int represent which way to move the board and can be one of four values:

- 1 = Up
- 2 = Down
- 3 = Left
- 4 = Right

## Environment Variables

To run this project, you will need to add the following environment variables to a .env file.

`PRODUCTION` Boolean of whether this is a production instance. Will set Flask [testing](https://flask.palletsprojects.com/en/stable/config/#TESTING) and [debug](https://flask.palletsprojects.com/en/stable/config/#DEBUG) config variables to opposite of this variable.

`SECRET_KEY` String that Flask should use as the secret key see [here](https://flask.palletsprojects.com/en/stable/config/#SECRET_KEY) for more information.

`DATABASE_URI` URI for the PostgreSQL server the app should use.

`GITHUB_URL` URL for the github page to redirect to after making the move and updating the file.

`UPDATE_FILE_PATH` Path of the git repo where the file to update is stored. The server must be able to push changes in this repo without requiring a password. To achieve this, the user account running the server must have an unlocked SSH key configured with push access to this repo. The default upstream must also be set for this repo.

`UPDATE_FILE_NAME` Name of the file to update.

## Run Locally

This section uses [poetry](https://python-poetry.org) in its examples but it's not necessary to run this (just easier).

Clone the project.

```bash
  git clone https://github.com/ky-42/readme-2048
```

Go to the project directory.

```bash
  cd readme-2048
```

Install dependencies.

```bash
  poetry install
```

Start the server. Ensure your .env is properly set at this point. You don't need to load it as the server will load it automatically.

```bash
  poetry run flask --app src run 
```

## Deployment

This section assumes you already cloned the project. This section uses [poetry](https://python-poetry.org) in its examples but it's not necessary to run this (just easier).

Install dependencies.

```bash
  poetry install
```

Add gunicorn as a dependency.

```bash
  poetry add gunicorn
```

Run server with gunicorn. Ensure your .env is properly set at this point. You don't need to load it as the server will load it automatically.

```bash
  poetry run gunicorn --workers 1 src:app
```

### Notes

- Its important that there is only one worker. This is because otherwise you would have race conditions.

- You would also likely want to put a reverse proxy in front of gunicorn read [here](https://www.digitalocean.com/community/tutorials/how-to-configure-nginx-as-a-reverse-proxy-on-ubuntu-22-04) for an idea of how to set this up.
