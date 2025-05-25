#!/usr/bin/env sh

source bin/activate
nohup python3 -u ./src/main.py > data/logs.txt &
