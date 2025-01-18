#!/usr/bin/env sh

source bin/activate

nohup python3 -u ./src/bot.py > src/data/logs.txt &