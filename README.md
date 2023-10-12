# Schedule-TG-Bot

這是一台提醒機器人  
抓取的時間是取+8時區的  
我的[機器人](https://t.me/EZMider_bot)

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
FILE=log資料夾的完整路徑
DEV=開發者人員ID 1
DEV1=開發者人員ID 2
```