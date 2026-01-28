#!/usr/bin/env python3
import os
from fireflies_client import FirefliesClient

client = FirefliesClient()

print("\n🔍 Поиск встреч healthy4u среди последних 20:\n")
transcripts = client.get_recent_transcripts(20)

keywords = ["healthy4u", "H4U", "здоровье", "healthy"]
found = []

for t in transcripts:
    title = t.get('title', '').lower()
    # Проверяем ключевые слова в названии
    if any(kw.lower() in title for kw in keywords):
        found.append(t)
        
if found:
    print(f"✅ Найдено {len(found)} встреч по healthy4u:\n")
    for i, t in enumerate(found, 1):
        print(f"{i}. {t.get('title')}")
        print(f"   Дата: {t.get('date')}")
        print(f"   Организатор: {t.get('organizer_email', 'N/A')}")
        participants = t.get('participants', [])
        if participants:
            print(f"   Участники: {', '.join(participants[:3])}")
        print()
else:
    print("❌ Встреч с упоминанием healthy4u не найдено")
    print("\n📋 Все встречи:")
    for i, t in enumerate(transcripts[:10], 1):
        print(f"{i}. {t.get('title', 'Без названия')}")
