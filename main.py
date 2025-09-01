import discord
from discord.ext import commands
import json
import Timing

# Intents 設定
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="T!", intents=intents)  # 設定指令前綴

Timing.Timer(bot)

# 當 Bot 啟動完成後顯示訊息
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    print("-# \"幽月YuYue\" 保有所有權利")

# 讀取 config.json 檔案中 Discord Bot Token
with open('config.json', 'r') as config_file:
    config = json.load(config_file)
    DISCORD_TOKEN = config.get('token')  # 從 config.json 讀取 token

# 啟動機器人
bot.run(DISCORD_TOKEN)