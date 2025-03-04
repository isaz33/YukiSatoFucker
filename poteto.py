import discord
from discord.ext import commands
import os
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.members = True

keep_alive()
print("in progress")

bot = commands.Bot(command_prefix='!', intents=intents)

client = discord.Client(intents = intents)

CHANNEL_ID = 727020336293609522

# 任意のチャンネルで挨拶する非同期関数を定義
async def greet():
    channel = client.get_channel(CHANNEL_ID)
    await channel.send('おはよう！')

# bot起動時に実行されるイベントハンドラを定義
@client.event
async def on_ready():
    await greet() # 挨拶する非同期関数を実行


# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    # 「/neko」と発言したら「にゃーん」が返る処理
    if message.content == '/neko':
        await message.channel.send('にゃーん')
        
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
