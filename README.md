# DiscordBotTimerFunction
一個能夠在Discord指定伺服器中設定時間並準時呼叫身分組的DiscirdBot功能

---

# 以下是使用教學
## 安裝
- 安裝完成以後直接放到一個資料夾中解壓縮
- 解壓縮完成檔案結構大概長這樣
![](https://github.com/YuYue71/DiscordBotTimerFunction/blob/main/image/a.png)

## 初步設定
- 首先用編輯器打開`config.json`檔案
- 更改內容:
```bash
{
    "token": "在此填入你的DiscordBotToken"
}
```

## 啟動
- 雙擊`TimerDiscordBot.exe`
- 等待啟動,如出現下圖畫面表示啟動成功
![](https://github.com/YuYue71/DiscordBotTimerFunction/blob/main/image/b.png)

## 注意!!重要設定
- 啟動完成先別急著開心,此時的Bot功能在背景執行時會自動進入凍結狀態,導致功能失常
- 以下方法為 [關閉背景凍結狀態] 方法 (禁用 Quick Edit Mode):
  - 對完成的打包檔.exe右鍵 → 內容 → 選項 → 關閉快速編輯模式(如圖)
    ![](https://github.com/YuYue71/DiscordBotTimerFunction/blob/main/image/c.png)
- 如果以設定完成,此時你的Bot就能夠正常工作啦!!
