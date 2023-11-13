# Schedule-TG-Bot

這是一台提醒機器人  
機器人的時區是: UTC+8  
這是我[機器人](https://t.me/EZMider_bot)的連接，
在私人聊天中直接傳送訊息即可觸發設定提醒。

指令說明: 
- 第一個字母不分大小寫
- /或者是!皆可使用
- 群組中只能使用指令設定提醒，與機器人的私人聊天可直接輸入提醒訊息，即可開始設定提醒
  - 指令:
  - 1.Schedule或S: 設定提醒，請將提醒內容添加在指令後方，如: !s 提醒訊息
  - 2.Delete或D: 刪除提醒
  - 3.Redo或R: 重新設定提醒，只會抓取設定中的最後五筆資料

## 開發

如果需要開發，需要創建以下資料:

- log/
- data/database.db
- .env

Pip
```
pip freeze > requests.txt
```

.env
```dotenv
TOKEN=您機器人的TOKEN
DB=data/database.db
DEV=開發者人員ID-1
DEV1=開發者人員ID-2
```
