#!/usr/bin/env python3
"""
Обработчик транскриптов для извлечения action items и задач с помощью Claude API
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import anthropic


class TranscriptProcessor:
    """Обработчик транскриптов для извлечения задач и action items"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Инициализация процессора

        Args:
            api_key: API ключ Anthropic. Если не указан, берется из переменной окружения ANTHROPIC_API_KEY
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            print("⚠️  ANTHROPIC_API_KEY не установлен.")

        self.client = anthropic.Anthropic(api_key=self.api_key) if self.api_key else None

        # Папки для хранения данных
        self.base_dir = Path(__file__).parent / "meetings"
        self.transcripts_dir = self.base_dir / "transcripts"
        self.processed_dir = self.base_dir / "processed"
        self.action_items_dir = self.base_dir / "action_items"

        for dir_path in [self.transcripts_dir, self.processed_dir, self.action_items_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)

    def _format_transcript_text(self, transcript: Dict) -> str:
        """
        Форматирует транскрипт в читабельный текст

        Args:
            transcript: Данные транскрипта от Fireflies

        Returns:
            Отформатированный текст транскрипта
        """
        lines = []

        # Заголовок
        lines.append(f"# {transcript.get('title', 'Встреча')}")
        lines.append(f"Дата: {transcript.get('date', 'N/A')}")
        lines.append(f"Длительность: {transcript.get('duration', 'N/A')} мин")

        # Участники
        participants = transcript.get('participants', [])
        if participants:
            lines.append(f"Участники: {', '.join(participants)}")

        lines.append("\n## Транскрипт\n")

        # Текст разговора
        sentences = transcript.get('sentences', [])
        current_speaker = None

        for sentence in sentences:
            speaker = sentence.get('speaker_name', 'Неизвестный')
            text = sentence.get('text', '')

            if speaker != current_speaker:
                lines.append(f"\n**{speaker}:**")
                current_speaker = speaker

            lines.append(text)

        return "\n".join(lines)

    def extract_action_items(self, transcript: Dict) -> Dict:
        """
        Извлекает action items и задачи из транскрипта с помощью Claude

        Args:
            transcript: Данные транскрипта

        Returns:
            Структурированные данные с action items
        """
        if not self.client:
            raise ValueError("Claude API клиент не инициализирован. Установите ANTHROPIC_API_KEY")

        transcript_text = self._format_transcript_text(transcript)

        prompt = """Проанализируй транскрипт встречи и извлеки из него следующую информацию:

1. **Action Items** - конкретные задачи, которые нужно выполнить
2. **Решения** - принятые на встрече решения
3. **Ключевые темы** - основные темы обсуждения
4. **Следующие шаги** - что нужно сделать дальше

Для каждого action item укажи:
- Что нужно сделать (описание задачи)
- Кто ответственный (если упоминалось)
- Срок (если упоминался)
- Приоритет (высокий/средний/низкий на основе контекста разговора)

Верни результат в формате JSON со следующей структурой:
{
  "action_items": [
    {
      "task": "описание задачи",
      "assignee": "ответственный или null",
      "deadline": "срок или null",
      "priority": "high/medium/low",
      "context": "краткий контекст из обсуждения"
    }
  ],
  "decisions": [
    "решение 1",
    "решение 2"
  ],
  "key_topics": [
    "тема 1",
    "тема 2"
  ],
  "next_steps": [
    "следующий шаг 1",
    "следующий шаг 2"
  ],
  "summary": "краткое резюме встречи (2-3 предложения)"
}

Транскрипт встречи:

"""

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=4000,
                messages=[
                    {
                        "role": "user",
                        "content": prompt + transcript_text
                    }
                ]
            )

            # Извлекаем JSON из ответа
            response_text = message.content[0].text

            # Пытаемся найти JSON в ответе
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                extracted_data = json.loads(json_match.group())
            else:
                extracted_data = json.loads(response_text)

            # Добавляем метаданные
            result = {
                "meeting_id": transcript.get("id"),
                "meeting_title": transcript.get("title"),
                "meeting_date": transcript.get("date"),
                "processed_at": datetime.now().isoformat(),
                "extracted_data": extracted_data
            }

            return result

        except Exception as e:
            print(f"❌ Ошибка при обработке транскрипта: {e}")
            raise

    def process_transcript_file(self, filepath: str) -> Path:
        """
        Обрабатывает файл транскрипта и сохраняет извлеченные action items

        Args:
            filepath: Путь к файлу транскрипта

        Returns:
            Путь к файлу с обработанными данными
        """
        print(f"📝 Обработка транскрипта: {filepath}")

        # Загружаем транскрипт
        with open(filepath, 'r', encoding='utf-8') as f:
            transcript = json.load(f)

        # Извлекаем action items
        result = self.extract_action_items(transcript)

        # Сохраняем результат
        filename = Path(filepath).stem + "_processed.json"
        output_path = self.processed_dir / filename

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"✅ Результат сохранен: {output_path}")

        # Также сохраняем в папку action_items отдельный файл с задачами
        self._save_action_items(result)

        return output_path

    def _save_action_items(self, result: Dict):
        """
        Сохраняет action items в отдельную базу задач

        Args:
            result: Результат обработки транскрипта
        """
        action_items_file = self.action_items_dir / "all_tasks.json"

        # Загружаем существующие задачи
        if action_items_file.exists():
            with open(action_items_file, 'r', encoding='utf-8') as f:
                all_tasks = json.load(f)
        else:
            all_tasks = {"tasks": []}

        # Добавляем новые задачи
        extracted = result.get("extracted_data", {})
        for item in extracted.get("action_items", []):
            task = {
                "id": f"{result['meeting_id']}_{len(all_tasks['tasks'])}",
                "meeting_id": result["meeting_id"],
                "meeting_title": result["meeting_title"],
                "meeting_date": result["meeting_date"],
                "task": item["task"],
                "assignee": item.get("assignee"),
                "deadline": item.get("deadline"),
                "priority": item.get("priority", "medium"),
                "context": item.get("context", ""),
                "status": "open",
                "created_at": result["processed_at"]
            }
            all_tasks["tasks"].append(task)

        # Сохраняем обновленный список
        with open(action_items_file, 'w', encoding='utf-8') as f:
            json.dump(all_tasks, f, ensure_ascii=False, indent=2)

        print(f"📋 Добавлено задач: {len(extracted.get('action_items', []))}")

    def process_all_transcripts(self):
        """
        Обрабатывает все транскрипты в папке transcripts
        """
        transcript_files = list(self.transcripts_dir.glob("*.json"))

        if not transcript_files:
            print("⚠️  Нет транскриптов для обработки")
            return

        print(f"🔄 Найдено транскриптов: {len(transcript_files)}")

        for filepath in transcript_files:
            # Проверяем, не обработан ли уже этот файл
            processed_filename = filepath.stem + "_processed.json"
            if (self.processed_dir / processed_filename).exists():
                print(f"⏭️  Пропускаем (уже обработан): {filepath.name}")
                continue

            try:
                self.process_transcript_file(str(filepath))
            except Exception as e:
                print(f"❌ Ошибка при обработке {filepath.name}: {e}")

        print("\n✅ Обработка завершена!")

    def get_open_tasks(self) -> List[Dict]:
        """
        Получить список открытых задач

        Returns:
            Список открытых задач
        """
        action_items_file = self.action_items_dir / "all_tasks.json"

        if not action_items_file.exists():
            return []

        with open(action_items_file, 'r', encoding='utf-8') as f:
            all_tasks = json.load(f)

        return [task for task in all_tasks.get("tasks", []) if task.get("status") == "open"]

    def generate_tasks_report(self) -> str:
        """
        Генерирует отчет по задачам в markdown формате

        Returns:
            Markdown текст отчета
        """
        tasks = self.get_open_tasks()

        if not tasks:
            return "## Открытых задач нет\n"

        # Группируем по приоритету
        high_priority = [t for t in tasks if t.get("priority") == "high"]
        medium_priority = [t for t in tasks if t.get("priority") == "medium"]
        low_priority = [t for t in tasks if t.get("priority") == "low"]

        report = ["# Action Items - Открытые задачи\n"]
        report.append(f"**Всего задач:** {len(tasks)}\n")

        if high_priority:
            report.append("## 🔴 Высокий приоритет\n")
            for task in high_priority:
                report.append(f"- [ ] **{task['task']}**")
                if task.get('assignee'):
                    report.append(f"  - Ответственный: {task['assignee']}")
                if task.get('deadline'):
                    report.append(f"  - Срок: {task['deadline']}")
                report.append(f"  - Встреча: {task['meeting_title']} ({task['meeting_date']})")
                report.append("")

        if medium_priority:
            report.append("## 🟡 Средний приоритет\n")
            for task in medium_priority:
                report.append(f"- [ ] {task['task']}")
                if task.get('assignee'):
                    report.append(f"  - Ответственный: {task['assignee']}")
                if task.get('deadline'):
                    report.append(f"  - Срок: {task['deadline']}")
                report.append(f"  - Встреча: {task['meeting_title']} ({task['meeting_date']})")
                report.append("")

        if low_priority:
            report.append("## 🟢 Низкий приоритет\n")
            for task in low_priority:
                report.append(f"- [ ] {task['task']}")
                if task.get('assignee'):
                    report.append(f"  - Ответственный: {task['assignee']}")
                report.append(f"  - Встреча: {task['meeting_title']} ({task['meeting_date']})")
                report.append("")

        return "\n".join(report)


def main():
    """Основная функция для тестирования процессора"""
    processor = TranscriptProcessor()

    if not processor.client:
        print("\n📋 Для работы необходим API ключ Anthropic:")
        print("1. Получите ключ на https://console.anthropic.com/")
        print("2. Установите переменную окружения: export ANTHROPIC_API_KEY='ваш_ключ'")
        print("   Или создайте файл .env с содержимым: ANTHROPIC_API_KEY=ваш_ключ")
        return

    # Обрабатываем все транскрипты
    processor.process_all_transcripts()

    # Генерируем отчет
    report = processor.generate_tasks_report()
    print("\n" + report)

    # Сохраняем отчет
    report_path = processor.action_items_dir / "tasks_report.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\n📄 Отчет сохранен: {report_path}")


if __name__ == "__main__":
    main()
