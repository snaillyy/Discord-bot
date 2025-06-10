# What is this?
This is a Discord bot that gives back roles to members who leave and join so that they don't have to go through a manual verification process again.

### Features:
- [x] While online, actively record member name and roles.
- [x] `/restore_roles` command.
- [ ] Command to review member information from the database.
- [ ] Command for administrators to remove a record.
- [ ] Encode binary roles in the db.
- [ ] Command to temporarily disable recording.
- [ ] Separate functions to separate files for better readability.

### Install/Setup
⚠️ REMEMBER NOT TO LEAK THE BOT'S TOKEN OTHERWISE THE ACCOUNT COULD BE COMPROMISED!
Check this [guide](https://www.geeksforgeeks.org/how-to-make-a-discord-bot/) for a how-to on creating a discord application.

Linux:
1. `gh repo clone snaillyy/Discord-bot`
2. `cd Discord-bot`
3. `python -m venv .` (use python3 if "command not found" occurs)
4. `source bin/activate`
5. `mkdir data`
6. `pip install -r requirements.txt`
7. `chmod +x run.sh`
8. `./run.sh`

The small script will store all the logs in data/

### Dependencies
* python3
* sqlite3
* python libraries in requirements.txt

### Thank you
[Zen](https://github.com/desultory) on github for helping me plan this out,\
The developers and contributors of the python libraries in requirements.txt,\
and Pycord.

### The heck is going on with your commits?
I am still learning how everything works, please bare with me on that.
