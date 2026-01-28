#!/usr/bin/env python3
"""
Автоматическая обработка встреч Fireflies для healthy4u
Запускается регулярно (каждый час) и обрабатывает новые встречи
"""
import os
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from fireflies_client import FirefliesClient
from anthropic import Anthropic

# Пути к файлам
STATE_FILE = Path("meetings/.auto_process_state.json")
TASKS_FILE = Path("meetings/action_items/tasks_clean.json")
KANBAN_HTML = Path("meetings/action_items/kanban.html")
LOG_FILE = Path("logs/auto_process.log")

def log(message):
    """Логирование с временной меткой"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}"
    print(log_message)

    # Записываем в файл
    LOG_FILE.parent.mkdir(exist_ok=True)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_message + "\n")

def load_state():
    """Загружает состояние обработанных встреч"""
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"processed_meetings": [], "last_check": None}

def save_state(state):
    """Сохраняет состояние обработанных встреч"""
    STATE_FILE.parent.mkdir(exist_ok=True)
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def analyze_meeting(transcript_data):
    """Анализирует встречу через Claude API напрямую"""
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

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

    try:
        message = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=4000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        response_text = message.content[0].text

        # Извлекаем JSON из ответа
        start = response_text.find('{')
        end = response_text.rfind('}') + 1
        if start != -1 and end > start:
            json_str = response_text[start:end]
            return json.loads(json_str)
    except Exception as e:
        log(f"Ошибка анализа встречи: {e}")
        return None

def is_recent_meeting(meeting_date_ms, hours=2):
    """Проверяет, была ли встреча в последние N часов"""
    # Fireflies возвращает timestamp в миллисекундах
    meeting_time = datetime.fromtimestamp(meeting_date_ms / 1000)
    now = datetime.now()
    time_diff = now - meeting_time

    return time_diff < timedelta(hours=hours)

def load_tasks():
    """Загружает текущие задачи из JSON"""
    if TASKS_FILE.exists():
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "project": "healthy4u",
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source": "auto_processing",
        "tasks": {
            "todo": [],
            "in_progress": [],
            "done": []
        },
        "summary": {
            "total": 0,
            "by_priority": {"high": 0, "medium": 0, "low": 0},
            "by_assignee": {}
        }
    }

def add_tasks_to_board(meeting_id, meeting_title, meeting_date, analysis_result):
    """Добавляет задачи из встречи в канбан"""
    tasks_data = load_tasks()

    action_items = analysis_result.get('action_items', [])

    added_count = 0
    for item in action_items:
        # Генерируем уникальный ID
        task_id = f"{meeting_id}_{added_count}"

        # Проверяем, не добавлена ли уже эта задача
        existing = any(
            t.get('id') == task_id
            for t in tasks_data['tasks']['todo']
        )

        if not existing:
            task = {
                "id": task_id,
                "meeting_id": meeting_id,
                "meeting_title": meeting_title,
                "meeting_date": meeting_date,
                "title": item.get('task'),
                "assignee": item.get('assignee'),
                "deadline": item.get('deadline'),
                "priority": item.get('priority', 'medium'),
                "context": item.get('context'),
                "status": "todo",
                "created_at": datetime.now().isoformat()
            }

            tasks_data['tasks']['todo'].append(task)
            added_count += 1

    # Обновляем статистику
    all_tasks = (
        tasks_data['tasks']['todo'] +
        tasks_data['tasks']['in_progress'] +
        tasks_data['tasks']['done']
    )

    tasks_data['summary']['total'] = len(all_tasks)
    tasks_data['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Подсчитываем по приоритетам
    for priority in ['high', 'medium', 'low']:
        count = sum(1 for t in all_tasks if t.get('priority') == priority)
        tasks_data['summary']['by_priority'][priority] = count

    # Подсчитываем по исполнителям
    assignee_counts = {}
    for task in all_tasks:
        assignee = task.get('assignee')
        if assignee:
            assignee_counts[assignee] = assignee_counts.get(assignee, 0) + 1
    tasks_data['summary']['by_assignee'] = assignee_counts

    # Сохраняем
    TASKS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks_data, f, ensure_ascii=False, indent=2)

    log(f"Добавлено задач: {added_count} из встречи '{meeting_title}'")

    return added_count

def regenerate_kanban():
    """Регенерирует HTML канбана из JSON"""
    tasks_data = load_tasks()

    # Формируем JavaScript массив задач
    all_tasks = (
        tasks_data['tasks']['todo'] +
        tasks_data['tasks']['in_progress'] +
        tasks_data['tasks']['done']
    )

    # Преобразуем в формат для канбана
    kanban_tasks = []
    for task in all_tasks:
        kanban_tasks.append({
            "id": task.get('id'),
            "title": task.get('title'),
            "assignee": task.get('assignee'),
            "deadline": task.get('deadline'),
            "priority": task.get('priority', 'medium'),
            "context": task.get('context', ''),
            "status": task.get('status', 'todo')
        })

    # Читаем шаблон канбана
    with open(KANBAN_HTML, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Заменяем массив задач
    tasks_json = json.dumps(kanban_tasks, ensure_ascii=False, indent=12)

    # Находим и заменяем tasks = [...]
    start_marker = "const tasks = ["
    end_marker = "        ];"

    start_idx = html_content.find(start_marker)
    if start_idx != -1:
        end_idx = html_content.find(end_marker, start_idx)
        if end_idx != -1:
            new_html = (
                html_content[:start_idx + len(start_marker)] +
                "\n" + tasks_json[1:-1] +  # Убираем внешние []
                "\n" + html_content[end_idx:]
            )

            with open(KANBAN_HTML, 'w', encoding='utf-8') as f:
                f.write(new_html)

            log(f"Канбан обновлен: {len(kanban_tasks)} задач")

def process_meetings():
    """Основная функция обработки встреч"""
    log("=" * 70)
    log("Запуск автоматической обработки встреч healthy4u")

    # Загружаем состояние
    state = load_state()

    # Подключаемся к Fireflies
    client = FirefliesClient()

    try:
        # Получаем последние встречи (за последние 48 часов)
        log("Получение списка встреч из Fireflies...")
        transcripts = client.get_recent_transcripts(50)

        log(f"Найдено встреч: {len(transcripts)}")

        # Фильтруем встречи по healthy4u (по заголовку или участникам)
        h4u_meetings = []
        for t in transcripts:
            title = t.get('title', '').lower()
            # Ищем встречи с ключевыми словами
            if any(keyword in title for keyword in ['healthy4u', 'h4u', 'дейлик', 'штурм']):
                h4u_meetings.append(t)

        log(f"Встреч healthy4u: {len(h4u_meetings)}")

        # Обрабатываем только новые встречи за последние 2 часа
        new_meetings = []
        for meeting in h4u_meetings:
            meeting_id = meeting.get('id')
            meeting_date = meeting.get('date')

            # Проверяем, не обработана ли уже
            if meeting_id in state['processed_meetings']:
                continue

            # Проверяем, что встреча недавняя (последние 2 часа)
            if is_recent_meeting(meeting_date, hours=2):
                new_meetings.append(meeting)

        log(f"Новых встреч для обработки: {len(new_meetings)}")

        # Обрабатываем каждую новую встречу
        total_tasks_added = 0
        for meeting in new_meetings:
            meeting_id = meeting.get('id')
            meeting_title = meeting.get('title')
            meeting_date = meeting.get('date')

            log(f"Обработка: {meeting_title}")

            # Анализируем встречу через Claude
            analysis = analyze_meeting(meeting)

            if analysis:
                # Добавляем задачи в канбан
                tasks_added = add_tasks_to_board(
                    meeting_id,
                    meeting_title,
                    meeting_date,
                    analysis
                )
                total_tasks_added += tasks_added

                # Сохраняем результат анализа
                analysis_file = Path(f"meetings/action_items/analysis_{meeting_id}.json")
                with open(analysis_file, 'w', encoding='utf-8') as f:
                    json.dump({
                        "meeting_id": meeting_id,
                        "title": meeting_title,
                        "date": meeting_date,
                        "analysis": analysis
                    }, f, ensure_ascii=False, indent=2)

                # Отмечаем встречу как обработанную
                state['processed_meetings'].append(meeting_id)
            else:
                log(f"Ошибка анализа встречи: {meeting_title}")

        # Если были добавлены задачи, обновляем канбан
        if total_tasks_added > 0:
            log(f"Всего добавлено задач: {total_tasks_added}")
            regenerate_kanban()
        else:
            log("Новых задач не добавлено")

        # Сохраняем состояние
        state['last_check'] = datetime.now().isoformat()
        save_state(state)

        log("Обработка завершена успешно")

    except Exception as e:
        log(f"ОШИБКА: {e}")
        import traceback
        log(traceback.format_exc())

if __name__ == "__main__":
    process_meetings()
