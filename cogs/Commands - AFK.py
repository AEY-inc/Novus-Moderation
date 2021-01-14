import discord, sqlite3
from discord.ext import commands, tasks

green=0x7fb069
red=0xca3c25
orange= 0xe03616
dbN="database.db"

def AFKcheck(uid):
    db=sqlite3.connect(dbN)
    c=db.cursor()
    c.execute("SELECT * FROM afkList WHERE userUID=?", (uid,))
    data=c.fetchone()
    if data is None:
        return True

class AFKcmds(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.mentions:
            for mention in message.mentions:
                if not AFKcheck(mention.id):
                    db=sqlite3.connect(dbN)
                    c=db.cursor()
                    c.execute("SELECT message FROM afkList WHERE userUID=?", (mention.id,))
                    afkMsg = c.fetchone()[0]
                    db.close()
                    em=discord.Embed(
                        title=f"**__{mention.name} is AFK.__**",
                        description=f"**Message**:\n\n{'No message was set' if afkMsg is None else afkMsg}",
                        color=green
                    )
                    em.set_image(url="https://i.imgur.com/kRLbxba.png")
                    em.set_footer(text="For AFK commands do !afk")
                    await message.channel.send(embed=em)
            return
        if not AFKcheck(message.author.id):
            if not "afk" in message.content.lower():
                db=sqlite3.connect(dbN)
                c=db.cursor()
                c.execute("DELETE FROM afkList WHERE userUID=?", (message.author.id,))
                db.commit()
                db.close()
                em=discord.Embed(
                    title="AFK status removed.",
                    description="I noticed you are set as AFK however you are talking. I removed your AFK status :wink:",
                    color=green
                )
                em.set_image(url="https://i.imgur.com/kRLbxba.png")
                em.set_footer(text="For AFK commands do !afk")
                await message.author.send(embed=em)
                return

    @commands.command()
    async def afk(self, ctx, *, message=None):
        db=sqlite3.connect(dbN)
        c=db.cursor()
        if AFKcheck(ctx.author.id):
            c.execute("INSERT INTO afkList VALUES (?,?)", (ctx.author.id, message,))
            db.commit()
            db.close()
            em=discord.Embed(
                title="AFK Status Set.",
                description=f"{ctx.author.mention}, I set your afk message to:\n\n```{message}```",
                color=green
            )
            em.set_image(url="https://i.imgur.com/kRLbxba.png")
            em.set_footer(text="For AFK commands do !afk")
            await ctx.send(embed=em)
            return
        c.execute("DELETE FROM afkList WHERE userUID=?", (ctx.author.id,))
        db.commit()
        db.close()
        em=discord.Embed(
            title="Welcome Back!",
            description=f"{ctx.author.mention}, I successfully removed your AFK status.",
            color=green
        )
        em.set_image(url="https://i.imgur.com/kRLbxba.png")
        em.set_footer(text="For AFK commands do !afk")
        await ctx.send(embed=em)

    
def setup(bot):
    bot.add_cog(AFKcmds(bot))