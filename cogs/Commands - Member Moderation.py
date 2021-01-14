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

#                                                                   Defining Colours

orange= 0xe03616
red= 0xfe5f00
green= 0x20fc8f

#                                                                   Start of commands section

class ModerationCommands(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

#                                                                   Snipe command

    @commands.command()
    async def snipe(self, ctx):
        db=sqlite3.connect("database.db")
        c=db.cursor()

        c.execute("SELECT * FROM snipeData WHERE channelID=?", (ctx.channel.id,))
        data=c.fetchone()
        if data is None:
            em=discord.Embed(
                description="There is nothing to snipe.",
                colour=orange
            )
            await ctx.send(embed=em)
            return
        user = await self.bot.fetch_user(data[1])
        em=discord.Embed(
            description=data[3],
            color=green
        )
        em.set_author(name=user.name, icon_url=user.avatar_url)
        em.set_footer(text=f"mID: {data[2]} uID: {data[2]}")
        await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(ModerationCommands(bot))