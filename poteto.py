import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def timeout(ctx, member: discord.Member, minutes: int):
    try:
        await member.timeout_for(minutes * 60)  # タイムアウト時間は秒単位
        await ctx.send(f"{member} has been timed out for {minutes} minutes.")
    except discord.Forbidden:
        await ctx.send("I don't have permission to timeout this user.")
    except discord.HTTPException as e:
        await ctx.send(f"An error occurred: {str(e)}")

bot.run('YOUR_BOT_TOKEN')