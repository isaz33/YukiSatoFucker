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

bot = commands.Bot(command_prefix='!', intents=intents)
client = discord.Client(intents = intents)
CHANNEL_ID = 927549442465349632

# PERSPECTIVE_API
PERSPECTIVE_API_KEY = "AIzaSyD6yd1tmX9S7QtkJTeJyn7rqe1UaiCtno4"
# 許容できる不適切スコアの閾値
TOXICITY_THRESHOLD = 0.3
# 監視対象のユーザーIDリスト
TARGET_USER_IDS = [449487835351744515]  








# 文字列の危険度判定
async def analyze_text(text):
    
    """Perspective API"""
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={PERSPECTIVE_API_KEY}"
    data = {
        "comment": {"text": text},
        "languages": ["ja"],  
        "requestedAttributes": {"TOXICITY": {}}
    }
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(url, data=json.dumps(data), headers=headers)
    
    
    if response.status_code == 200:
        result = response.json()
        toxicity_score = result["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
        return toxicity_score
    else:
        print(f"Perspective API エラー: {response.status_code}, {response.text}")
        return None



# メッセージ受信時に動作する処理
@bot.event
async def on_message(message):
    
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return

    
    target_user = message.guild.get_member(449487835351744515)  # 指定されたユーザーを取得(ポテト)
    mentioned_user = message.mentions  # メンションされたユーザー(1人目)を取得

    #メンションされたユーザーがリスト入りしている場合
    # for user in mentioned_user:
    #     if user.id in TARGET_USER_IDS:
    #         await message.channel.send("test")
    #         def check(m):
    #             return m.author == mentioned_user and m.channel == message.channel
        
    #         try:
    #             # ユーザーからのメッセージを10秒以内に待機
    #             await bot.wait_for('message', timeout=10, check=check)
    #         except asyncio.TimeoutError:
    #             # ユーザーが返答しなかった場合、タイムアウト
    #             min = 1
    #             await target_user.timeout(timedelta(minutes=min), reason="ホモのためタイムアウト(応答なし)")
    #             await message.channel.send(f"{target_user} が応答の義務を果たさなかったため、ファックします。")

    
    #　リスト入りしているユーザーによりボットがメンションされた場合
    if message.author.id in TARGET_USER_IDS:

        #危険度を測定
        toxicity_score = await analyze_text(message.content)
        # 危険性が規定値以上に認められた場合
        if toxicity_score is not None and toxicity_score > TOXICITY_THRESHOLD:
            # タイムアウト（mute）処理
            min = 1  # 1分タイムアウト
            await target_user.timeout(timedelta(minutes=min), reason="ホモのためタイムアウト(危険度)")
            await message.channel.send(f"{target_user} の発言は不適切と判断したため、ファックします。{min}分間ミュートされます。危険度 = {toxicity_score}")

    #　その他ユーザーによりボットがメンションされた場合
    elif bot.user in message.mentions:
        # ユーザーが存在する場合
        if target_user:  
            #ポテトファッカーを実行
            await potato_fucker(message,target_user)
            
        else:
            await print("user=none")

    # 動作後、コマンド処理を続ける
    await bot.process_commands(message)


async def potato_fucker(message, target_user):
    # タイムアウト処理
        try:
            content_without_mentions = message.content
            for mention in message.mentions:
                # メンション部分以外のテキストを取得
                content_without_mentions = int(content_without_mentions.replace(mention.mention, ""))

            if content_without_mentions == "解除":
                await target_user.timeout(None)
            # メンション以外のテキストがint型に変換できる場合
            elif isinstance(content_without_mentions, int):
                min = content_without_mentions / 60
                
                # 指定時間タイムアウト
                await target_user.timeout(timedelta(minutes=min), reason="ホモのためタイムアウト(時間指定)")
                await message.channel.send(f"Potato was fucked! ({min}min) ")
            else:
                await target_user.timeout(timedelta(minutes=0.1), reason="ホモのためタイムアウト(デフォルト)")
                await message.channel.send("Potato was fucked!")
        except:
            #例外時、再度ポテトファックを試行
            #ここで例外が発生した場合はキャッチしない
            await target_user.timeout(timedelta(minutes=0.1), reason="ホモのためタイムアウト(例外)")
            await message.channel.send("Potato was fucked!")


#以下編集しないこと
TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
