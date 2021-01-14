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



class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

#                                                                   RELOADS OR LOADS THE MODULES.

    def reload_or_load_extension(self,module):
        try:
            self.bot.reload_extension(f"cogs.{module}")
            return True
        except commands.ExtensionNotLoaded:
            self.bot.load_extension(f"cogs.{module}")
            return False
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reload(self, ctx, module = None):
        COGS = [path.split("\\")[-1][:-3] for path in glob("./cogs/*.py")]
        em = discord.Embed(
            title="Reloading Logs:",
            color = 0xC0C0C0
        )
        for cog in COGS:
            try:
                if self.reload_or_load_extension(cog):
                    em.add_field(name=cog, value="SUCCESSFULLY Reloaded", inline=False)
                else:
                    em.add_field(name=cog, value="SUCCESSFULLY Loaded", inline=False)
            except commands.ExtensionError:
                em.add_field(name=cog, value="FAILED to load/reload", inline=False)
        await ctx.send(embed=em)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def config(self, ctx, module=None, setting=None):
        if module is None or setting is None:
            await ctx.send(f"{ctx.prefix}config <module> <true/false/on/off>")
            return
        db=sqlite3.connect("database.db")
        c=db.cursor()
        c.execute("SELECT successCHECK FROM moduleConfig")
        check = c.fetchone()
        if module.lower() == "success":
            if setting.lower() == "true" or setting.lower() == "on":
                if check[0] == True:
                    await ctx.send("already enabled.")
                    return
                c.execute("UPDATE moduleConfig SET successCHECK = ?", (True,))
                await ctx.send("Enabled.")
            elif setting.lower() == "false" or setting.lower() == "off":
                if check[0] == False:
                    await ctx.send("already disabled.")
                    return
                c.execute("UPDATE moduleConfig SET successCHECK = ?", (False,))
                await ctx.send("Disabled.")
            db.commit()
            db.close()

def setup(bot):
    bot.add_cog(AdminCommands(bot))
