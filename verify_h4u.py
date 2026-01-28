#!/usr/bin/env python3
import anthropic
import os

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

prompt = """
Используя Fireflies MCP, найди встречи 27 января 2025 года с участием irynamarchenko1@gmail.com.

Для каждой встречи покажи:
1. Название встречи
2. Точные первые 10-15 предложений из транскрипта (дословно!)
3. О чём реально говорили

Мне нужно проверить - действительно ли обсуждались темы про офис, pricing model, team building.
Покажи ТОЛЬКО то что реально есть в транскрипте.
"""

response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=6000,
    messages=[{"role": "user", "content": prompt}]
)

print(response.content[0].text)
