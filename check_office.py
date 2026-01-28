#!/usr/bin/env python3
import anthropic
import os

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

prompt = """
Используя Fireflies MCP сервер, найди встречу где обсуждалась тема про офис (office location, переезд офиса).

Нужно понять:
1. Была ли вообще такая встреча?
2. Если да - покажи точную цитату из транскрипта
3. ID встречи
4. Когда это было

Если такой встречи не было - скажи прямо.
"""

response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=4000,
    messages=[{"role": "user", "content": prompt}]
)

print(response.content[0].text)
