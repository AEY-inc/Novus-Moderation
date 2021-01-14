import discord, sqlite3, os.path, os, asyncio, string, random
from discord.ext import (
    commands,
    tasks
)
from os import path
from colorama import init, Fore
from datetime import date
from throwbin import ThrowBin
from glob import glob

vc_ids=[773882855725072425, 774339648431587358, 786916685851787304]
pic_ext = ['.jpg','.png','.jpeg', '.gif']

#                                                                   Defining Colours

orange= 0xe03616
red= 0xfe5f00
green= 0x20fc8f    

#                                                                   Start of events section

class otherEvents(commands.Cog):
    def __init__(self, bot):
        self.bot=bot  

#                                                                   ON DELETE

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        db=sqlite3.connect("database.db")
        c=db.cursor()

        c.execute("SELECT * FROM snipeData WHERE channelID=?", (message.channel.id,))
        data = c.fetchone()

        if data is None:
            try:
                c.execute("INSERT INTO snipeData VALUES (?,?,?,?)", (message.channel.id, message.author.id, message.id, message.content,))
            except:
                pass
            db.commit()
            db.close()
            return
        c.execute("DELETE FROM snipeData WHERE channelID=?", (message.channel.id,))
        try:
            c.execute("INSERT INTO snipeData VALUES (?,?,?,?)", (message.channel.id, message.author.id, message.id, message.content,))
        except:
            pass
        db.commit()
        db.close()
        
#                                                                   ON MESSAGE

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.bot.user in message.mentions:
            em=discord.Embed(
                description=f"Do `>cmds` to see the list of commands.",
                color=green
            )
            await message.channel.send(embed=em)
            return
        if "success" in message.channel.name:
            db = sqlite3.connect("database.db")
            c=db.cursor()
            c.execute("SELECT successCHECK FROM moduleConfig")
            check = c.fetchone()
            if check[0] == True:
                if not message.attachments:
                    if any(ext in message.content for ext in pic_ext):
                        return
                    await message.delete()
                else:
                    await self.bot.process_commands(message)
                    

#                                                                   ON COMMAND ERROR

    @commands.Cog.listener()# sends error message to server
    async def on_command_error(self, ctx, error):
            error = getattr(error, 'original', error)
            if isinstance(error, commands.CommandNotFound):
                em=discord.Embed(
                    title="Error",
                    description="Command not found",
                    color=red
                )
                await ctx.send(embed=em)
            elif isinstance(error, commands.CheckFailure):
                em=discord.Embed(
                    title="Error",
                    description="Your missing perms to run that command",
                    color=red
                )
                await ctx.send(embed=em)
            elif isinstance(error, commands.MissingRequiredArgument):
                em=discord.Embed(
                    title="Error",
                    description=f"Missing arguments: {error}",
                    color=red
                )
                await ctx.send(embed=em)         
            else:      
                print(error)

def setup(bot):
    bot.add_cog(otherEvents(bot))