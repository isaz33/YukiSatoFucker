import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')
    
@bot.command()
async def timeout(ctx, member: discord.Member, minutes: int):
    try:
        print("timeout")
        await member.timeout_for(minutes * 10)  # タイムアウト時間は秒単位
        await ctx.send(f"{member} has been timed out for {minutes} minutes.")
    except discord.Forbidden:
        await ctx.send("I don't have permission to timeout this user.")
    except discord.HTTPException as e:
        await ctx.send(f"An error occurred: {str(e)}")

TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
