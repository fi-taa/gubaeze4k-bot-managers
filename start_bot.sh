#!/bin/bash
cd /Users/m3/fitaa/gubaeze4kbot
python3 main.py > bot.log 2>&1 &
echo $! > bot.pid
echo "Bot started with PID: $(cat bot.pid)"
echo "Logs: tail -f bot.log"

