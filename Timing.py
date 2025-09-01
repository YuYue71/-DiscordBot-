import discord
from discord.ext import commands, tasks
import json
from datetime import datetime
import pytz
import re

def Timer(bot):
    # 驗證時間格式 (HH:MM)
    def valid_time_format(time_str):
        return re.match(r"^(?:[01]\d|2[0-3]):[0-5]\d$", time_str)
    
    # 讀取設定檔
    def load_settings():
        try:                # 如果有設定檔就讀取
            with open("TimingSet.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:             # 如果沒有設定檔就回傳空的
            return {}

    # 儲存設定檔
    def save_settings(data):
        with open("TimingSet.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    settings = load_settings()  # 載入設定檔

    # 新增定時器指令
    @bot.command()
    async def addtime(ctx, time: str, role: discord.Role, name: str, *, Remarks: str):  # 指令格式範例: T!addtime 14:30 @Role
        """T!addtime <HH:MM> @身分組 <定時器名字> <備註> → 新增一個定時器"""
        if len(name) > 4:          # 限制最多 4 個字
            await ctx.send("名字太長，最多 4 個字")
            return
        if len(name) == 0:
            await ctx.send("名字不能為空")
            return
        if not valid_time_format(time):             # 驗證時間格式
            await ctx.send("時間格式錯誤，請輸入 HH:MM")
            return
        hour, minute = time.split(":")              # 分割時間字串
        time = f"{int(hour):02d}:{int(minute):02d}" # 格式化時間 (去除前導零)
        guild_id = str(ctx.guild.id)    # 取得伺服器 ID
        if guild_id not in settings:    # 如果伺服器沒有設定就新增一個空的
            settings[guild_id] = []

        # 自動編號
        next_id = max([t["id"] for t in settings[guild_id]], default=0) + 1

        # 新增定時器
        timer = {
            "name": name,
            "id": next_id,
            "time": time,
            "role_id": role.id,
            "channel_id": ctx.channel.id,
            "Remarks": Remarks
        }

        # 加入設定並儲存
        settings[guild_id].append(timer)
        save_settings(settings)
        
        # 成功設定通知
        await ctx.send(f"已新增定時器 編號{next_id} 名字{name}→ {time} 提醒 {role.mention}")

    # 查表
    @bot.command()
    async def listtime(ctx):        # 指令格式範例: T!listtime
        """T!listtime → 查看伺服器的所有定時器"""
        guild_id = str(ctx.guild.id)
        timers = settings.get(guild_id, [])
        if not timers:
            await ctx.send("這個伺服器沒有設定定時器。")
            return

        msg = "📋**定時器列表**\n"
        for t in timers:
            role = ctx.guild.get_role(t["role_id"])     # 取得身分組物件
            role_name = role.mention if role else "(角色已刪除)"    # 如果身分組不存在就顯示已刪除
            msg += f"編號 `{t['id']}` | 名字 `{t['name']}` | 時間 `{t['time']}` | 通知 {role_name}\n"      # 顯示編號、時間、身分組
        await ctx.send(msg) # 發送列表訊息
        
    # 刪除
    @bot.command()
    async def deltime(ctx, timer_id: int):  # 指令格式範例: T!deltime 1
        """T!deltime <編號> → 刪除指定的定時器"""
        guild_id = str(ctx.guild.id)        # 取得伺服器 ID
        timers = settings.get(guild_id, []) # 取得該伺服器的定時器列表
        for t in timers:                    # 找到對應的定時器並刪除
            if t["id"] == timer_id:
                timers.remove(t)
                save_settings(settings)
                await ctx.send(f"已刪除定時器 #{timer_id}")
                return
        await ctx.send(f"找不到編號 {timer_id} 的定時器")   # 如果找不到就通知

    # 修改
    @bot.command()  
    async def edittime(ctx, timer_id: int, new_time: str, role: discord.Role, name: str, *, Remarks: str):  # 指令格式範例: T!edittime 1 15:00 @NewRole
        """T!edittime <編號> <HH:MM> @身分組 <定時器名字> <備註> → 修改指定的定時器"""
        if len(name) > 4:          # 限制最多 4 個字
            await ctx.send("名字太長，最多 4 個字")
            return
        if len(name) == 0:
            await ctx.send("名字不能為空")
            return
        if not valid_time_format(new_time):        # 驗證時間格式
            await ctx.send("時間格式錯誤，請輸入 HH:MM")
            return
        hour, minute = new_time.split(":")          # 分割時間字串
        time = f"{int(hour):02d}:{int(minute):02d}" # 格式化時間 (去除前導零)
        guild_id = str(ctx.guild.id)        # 取得伺服器 ID
        timers = settings.get(guild_id, []) # 取得該伺服器的定時器列表
        for t in timers:                    # 找到對應的定時器並修改
            if t["id"] == timer_id:
                t["name"] = name
                t["time"] = new_time
                t["role_id"] = role.id
                t["channel_id"] = ctx.channel.id
                t["Remarks"] = Remarks
                save_settings(settings)
                await ctx.send(f"已修改定時器 #{timer_id} → {new_time} 提醒 {role.mention}")    # 成功修改通知
                return
        await ctx.send(f"找不到編號 {timer_id} 的定時器")   # 如果找不到就通知

    # 這段套娃有點吃算力QQ
    @tasks.loop(minutes=1)              # 每分鐘檢查一次時間
    async def check_time():             # 定時檢查時間
        now = datetime.now(pytz.timezone("Asia/Taipei")).strftime("%H:%M")  # 取得當前時間 (台北時區)
        print(f"[Debug] 現在時間: {now}")
        for guild_id, timers in settings.items():   # 遍歷所有伺服器的定時器
            for t in timers:                        # 遍歷該伺服器的每個定時器
                if t["time"] == now:                # 如果時間符合
                    print(f"[Debug] 發送提醒 {t['role_id']}")
                    guild = bot.get_guild(int(guild_id))    # 取得伺服器物件
                    if guild:                               # 確保伺服器存在
                        channel = guild.get_channel(t["channel_id"])    # 取得頻道物件
                        role = guild.get_role(t["role_id"])             # 取得身分組物件
                        if channel and role:                            # 確保頻道和身分組存在
                            await channel.send(f"{role.mention} 現在是 `{now}`，{t['name']}時間到啦!!\n備註:\n> {t['Remarks']}")      # 發送提醒訊息
        
    # 啟動!!
    async def start_loop():
        if not check_time.is_running():
            check_time.start()
            print("計時任務已啟動")
            
    bot.add_listener(start_loop, "on_ready")