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


    if bot.user in message.mentions:  # ボットがメンションされた場合
        target_user = message.guild.get_member(541887811742334987)  # 指定されたユーザーを取得
        if target_user:  # ユーザーが存在する場合
            # タイムアウト処理 (例: 10分)
            # timeout_duration = discord.utils.utcnow() + discord.timedelta(minutes=0.1)
            # await target_user.edit(timeout=timeout_duration)

            duration = datetime.timedelta(seconds=10, minutes=0, hours= 0, days=0)
            await target_user.timeout(duration, reason="gay")
            
            # await target_user.timeout_for(timeout_duration)
            await message.channel.send(f"{target_user.mention} さんはタイムアウトされました。")
        else:
            await message.channel.send(f"指定されたユーザーが見つかりませんでした。")

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
