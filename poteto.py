import discord
from discord.ext import commands
import os
from keep_alive import keep_alive
from flask import Flask, request
from datetime import timedelta
import requests
import json
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

app = Flask(__name__)

keep_alive()
print("in progress")

bot = commands.Bot(command_prefix='!', intents=intents)

client = discord.Client(intents = intents)

CHANNEL_ID = 927549442465349632
PERSPECTIVE_API_KEY = "AIzaSyD6yd1tmX9S7QtkJTeJyn7rqe1UaiCtno4"
# 許容できる不適切スコアの閾値
TOXICITY_THRESHOLD = 0.1
TARGET_USER_IDS = [449487835351744515,541887811742334987]  # 監視対象のユーザーIDリスト

async def analyze_text(text,message):
    
    """Perspective API を使用してテキストの不適切度を分析"""
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={PERSPECTIVE_API_KEY}"
    data = {
        "comment": {"text": text},
        "languages": ["ja"],  # 日本語をチェックする場合は ["ja"] に変更
        "requestedAttributes": {"TOXICITY": {}}
    }
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(url, data=json.dumps(data), headers=headers)
    
    
    if response.status_code == 200:
        await message.channel.send("テスト3")
        result = response.json()
        toxicity_score = result["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
        return toxicity_score
    else:
        await message.channel.send("テスト4")
        print(f"Perspective API エラー: {response.status_code}, {response.text}")
        return None



# メッセージ受信時に動作する処理
@bot.event
async def on_message(message):
    
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return

    if message.author.id in TARGET_USER_IDS:
       
        toxicity_score = await analyze_text(message.content,message)
    
        if toxicity_score is not None and toxicity_score > TOXICITY_THRESHOLD:
            try:
                await message.channel.send("テスト1")
                # タイムアウト（mute）処理
                min = 1  # 60秒間タイムアウト
                
                await target_user.timeout(timedelta(minutes=min), reason="ホモのためタイムアウト(時間指定)")
                
                await message.channel.send(f"{target_user} さんの発言は不適切と判断されました。{min}分間ミュートされます。危険度 = {toxicity_score}")
            except Exception as e:
                await message.channel.send("テスト2")
                print(f"タイムアウトエラー: {e}")

    elif bot.user in message.mentions:  # ボットがメンションされた場合
        target_user = message.guild.get_member(449487835351744515)  # 指定されたユーザーを取得
    
        if target_user:  # ユーザーが存在する場合
            # タイムアウト処理 (例: 10分)
            # timeout_duration = discord.utils.utcnow() + discord.timedelta(minutes=0.1)
            # await target_user.edit(timeout=timeout_duration)
            try:
                content_without_mentions = message.content
                for mention in message.mentions:
                    content_without_mentions = int(content_without_mentions.replace(mention.mention, ""))

                if content_without_mentions == "解除":
                    await target_user.timeout(None)
                elif isinstance(content_without_mentions, int):
                    min = content_without_mentions / 60
                    await target_user.timeout(timedelta(minutes=min), reason="ホモのためタイムアウト(時間指定)")
                    await message.channel.send(f"Potato was fucked! ({min}min) ")
                else:
                    await target_user.timeout(timedelta(minutes=0.1), reason="ホモのためタイムアウト")
                    await message.channel.send("Potato was fucked!")
            except:
                await target_user.timeout(timedelta(minutes=0.1), reason="ホモのためタイムアウト(例外)")
                await message.channel.send("Potato was fucked!")
                
            
        else:
            await print("user=none")

    # コマンド処理を続ける
    await bot.process_commands(message)
                
 # member:discord.Member = 541887811742334987
    # await member.timeout(10)
    # if bot.user.mentioned_in(message):
    #     await message.channel.send(f"{message.author.mention} こんにちは！Botにメンションされました！")
    
    # if client.user in message.mentions:
    #     await message.channel.send('test2')
    #     time = message.content
    #     member:discord.Member = 541887811742334987
    #     await member.timeout_for(1)
    #     if time.isdigit():
    #         await message.channel.send('test3')
    #         await member.timeout_for(time)
    #     else:
    #         await message.channel.send('test4')
    #         await member.timeout_for(1)
    # # メッセージがBotへのメンションを含んでいるか確認
    # # if bot.user.mentioned_in(message):
    # #     await message.channel.send(f"{message.author.mention} こんにちは！Botにメンションされました！")

    # # await bot.process_commands(message)
    #     await message.channel.send('タイムアウトを実行します。')
   
    
        
        
# @app.route('/timeout', methods=['POST'])
# # def timeout(ctx, member: discord.Member, minutes: int):
# def timeout(data):
#     message.channel.send('タイムアウトを実行します。')
#     # try:
#     #     print("timeout")
#     #     await member.timeout_for(minutes * 10)  # タイムアウト時間は秒単位
#     #     await ctx.send(f"{member} has been timed out for {minutes} minutes.")
#     # except discord.Forbidden:
#     #     await ctx.send("I don't have permission to timeout this user.")
#     # except discord.HTTPException as e:
#     #     await ctx.send(f"An error occurred: {str(e)}")

TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
