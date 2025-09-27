# Readme 2048

The game of 2048 but playable in a Github readme file! This is a Flask server that you send moves in a game of 2048 to and it loads, updates and stores the game. It also automatically updates the readme of your Github profile (or and any other file) with the updated game board. It's just a cool little thing to add to your profile!

## Customizing

When the server update's the readme file it completely replaces the current file. With this in mind if you were to host this you would likely want to customize the non-game part of the readme. To do this you can simply edit the markdown files in `./src/templates`. There are currently 3 templates in this folder being `game.md`, `personal.md`, and `combined_readme.md`. The `game.md` file is where the game is rendered and you would likely not want to change this. What you would want to change is the `personal.md`. This is currently where all the non-game information is and where you would want to put your regular readme stuff. `combined_readme.md` is where the two previous files are combined and the only reason to change this is if you want to change the order of the two or add another file. All the files use [Jinja templating](https://jinja.palletsprojects.com/en/stable/).

## Routes

`/setup` Use to do initial setup.

`/click/<int>` Use to make move in the game. The int represent which way to move the board and can be one of four values:

- 1 = Up
- 2 = Down
- 3 = Left
- 4 = Right

## Notes

- Its important that there is only one worker when deploying because otherwise you would have race conditions.
- When using docker mount ssh keys you want to use