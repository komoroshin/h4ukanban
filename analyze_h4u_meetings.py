#!/usr/bin/env python3
from fireflies_client import FirefliesClient
import anthropic
import os
import json

client_ff = FirefliesClient()
client_ai = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Получаем встречи
transcripts = client_ff.get_recent_transcripts(20)

# Ищем Дейлики и Штурм по проектам
h4u_meetings = []
for t in transcripts:
    title = t.get('title', '')
    if 'Дейлик' in title or 'Штурм по проектам' in title:
        h4u_meetings.append(t)

print(f"\n🔍 Найдено {len(h4u_meetings)} встреч healthy4u:\n")

for meeting in h4u_meetings:
    print("=" * 70)
    print(f"📅 {meeting.get('title')}")
    print(f"Дата: {meeting.get('date')}")
    
    # Собираем полный текст транскрипта
    sentences = meeting.get('sentences', [])
    if not sentences:
        print("⚠️  Нет транскрипта")
        continue
    
    full_text = "\n".join([f"{s.get('speaker_name', 'Unknown')}: {s.get('text', '')}" for s in sentences])
    
    # Показываем начало
    print(f"\n💬 Первые 5 реплик:")
    for s in sentences[:5]:
        print(f"  {s.get('speaker_name', 'Unknown')}: {s.get('text', '')[:100]}...")
    
    # Анализируем через Claude БЕЗ MCP - напрямую передаем текст
    print(f"\n🤖 Анализирую через Claude...")
    
    prompt = f"""Проанализируй транскрипт встречи по проекту healthy4u и извлеки:

1. **Action items** - конкретные задачи (с приоритетом high/medium/low)
2. **Решения** - что решили
3. **Ключевые темы** - о чем говорили

**ВАЖНО:** Используй ТОЛЬКО информацию из транскрипта. Не придумывай ничего.

Транскрипт:
{full_text[:8000]}

Верни JSON:
{{
  "action_items": [
    {{"task": "описание", "priority": "high/medium/low", "context": "контекст"}}
  ],
  "decisions": ["решение 1"],
  "key_topics": ["тема 1"],
  "summary": "краткое резюме"
}}
"""
    
    try:
        response = client_ai.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        import re
        result_text = response.content[0].text
        json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
        
        if json_match:
            result = json.loads(json_match.group())
            
            print(f"\n📋 Action Items ({len(result.get('action_items', []))}):")
            for item in result.get('action_items', []):
                priority = item.get('priority', 'medium')
                emoji = '🔴' if priority == 'high' else '🟡' if priority == 'medium' else '🟢'
                print(f"  {emoji} {item.get('task')}")
            
            if result.get('decisions'):
                print(f"\n✅ Решения:")
                for dec in result.get('decisions', []):
                    print(f"  • {dec}")
            
            if result.get('key_topics'):
                print(f"\n🎯 Ключевые темы:")
                for topic in result.get('key_topics', []):
                    print(f"  • {topic}")
            
            print(f"\n📝 {result.get('summary', '')}")
    
    except Exception as e:
        print(f"❌ Ошибка анализа: {e}")
    
    print()

