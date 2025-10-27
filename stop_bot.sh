#!/bin/bash
if [ -f bot.pid ]; then
    kill $(cat bot.pid)
    rm bot.pid
    echo "Bot stopped"
else
    echo "Bot is not running"
fi

