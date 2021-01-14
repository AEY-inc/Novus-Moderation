import discord, json, asyncio, time, sqlite3
from discord.ext import commands, tasks
from glob import glob
from colorama import Fore, init
from os import path

init(autoreset=True)

intents = discord.Intents.default()
intents.members=True

orange= 0xe03616
red= 0xfe5f00
green= 0x20fc8f

COGS = [path.split("\\")[-1][:-3] for path in glob("./cogs/*.py")]
start = time.time()

client = commands.Bot(
    command_prefix="!",
    command_insensitive=True,
    description="Novus Moderation",
    intents=intents
)
client.remove_command('help')

async def presChange():
    await client.wait_until_ready()
    print(f"{Fore.GREEN}[LOGGING] - Bot is ready. Preparing to update presence.")
    while True:
        await client.change_presence(activity=discord.Activity(type=1, name=f"!cmds", url="https://www.twitch.tv/twitch"))
        print(f"{Fore.GREEN}[LOGGING] - Presence updated.")
        await asyncio.sleep(10)
        await client.change_presence(activity=discord.Activity(type=1, name=f"Made with <3 by AEY inc.#1337", url="https://www.twitch.tv/twitch"))
        print(f"{Fore.GREEN}[LOGGING] - Presence updated.")
        await asyncio.sleep(10)


@client.event
async def on_connect():
    print(f"{Fore.YELLOW}[LOGGING] - Connected. Checking database...")
    if path.exists("database.db"):
        print(f"{Fore.GREEN}[LOGGING] - Database is fine. Continuing...")
    else:
        db = sqlite3.connect("database.db")
        c = db.cursor()
        c.execute("CREATE TABLE ticketPanels (messageID integer, serverID integer, categoryNAME text, welcomeMSG text)")
        c.execute("CREATE TABLE ticketData (count integer)")
        c.execute("INSERT INTO ticketData VALUES (0)")
        c.execute("CREATE TABLE snipeData (channelID, userUID integer, messageID integer, content text)")
        c.execute("CREATE TABLE afkList (userUID integer, message text)")
        c.execute("CREATE TABLE moduleConfig (successCHECK boolean)")
        c.execute("INSERT INTO moduleConfig VALUES (?)", (True,))
        db.commit()
        db.close()
        print(f"{Fore.GREEN} [LOGGING] - Database created. Proceeding...\n")
        await asyncio.sleep(2)
    

@client.event
async def on_command_error(ctx, error):
    print(error)


@client.command()
async def uptime(ctx):
    done = time.time()
    s = done - start
    hours, remainder = divmod(s, 3600)
    minutes, seconds = divmod(remainder, 60)
    embed = discord.Embed(
        colour = 0x20fc8f ,
        description='**Uptime:** {:02} Hours, {:02} Minutes and {:02} Seconds.'.format(int(hours), int(minutes), int(seconds)),
        timestamp = ctx.message.created_at
        )
    embed.set_footer(text = "Made with ❤ by AEY")
    await ctx.send(embed=embed)

for cog in COGS:
    client.load_extension(f"cogs.{cog}")

client.loop.create_task(presChange())
client.run("Nzk4NjQ2MjA2Nzk1ODc0Mzc3.X_4DPQ.fIMI-cfT-pCBVygfq7nuf4n0mlg")