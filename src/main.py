import discord
import sqlite3
import pickle

from os import getenv, listdir, mkdir, path
from dotenv import load_dotenv

def create_table() -> None:
    with sqlite3.connect("data/members.db") as con:
        cursor = con.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS member (
                        id INTEGER PRIMARY KEY,
                        member_name VARCHAR(32) NOT NULL,
                        member_roles VARCHAR(100),
                        binary_roles BLOB NOT NULL
                        );""")
        con.commit()
    return # end create_table()

def encodeBinary():
    """TODO!"""
    return

def decodeBinary():
    """TODO!"""
    return

def showRoles():
    """TODO!"""
    return

def manage_db(cond, mem_id, mem_name=None, mem_roles=None, binary_roles=None):
    """Add or remove member from database based on the condition passed.
    Conditions:
    0 inserts a new record
    1 deletes an existing record
    2 searches for a member id and returns a list of stored roles"""

    try:
        with sqlite3.connect("data/members.db") as con:
            cursor = con.cursor()

            if cond == 0:
                memberInfo = cursor.execute("SELECT id, member_roles, binary_roles FROM member WHERE id = ?;", (mem_id,)).fetchone()

                current = mem_roles.split(",")

                if memberInfo != None:
                    # i love spaghetti, and so should you!
                    stored = pickle.loads(memberInfo[2])

                # check if the member exists and has the same id, insert if not in record
                # and update if there were new roles, else error out
                if memberInfo == None:
                    pklRoles = pickle.dumps(binary_roles)
                    cursor.execute("""INSERT INTO member(id, member_name, member_roles, binary_roles)
                                      VALUES (?, ?, ?, ?)""", (mem_id, mem_name, mem_roles, pklRoles))
                elif (memberInfo != None) and (mem_id == memberInfo[0]) and (len(current) > len(stored)):
                    cursor.execute("""UPDATE member SET member_roles = ?, binary_roles = ?
                                      WHERE id = ?""", (mem_roles,pklRoles,mem_id,))
                else:
                    print("[ERROR] An error has occurred.")
                    print(f"{cond}\n{mem_id}\n{mem_name}\n{mem_roles}\n{binary_roles}")

            elif cond == 1:
                cursor.execute("DELETE FROM member WHERE id = ?;", (mem_id,))
            elif cond == 2:
                cursor.execute(f"SELECT binary_roles FROM member WHERE id = ?;", (mem_id,))
                data = cursor.fetchone()

                if data is None:
                    print(f"[ERROR] {mem_id} tried restoring roles, but no roles were found in the list.")
                    return

                unpklRoles = pickle.loads(data[0])
                return unpklRoles
            else:
                print("[ERROR] An error has occurred.")
                print(f"{cond}\n{mem_id}\n{mem_name}\n{mem_roles}\n{binary_roles}")

            con.commit() # write into db

    except sqlite3.Error as error:
        print(error)

    return # end manage_db()

def main():
    intents = discord.Intents.default()
    intents.members = True
    intents.moderation = True

    client = discord.Bot(intents=intents)

    loadToken = load_dotenv(f"data/token.env")  # returns bool if .env is found
    token = str(getenv("TOKEN"))  # returns string of the variable

    create_table() # create the table if it doesn't exist

    @client.event
    async def on_ready():
        print(f"INFO: {client.user} ({client.user.id}) is ready")

    @client.event
    async def on_member_remove(member):
        try:
            # mem_roles for plaintext, binary_roles for binary
            mem_roles = []
            binary_roles = []

            for roles in member.roles:  # append to list for every non-default role
                if not roles.is_default():
                    mem_roles.append(roles.name)
                    binary_roles.append(roles.id)

            memstr_roles = ",".join(mem_roles) # convert list into string so that it can be stored as VARCHAR
            manage_db(0, member.id, member.name, memstr_roles, binary_roles)
        except Exception as error:
            print(error)

    @client.slash_command (
        name="restore_roles", 
        description="Gives back roles the user previously had, if a role no longer exists, it will be ignored."
        )
    async def give_roles(ctx: discord.ApplicationContext):
        mem_id = ctx.author.id
        unpklRoles = manage_db(2, mem_id)  # retrieve and unpickle the list

        if unpklRoles == 0:
            await ctx.respond("Member ID is not registered, or roles were already given.", ephemeral=True)
            return

        # get guild roles, then iterate through them
        # if a role id is found, give it to the user
        guild_roles = ctx.guild.roles

        try:
            for roles in guild_roles:
                if (roles.id in unpklRoles) and (unpklRoles != None):
                    await ctx.author.add_roles(roles)
                else:
                    continue
            manage_db(1, mem_id)  # remove member from db via id
            await ctx.respond(f"Roles restored!", ephemeral=True)

        except Exception as error:
            await ctx.respond("An error has occurred, event logged.", ephemeral=True)
            print(error)

    client.run(token)
    return # end main()

if __name__ == "__main__":
    main()
