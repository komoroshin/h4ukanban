#!/usr/bin/env python3
import os
from fireflies_client import FirefliesClient

# Создаем клиента
client = FirefliesClient()

# Получаем последние 5 встреч БЕЗ фильтрации
print("\n🔍 Проверка последних 5 встреч в Fireflies:\n")
transcripts = client.get_recent_transcripts(5)

if not transcripts:
    print("❌ Встреч не найдено")
else:
    for i, t in enumerate(transcripts, 1):
        print(f"{i}. {t.get('title', 'Без названия')}")
        print(f"   Дата: {t.get('date', 'N/A')}")
        print(f"   Организатор: {t.get('organizer_email', 'N/A')}")
        participants = t.get('participants', [])
        if participants:
            print(f"   Участники ({len(participants)}):")
            for p in participants[:5]:  # Показываем первых 5
                print(f"      - {p}")
            if len(participants) > 5:
                print(f"      ... и еще {len(participants) - 5}")
        else:
            print(f"   Участники: нет данных")
        print()
