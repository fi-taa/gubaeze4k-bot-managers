# Telegram Bot to Group Bridge

A Python bot that forwards messages from users to a Telegram group and reflects replies back to users.

## Setup

1. Create a Telegram bot using [@BotFather](https://t.me/BotFather)
2. Get your bot token
3. Add the bot to your target group and make it an admin
4. Get your group chat ID (send a message in the group and visit: https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates)

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file:

```
BOT_TOKEN=your_bot_token_here
GROUP_CHAT_ID=your_group_chat_id_here
```

## Usage

Run the bot:

```bash
python main.py
```

## How it works

1. Users send messages to your bot
2. Bot forwards these messages to the specified group
3. When someone replies in the group, the bot sends the reply back to the original user

