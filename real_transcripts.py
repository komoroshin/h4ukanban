#!/usr/bin/env python3
from fireflies_client import FirefliesClient
import json

client = FirefliesClient()

print("\n🔍 Проверяем реальные транскрипты из Fireflies:\n")
print("=" * 70)

# Получаем последние 20 встреч
transcripts = client.get_recent_transcripts(20)

# Ищем встречи где есть хоть что-то в транскрипте
for i, t in enumerate(transcripts, 1):
    title = t.get('title', 'Без названия')
    date = t.get('date')
    sentences = t.get('sentences', [])
    
    # Показываем только встречи с транскриптом
    if sentences and len(sentences) > 3:
        print(f"\n#{i}. {title}")
        print(f"Дата: {date}")
        print(f"Реплик: {len(sentences)}")
        print(f"\nПервые 10 реплик:")
        print("-" * 70)
        
        for s in sentences[:10]:
            speaker = s.get('speaker_name', 'Unknown')
            text = s.get('text', '')
            print(f"{speaker}: {text}")
        
        print("=" * 70)

print("\n✅ Это ВСЕ реальные транскрипты из Fireflies")
