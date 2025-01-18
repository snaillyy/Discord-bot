# What is this?
This is a Discord bot that only serves as giving back member roles when they leave and join.

### How does it work?
First it will create a directory called "data" which will contain files (.db for members and .env for token).

Then as long as the bot stays active, it will take members that leave and store them in the database.
When the member joins back and executes the slash command `/restore_roles`, it will check for the member's id, restore the roles, and remove from the database.

### Install/Setup
Linux/Unix:
1. Set up a bot application through [Discord Developer Portal](https://discord.com/developers).
2. `git clone https://codeberg.org/snaily/Discord-bot.git`
3. Change directory into Discord-bot, create a virtual environment `python -m venv .`
4. `source bin/activate`.
5. `pip install -r requirements.txt`.
6. Make sure everything is working with `python3 src/bot.py`.
7. After everything is working as intended `./run.sh`.

### Dependencies
This was made using >= python3.12, the rest are found in `requirements.txt`

### Thank you
[Zen](https://github.com/desultory) on github for helping me plan this out.\
The developers in requirements.txt who made this possible.\
And you for finding this repository.

### The heck is going on with your commits?
I am still learning how everything works, please bare with me.