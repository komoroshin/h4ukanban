#!/usr/bin/env python3
from fireflies_client import FirefliesClient

client = FirefliesClient()
transcripts = client.get_recent_transcripts(20)

# Ищем "Штурм по проектам"
for t in transcripts:
    if 'Штурм' in t.get('title', ''):
        print(f"\n📅 {t.get('title')}")
        print(f"ID: {t.get('id')}")
        print(f"Дата: {t.get('date')}")
        print(f"Длительность: {t.get('duration')} сек")
        
        sentences = t.get('sentences', [])
        print(f"Количество реплик: {len(sentences)}")
        print("\n💬 ПОЛНЫЙ ТРАНСКРИПТ:\n")
        print("=" * 70)
        
        current_speaker = None
        for s in sentences:
            speaker = s.get('speaker_name', 'Unknown')
            text = s.get('text', '')
            
            if speaker != current_speaker:
                print(f"\n{speaker}:")
                current_speaker = speaker
            
            print(f"  {text}")
        
        print("\n" + "=" * 70)
        
        # Summary
        summary = t.get('summary', {})
        if summary:
            print("\n📊 Summary от Fireflies:")
            if summary.get('overview'):
                print(f"Обзор: {summary.get('overview')}")
            if summary.get('action_items'):
                print("\nAction items:")
                for item in summary.get('action_items', []):
                    print(f"  - {item}")

