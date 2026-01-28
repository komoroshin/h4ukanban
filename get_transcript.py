#!/usr/bin/env python3
from fireflies_client import FirefliesClient
import json

client = FirefliesClient()

# Получаем конкретную встречу
transcript = client.get_transcript_by_id("aEJ2xNWMDWQQ39t4")

if transcript:
    print("\n📝 Полный транскрипт встречи:")
    print("=" * 60)
    print(f"Название: {transcript.get('title')}")
    print(f"Дата: {transcript.get('date')}")
    print(f"Длительность: {transcript.get('duration')} сек")
    print(f"Участники: {transcript.get('participants', [])}")
    print("\n" + "=" * 60)
    
    # Показываем текст
    sentences = transcript.get('sentences', [])
    if sentences:
        print("\n💬 Разговор:\n")
        current_speaker = None
        for s in sentences:
            speaker = s.get('speaker_name', 'Unknown')
            text = s.get('text', '')
            
            if speaker != current_speaker:
                print(f"\n{speaker}:")
                current_speaker = speaker
            
            print(f"  {text}")
    
    # Показываем summary от Fireflies
    summary = transcript.get('summary', {})
    if summary:
        print("\n\n" + "=" * 60)
        print("📊 Summary от Fireflies:")
        print("=" * 60)
        
        if summary.get('overview'):
            print(f"\nОбзор: {summary.get('overview')}")
        
        if summary.get('keywords'):
            print(f"\nКлючевые слова: {', '.join(summary.get('keywords', []))}")
        
        if summary.get('action_items'):
            print(f"\nAction Items от Fireflies:")
            for item in summary.get('action_items', []):
                print(f"  - {item}")
else:
    print("Встреча не найдена")
