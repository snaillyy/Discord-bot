import discord
import sqlite3
import pickle

from os import getenv, listdir, mkdir
from dotenv import load_dotenv

def create_table() -> None:
    with sqlite3.connect("src/data/members.db") as con:
        cursor = con.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS member (
                        id INTEGER PRIMARY KEY,
                        member_name VARCHAR(32) NOT NULL,
                        member_roles BLOB NOT NULL
                        );""")
        con.commit()

def manage_db(cond, mem_id, mem_name=None, mem_roles=None) -> int:
    """Add or remove member from database based on the condition passed."""
    try:
        with sqlite3.connect("src/data/members.db") as con:
            cursor = con.cursor()

            if cond == 0:
                pklRoles = pickle.dumps(mem_roles)
                cursor.execute("""INSERT INTO member(id, member_name, member_roles)
                                VALUES (?, ?, ?)""", (mem_id, mem_name, pklRoles))
            elif cond == 1:
                cursor.execute("DELETE FROM member WHERE id = ?;", (mem_id,))

            con.commit()
    except sqlite3.Error as error:
        print(error)

def fetch_member_pkl(mem_id):
    """Called when give_roles() is executed.
    Takes mem_id, fetches one id from db, unpickles and returns the list"""
    try:
        with sqlite3.connect("src/data/members.db") as con:
            cursor = con.cursor()
            cursor.execute(f"SELECT member_roles FROM member WHERE id = ?;", (mem_id,))
            data = cursor.fetchone()[0]

            unpklRoles = pickle.loads(data)
            return unpklRoles

    except sqlite3.Error as error:
        print(error)

def main(client, token) -> None:
    @client.event
    async def on_ready():
        print(f"INFO: {client.user} ({client.user.id}) is ready")

    @client.event
    async def on_member_remove(member):
        mem_roles = []

        for roles in member.roles:  # append to list for every non-default role
            if roles.is_default() == False:
                mem_roles.append(roles.id)

        try:
            manage_db(0, member.id, member.name, mem_roles)
        except RecursionError as error:
            print(error)

    @client.slash_command (
        name="restore_roles", 
        description="Gives back roles the user previously had, if a role no longer exists, it will be ignored."
        )
    async def give_roles(ctx: discord.ApplicationContext):
        mem_id = ctx.author.id

        unpklRoles = fetch_member_pkl(mem_id)  # unpickle the list

        # get guild roles, then iterate through them
        # if a role id is found, give it to the user
        guild_roles = ctx.guild.roles

        try:
            for roles in guild_roles:
                if roles.id in unpklRoles:
                    await ctx.author.add_roles(roles)
                else:
                    continue
            await ctx.respond(f"Roles successfully restored", ephemeral=True)
            manage_db(1, mem_id)  # remove member from db via id

        except Exception as error:
            await ctx.respond("An error has occurred.", ephemeral=True)
            print(error)

    client.run(token)

def prepare() -> None:
    """First function to execute."""
    try:  # check if files exist
        listFiles = listdir("src/data/")

        if not listFiles:  # check if src/data/ is empty
            raise FileNotFoundError

        for files in listFiles:
            if files.endswith(".env"):
                print(f"INFO: {files} found")
                loadToken = load_dotenv(f"src/data/{files}")
                token = str(getenv("TOKEN") or getenv("token"))

            elif files.endswith(".db"):
                print(f"INFO: {files} found")
                break

            else:
                raise FileNotFoundError

    except FileNotFoundError:
        mkdir("src/data/")
        with open("src/data/token.env", "w") as token:
            tk = input("Enter your token for src/data/token.env:\n> ")
            token.write(f"TOKEN={tk}")
        
        with open("src/data/members.db", "w") as db:
            create_table()

        prepare()  # recall function after write to avoid improper token, if it is correct

    intents = discord.Intents.default()
    intents.members = True
    intents.moderation = True

    bot = discord.Bot(intents=intents)
    main(bot, token)

if __name__ == "__main__":
    prepare()