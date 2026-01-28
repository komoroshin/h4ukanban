#!/usr/bin/env python3
from fireflies_client import FirefliesClient
import json
from datetime import datetime

client = FirefliesClient()
transcripts = client.get_recent_transcripts(10)

print("\n🔍 Последние 10 встреч с содержимым:\n")

for i, t in enumerate(transcripts, 1):
    print("=" * 70)
    print(f"#{i}. {t.get('title', 'Без названия')}")
    print(f"ID: {t.get('id')}")
    print(f"Дата: {t.get('date')}")
    print(f"Длительность: {t.get('duration')} сек")
    
    # Показываем первые несколько предложений
    sentences = t.get('sentences', [])
    if sentences:
        print(f"\n💬 Начало разговора (первые 5 реплик):")
        for s in sentences[:5]:
            speaker = s.get('speaker_name', 'Unknown')
            text = s.get('text', '')
            print(f"  {speaker}: {text[:100]}{'...' if len(text) > 100 else ''}")
    
    # Summary от Fireflies
    summary = t.get('summary', {})
    if summary and summary.get('overview'):
        print(f"\n📝 Обзор: {summary.get('overview')[:200]}...")
    
    print()

