#!/usr/bin/env python3
"""Анализ встречи 'Штурм по проектам' с извлечением action items"""
import os
from fireflies_client import FirefliesClient
from anthropic import Anthropic
import json

def analyze_meeting(transcript_data):
    """Анализирует встречу через Claude API напрямую"""
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    # Формируем текст транскрипта
    title = transcript_data.get('title', 'Unknown')
    date = transcript_data.get('date', 'Unknown')
    sentences = transcript_data.get('sentences', [])

    # Собираем текст по спикерам
    transcript_text = []
    current_speaker = None
    for s in sentences:
        speaker = s.get('speaker_name', 'Unknown')
        text = s.get('text', '')

        if speaker != current_speaker:
            transcript_text.append(f"\n{speaker}:")
            current_speaker = speaker

        transcript_text.append(f"  {text}")

    full_transcript = "\n".join(transcript_text)

    # Промпт для Claude
    prompt = f"""Проанализируй транскрипт встречи по проекту healthy4u и извлеки:

1. **Action Items** - конкретные задачи, которые нужно выполнить:
   - Что нужно сделать
   - Кто ответственен (если упоминается)
   - Срок (если упоминается)
   - Приоритет (high/medium/low)

2. **Решения** - принятые решения по проекту

3. **Ключевые темы** - основные обсуждаемые темы

Встреча: {title}
Дата: {date}

ТРАНСКРИПТ:
{full_transcript}

Верни результат в JSON формате:
{{
  "action_items": [
    {{
      "task": "описание задачи",
      "assignee": "имя или null",
      "deadline": "срок или null",
      "priority": "high/medium/low",
      "context": "краткий контекст из обсуждения"
    }}
  ],
  "decisions": [
    "решение 1",
    "решение 2"
  ],
  "key_topics": [
    "тема 1",
    "тема 2"
  ]
}}

ВАЖНО: Извлекай только РЕАЛЬНЫЕ задачи и решения из транскрипта. Не придумывай ничего."""

    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=4000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    response_text = message.content[0].text

    # Извлекаем JSON из ответа
    try:
        # Ищем JSON блок в ответе
        start = response_text.find('{')
        end = response_text.rfind('}') + 1
        if start != -1 and end > start:
            json_str = response_text[start:end]
            return json.loads(json_str)
    except Exception as e:
        print(f"Ошибка парсинга JSON: {e}")
        print(f"Ответ Claude:\n{response_text}")
        return None

def main():
    client = FirefliesClient()

    # Получаем последние транскрипты
    print("🔍 Поиск встречи 'Штурм по проектам'...\n")
    transcripts = client.get_recent_transcripts(20)

    # Ищем "Штурм"
    shturm_meeting = None
    for t in transcripts:
        if 'Штурм' in t.get('title', ''):
            shturm_meeting = t
            break

    if not shturm_meeting:
        print("❌ Встреча 'Штурм' не найдена")
        return

    print(f"✅ Найдена встреча: {shturm_meeting.get('title')}")
    print(f"   Дата: {shturm_meeting.get('date')}")
    print(f"   Длительность: {shturm_meeting.get('duration')} сек")
    print(f"   Количество реплик: {len(shturm_meeting.get('sentences', []))}")
    print("\n📊 Анализирую встречу через Claude...\n")

    # Анализируем
    result = analyze_meeting(shturm_meeting)

    if not result:
        print("❌ Не удалось извлечь данные")
        return

    # Сохраняем результат
    output_file = "meetings/action_items/shturm_analysis.json"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    full_result = {
        "meeting_id": shturm_meeting.get('id'),
        "title": shturm_meeting.get('title'),
        "date": shturm_meeting.get('date'),
        "duration": shturm_meeting.get('duration'),
        "analysis": result
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(full_result, f, ensure_ascii=False, indent=2)

    print(f"💾 Результаты сохранены в: {output_file}\n")

    # Выводим на экран
    print("=" * 70)
    print("📋 ACTION ITEMS:")
    print("=" * 70)

    for i, item in enumerate(result.get('action_items', []), 1):
        priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(item.get('priority', 'low'), "⚪")
        print(f"\n{i}. {priority_emoji} {item.get('task')}")
        if item.get('assignee'):
            print(f"   👤 Ответственный: {item.get('assignee')}")
        if item.get('deadline'):
            print(f"   📅 Срок: {item.get('deadline')}")
        if item.get('context'):
            print(f"   💡 Контекст: {item.get('context')}")

    print("\n" + "=" * 70)
    print("✅ РЕШЕНИЯ:")
    print("=" * 70)
    for i, decision in enumerate(result.get('decisions', []), 1):
        print(f"{i}. {decision}")

    print("\n" + "=" * 70)
    print("🎯 КЛЮЧЕВЫЕ ТЕМЫ:")
    print("=" * 70)
    for i, topic in enumerate(result.get('key_topics', []), 1):
        print(f"{i}. {topic}")

    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
