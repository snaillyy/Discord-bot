# What is this?
This is a Discord bot that gives back roles to members who leave and join so that they don't have to go through a manual verification process again.

### Features:
[x] While online, actively record member name and roles.\
[x] `/restore_roles` command.

### TODO:
[ ] Command to review member information from the database.\
[ ] Command for administrators to remove a record.\
[ ] Encode binarified roles

### Install/Setup
⚠️ REMEMBER NOT TO LEAK THE BOT'S TOKEN OTHERWISE THE ACCOUNT COULD BE COMPROMISED!

Make a new file in data directory called token.env, then add the discord bot's token the same as this one `TOKEN=<token goes here>`
If unsure how, check out this [guide](https://www.geeksforgeeks.org/how-to-make-a-discord-bot/).

Linux:
1. `gh repo clone snaillyy/Discord-bot`
2. `cd Discord-bot`
3. `mkdir data`
4. `source bin/activate`
5. `pip install -r requirements.txt`
6. `chmod +x run.sh`
7. `./run.sh`

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
