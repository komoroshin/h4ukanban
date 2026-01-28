#!/usr/bin/env python3
"""
Непрерывный мониторинг встреч healthy4u через Fireflies MCP
Автоматически проверяет новые встречи, фильтрует по проекту и извлекает action items
"""

import anthropic
import os
import json
import sys
import time
import signal
from pathlib import Path
from datetime import datetime, timedelta


class MeetingsMonitor:
    """Монитор встреч для автоматической обработки"""

    def __init__(self):
        self.running = True
        self.config = self.load_config()
        self.client = None
        self.base_dir = Path(__file__).parent / "meetings"
        self.action_items_dir = self.base_dir / "action_items"
        self.state_file = self.base_dir / ".monitor_state.json"

        # Создаем папки
        self.action_items_dir.mkdir(parents=True, exist_ok=True)

        # Загружаем состояние
        self.state = self.load_state()

        # Настраиваем обработку сигналов для graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def signal_handler(self, signum, frame):
        """Обработка сигнала завершения"""
        print("\n\n🛑 Получен сигнал завершения. Остановка мониторинга...")
        self.running = False

    def load_config(self):
        """Загружает конфигурацию проекта"""
        config_file = Path(__file__).parent / "config.json"
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                print(f"✅ Конфигурация загружена")
                return config
        except FileNotFoundError:
            print(f"❌ Файл конфигурации не найден: {config_file}")
            sys.exit(1)

    def load_state(self):
        """Загружает состояние мониторинга (последняя обработанная встреча)"""
        if self.state_file.exists():
            with open(self.state_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "last_check": None,
            "processed_meetings": [],
            "total_meetings_processed": 0,
            "total_action_items": 0
        }

    def save_state(self):
        """Сохраняет текущее состояние"""
        self.state["last_check"] = datetime.now().isoformat()
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, ensure_ascii=False, indent=2)

    def check_environment(self):
        """Проверяет наличие необходимых переменных окружения"""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            print("❌ ANTHROPIC_API_KEY не установлен")
            return False

        fireflies_key = os.getenv("FIREFLIES_API_KEY")
        if not fireflies_key:
            print("❌ FIREFLIES_API_KEY не установлен")
            return False

        return True

    def init_client(self):
        """Инициализирует Claude клиента"""
        if not self.check_environment():
            return False

        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        return True

    def process_new_meetings(self):
        """Обрабатывает новые встречи"""
        team_members = self.config.get("team_members", [])
        project_name = self.config.get("project_name", "healthy4u")

        if not team_members:
            print("⚠️  В конфигурации не указаны участники команды")
            return None

        # Формируем промпт для Claude
        prompt = f"""
Используя Fireflies MCP сервер, выполни следующую задачу:

## Цель
Найди НОВЫЕ встречи по проекту "{project_name}" и извлеки из них action items.

## Фильтрация
- Участники команды: {', '.join(team_members)}
- Ищи встречи где участвовал хотя бы один из этих людей
- Проверь последние 10 встреч
- Исключи встречи которые уже обработаны: {self.state.get('processed_meetings', [])}

## Что извлечь из КАЖДОЙ НОВОЙ встречи:

1. **Action Items**:
   - Описание задачи
   - Ответственный (если упоминался)
   - Срок (если указан)
   - Приоритет (high/medium/low)
   - Контекст

2. **Решения** - принятые решения

3. **Ключевые темы**

4. **Метрики** - упомянутые цифры, KPI

## Формат ответа

Верни JSON:

```json
{{
  "new_meetings": [
    {{
      "meeting_id": "id",
      "title": "название",
      "date": "дата ISO формат",
      "participants": ["участник1", "участник2"],
      "action_items": [
        {{
          "task": "описание",
          "assignee": "ответственный или null",
          "deadline": "срок или null",
          "priority": "high/medium/low",
          "context": "контекст"
        }}
      ],
      "decisions": ["решение 1"],
      "key_topics": ["тема 1"],
      "metrics": ["метрика 1"],
      "summary": "краткое резюме"
    }}
  ],
  "found_count": число_найденных,
  "processed_at": "{datetime.now().isoformat()}"
}}
```

Если новых встреч нет - верни empty array в new_meetings.
"""

        try:
            print(f"🔍 Проверка новых встреч... ({datetime.now().strftime('%H:%M:%S')})")

            response = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=16000,
                messages=[{"role": "user", "content": prompt}]
            )

            result_text = response.content[0].text

            # Извлекаем JSON
            import re
            json_match = re.search(r'```json\n(.*?)\n```', result_text, re.DOTALL)
            if not json_match:
                json_match = re.search(r'\{.*\}', result_text, re.DOTALL)

            if not json_match:
                print("⚠️  Не удалось извлечь JSON из ответа")
                return None

            result_json = json.loads(json_match.group(1) if json_match.lastindex else json_match.group(0))

            new_meetings = result_json.get("new_meetings", [])

            if not new_meetings:
                print("   ℹ️  Новых встреч не найдено")
                return None

            print(f"   ✅ Найдено новых встреч: {len(new_meetings)}")

            # Обрабатываем каждую встречу
            total_action_items = 0
            for meeting in new_meetings:
                meeting_id = meeting.get("meeting_id")
                action_items = meeting.get("action_items", [])
                total_action_items += len(action_items)

                # Добавляем в список обработанных
                if meeting_id not in self.state["processed_meetings"]:
                    self.state["processed_meetings"].append(meeting_id)

                print(f"   📋 {meeting.get('title')}: {len(action_items)} задач")

            # Обновляем статистику
            self.state["total_meetings_processed"] += len(new_meetings)
            self.state["total_action_items"] += total_action_items

            # Сохраняем результаты
            self.save_results(result_json)

            return result_json

        except Exception as e:
            print(f"❌ Ошибка при обработке: {e}")
            import traceback
            traceback.print_exc()
            return None

    def save_results(self, result_json):
        """Сохраняет результаты обработки"""
        # Сохраняем JSON
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        json_file = self.action_items_dir / f"batch_{timestamp}.json"

        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(result_json, f, ensure_ascii=False, indent=2)

        # Обновляем общий файл задач
        all_tasks_file = self.action_items_dir / "all_tasks.json"

        if all_tasks_file.exists():
            with open(all_tasks_file, 'r', encoding='utf-8') as f:
                all_tasks = json.load(f)
        else:
            all_tasks = {"tasks": []}

        # Добавляем новые задачи
        for meeting in result_json.get("new_meetings", []):
            for item in meeting.get("action_items", []):
                task = {
                    "id": f"{meeting['meeting_id']}_{len(all_tasks['tasks'])}",
                    "meeting_id": meeting["meeting_id"],
                    "meeting_title": meeting["title"],
                    "meeting_date": meeting["date"],
                    "task": item["task"],
                    "assignee": item.get("assignee"),
                    "deadline": item.get("deadline"),
                    "priority": item.get("priority", "medium"),
                    "context": item.get("context", ""),
                    "status": "open",
                    "created_at": datetime.now().isoformat()
                }
                all_tasks["tasks"].append(task)

        with open(all_tasks_file, 'w', encoding='utf-8') as f:
            json.dump(all_tasks, f, ensure_ascii=False, indent=2)

        # Генерируем markdown отчет
        self.generate_report(all_tasks)

        print(f"   💾 Результаты сохранены: {json_file.name}")

    def generate_report(self, all_tasks):
        """Генерирует markdown отчет"""
        tasks = [t for t in all_tasks.get("tasks", []) if t.get("status") == "open"]

        if not tasks:
            return

        # Группируем по приоритету
        high = [t for t in tasks if t.get("priority") == "high"]
        medium = [t for t in tasks if t.get("priority") == "medium"]
        low = [t for t in tasks if t.get("priority") == "low"]

        report = ["# Action Items - Открытые задачи\n"]
        report.append(f"**Обновлено:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report.append(f"**Всего задач:** {len(tasks)}\n")

        if high:
            report.append("## 🔴 Высокий приоритет\n")
            for task in high:
                report.append(f"- [ ] **{task['task']}**")
                if task.get('assignee'):
                    report.append(f"  - Ответственный: {task['assignee']}")
                if task.get('deadline'):
                    report.append(f"  - Срок: {task['deadline']}")
                report.append(f"  - Встреча: {task['meeting_title']} ({task['meeting_date']})")
                report.append("")

        if medium:
            report.append("## 🟡 Средний приоритет\n")
            for task in medium:
                report.append(f"- [ ] {task['task']}")
                if task.get('assignee'):
                    report.append(f"  - Ответственный: {task['assignee']}")
                report.append(f"  - Встреча: {task['meeting_title']}")
                report.append("")

        if low:
            report.append("## 🟢 Низкий приоритет\n")
            for task in low:
                report.append(f"- [ ] {task['task']}")
                report.append(f"  - Встреча: {task['meeting_title']}")
                report.append("")

        report_file = self.action_items_dir / "tasks_report.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(report))

    def run(self, interval_minutes=30):
        """
        Запускает непрерывный мониторинг

        Args:
            interval_minutes: Интервал проверки в минутах
        """
        print("=" * 60)
        print("🚀 Запуск мониторинга встреч healthy4u")
        print("=" * 60)
        print(f"📊 Проект: {self.config.get('project_name', 'healthy4u')}")
        print(f"👥 Участники: {', '.join(self.config.get('team_members', []))}")
        print(f"⏱️  Интервал проверки: {interval_minutes} минут")
        print(f"📁 Результаты: {self.action_items_dir}")
        print("=" * 60)
        print()

        if not self.init_client():
            print("❌ Не удалось инициализировать клиента")
            sys.exit(1)

        print("✅ Клиент инициализирован")
        print(f"📊 Статистика: обработано встреч: {self.state.get('total_meetings_processed', 0)}, "
              f"задач: {self.state.get('total_action_items', 0)}")
        print()
        print("🔄 Начинаем мониторинг... (Ctrl+C для остановки)\n")

        iteration = 0

        while self.running:
            try:
                iteration += 1
                print(f"[Итерация #{iteration}]")

                # Обрабатываем встречи
                result = self.process_new_meetings()

                # Сохраняем состояние
                self.save_state()

                if result:
                    print(f"   📊 Статистика: обработано встреч всего: {self.state['total_meetings_processed']}, "
                          f"задач всего: {self.state['total_action_items']}")

                # Ждем следующей проверки
                if self.running:
                    print(f"   ⏳ Следующая проверка через {interval_minutes} минут...")
                    print()

                    # Спим с возможностью прерывания
                    for _ in range(interval_minutes * 60):
                        if not self.running:
                            break
                        time.sleep(1)

            except KeyboardInterrupt:
                print("\n\n🛑 Остановка по Ctrl+C...")
                break
            except Exception as e:
                print(f"❌ Ошибка в цикле мониторинга: {e}")
                import traceback
                traceback.print_exc()

                # Продолжаем после ошибки
                if self.running:
                    print("⏳ Повтор через 5 минут...")
                    time.sleep(300)

        print("\n" + "=" * 60)
        print("✅ Мониторинг остановлен")
        print(f"📊 Итоговая статистика:")
        print(f"   • Обработано встреч: {self.state['total_meetings_processed']}")
        print(f"   • Извлечено задач: {self.state['total_action_items']}")
        print("=" * 60)


def main():
    """Главная функция"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Непрерывный мониторинг встреч healthy4u через Fireflies MCP",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:

  # Запустить с проверкой каждые 30 минут (по умолчанию)
  python monitor_meetings.py

  # Проверять каждые 15 минут
  python monitor_meetings.py --interval 15

  # Проверять каждый час
  python monitor_meetings.py --interval 60

  # Запустить в фоне (Linux/Mac)
  nohup python monitor_meetings.py &

  # Остановить мониторинг
  Ctrl+C или kill <PID>

Требования:
  - Настроенный Fireflies MCP сервер
  - ANTHROPIC_API_KEY в переменных окружения
  - FIREFLIES_API_KEY в переменных окружения
  - config.json с team_members
        """
    )

    parser.add_argument(
        "--interval",
        type=int,
        default=30,
        help="Интервал проверки новых встреч в минутах (по умолчанию: 30)"
    )

    parser.add_argument(
        "--once",
        action="store_true",
        help="Запустить только один раз (без непрерывного мониторинга)"
    )

    args = parser.parse_args()

    monitor = MeetingsMonitor()

    if args.once:
        print("🔄 Режим одноразовой проверки")
        monitor.init_client()
        monitor.process_new_meetings()
        monitor.save_state()
    else:
        monitor.run(interval_minutes=args.interval)


if __name__ == "__main__":
    main()
