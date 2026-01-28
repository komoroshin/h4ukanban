#!/bin/bash
cd /Users/komoroshi/Documents/playground/healthy4u
source venv/bin/activate
source .env
export FIREFLIES_API_KEY
export ANTHROPIC_API_KEY
python3 monitor_meetings.py --interval 30
