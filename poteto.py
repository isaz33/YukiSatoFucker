import discord
from discord.ext import commands
import os
from keep_alive import keep_alive
from flask import Flask, request

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

app = Flask(__name__)

keep_alive()
print("in progress")

bot = commands.Bot(command_prefix='!', intents=intents)

client = discord.Client(intents = intents)

CHANNEL_ID = 727020336293609522


# メッセージ受信時に動作する処理
@bot.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    # 「/neko」と発言したら「にゃーん」が返る処理
    await message.channel.send('test')
    if client.user in message.mentions:
        
        time = message.content
        member:discord.Member = 541887811742334987
        
        if time.isdigit():
            member.timeout_for(time)
        else:
            member.timeout_for(1)
        await message.channel.send('タイムアウトを実行します。')
    
        
        
@app.route('/timeout', methods=['POST'])
# def timeout(ctx, member: discord.Member, minutes: int):
def timeout(data):
    message.channel.send('タイムアウトを実行します。')
    # try:
    #     print("timeout")
    #     await member.timeout_for(minutes * 10)  # タイムアウト時間は秒単位
    #     await ctx.send(f"{member} has been timed out for {minutes} minutes.")
    # except discord.Forbidden:
    #     await ctx.send("I don't have permission to timeout this user.")
    # except discord.HTTPException as e:
    #     await ctx.send(f"An error occurred: {str(e)}")

TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
