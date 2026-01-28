#!/usr/bin/env python3
"""
Автоматическая обработка транскриптов встреч healthy4u через MCP
Использует Fireflies MCP сервер для прямого доступа к данным встреч
"""

import anthropic
import os
import json
import sys
from pathlib import Path
from datetime import datetime


def load_config():
    """Загружает конфигурацию проекта"""
    config_file = Path(__file__).parent / "config.json"
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️  Файл конфигурации не найден: {config_file}")
        return {"team_members": [], "project_name": "healthy4u"}


def check_environment():
    """Проверяет наличие необходимых переменных окружения"""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY не установлен")
        print("\n📋 Установите переменную окружения:")
        print("   export ANTHROPIC_API_KEY='ваш_ключ'")
        print("   Или создайте файл .env")
        print("\n📖 Получить ключ: https://console.anthropic.com/")
        return False

    fireflies_key = os.getenv("FIREFLIES_API_KEY")
    if not fireflies_key:
        print("⚠️  FIREFLIES_API_KEY не установлен")
        print("   Для работы MCP сервера нужен этот ключ")
        print("   Получить: https://app.fireflies.ai/integrations/custom/fireflies")
        return False

    return True


def process_meetings_with_mcp(limit: int = 20):
    """
    Обрабатывает встречи используя Claude с MCP сервером Fireflies

    Args:
        limit: Количество последних встреч для обработки
    """
    print("=" * 60)
    print("🚀 Обработка встреч healthy4u через Fireflies MCP")
    print("=" * 60)
    print()

    if not check_environment():
        sys.exit(1)

    config = load_config()
    team_members = config.get("team_members", [])
    project_name = config.get("project_name", "healthy4u")

    if not team_members:
        print("⚠️  В конфигурации не указаны участники команды")
        print("   Отредактируйте config.json и добавьте team_members")
        print("   Или запустите: python process_meetings.py --config")
        sys.exit(1)

    # Создаем папки для результатов
    base_dir = Path(__file__).parent / "meetings"
    action_items_dir = base_dir / "action_items"
    action_items_dir.mkdir(parents=True, exist_ok=True)

    # Инициализация Claude клиента
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    print(f"🔍 Поиск встреч по проекту: {project_name}")
    print(f"👥 Участники команды: {', '.join(team_members)}")
    print(f"📊 Лимит встреч: {limit}")
    print()

    # Формируем промпт для Claude с использованием MCP
    prompt = f"""
Используя Fireflies MCP сервер, выполни следующую задачу:

## Задача
Найди и проанализируй встречи по проекту "{project_name}"

## Критерии фильтрации
- Участники команды: {', '.join(team_members)}
- Количество последних встреч для анализа: {limit}
- Фильтруй встречи, где участвовал хотя бы один член команды

## Что нужно извлечь из каждой встречи:

1. **Action Items** - конкретные задачи:
   - Описание задачи
   - Ответственный (если упоминался)
   - Срок (если упоминался)
   - Приоритет (high/medium/low на основе контекста)
   - Контекст из обсуждения

2. **Решения** - принятые на встрече решения

3. **Ключевые темы** - основные темы обсуждения

4. **Следующие шаги** - что нужно сделать дальше

5. **Метрики и цифры** - упомянутые метрики, KPI, числовые данные

## Формат вывода

Верни результат в следующем формате JSON:

```json
{{
  "meetings_analyzed": [
    {{
      "meeting_id": "id встречи",
      "title": "название встречи",
      "date": "дата встречи",
      "participants": ["участник1", "участник2"],
      "action_items": [
        {{
          "task": "описание задачи",
          "assignee": "ответственный или null",
          "deadline": "срок или null",
          "priority": "high/medium/low",
          "context": "краткий контекст"
        }}
      ],
      "decisions": ["решение 1", "решение 2"],
      "key_topics": ["тема 1", "тема 2"],
      "next_steps": ["шаг 1", "шаг 2"],
      "metrics": ["метрика 1", "метрика 2"],
      "summary": "краткое резюме встречи"
    }}
  ],
  "total_meetings": число,
  "total_action_items": число,
  "processed_at": "{datetime.now().isoformat()}"
}}
```

После JSON создай также markdown отчет со всеми открытыми задачами,
сгруппированными по приоритетам (🔴 Высокий, 🟡 Средний, 🟢 Низкий).
"""

    print("🤖 Отправка запроса Claude с использованием MCP...")
    print()

    try:
        # Создаем сообщение с использованием MCP
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=16000,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        # Получаем ответ
        result_text = response.content[0].text

        print("✅ Получен ответ от Claude")
        print()

        # Извлекаем JSON из ответа
        import re
        json_match = re.search(r'```json\n(.*?)\n```', result_text, re.DOTALL)
        if json_match:
            result_json = json.loads(json_match.group(1))

            # Сохраняем JSON результат
            json_output_file = action_items_dir / f"processed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(json_output_file, 'w', encoding='utf-8') as f:
                json.dump(result_json, f, ensure_ascii=False, indent=2)

            print(f"💾 JSON результат сохранен: {json_output_file}")

        # Извлекаем markdown отчет
        md_match = re.search(r'```markdown\n(.*?)\n```', result_text, re.DOTALL)
        if md_match:
            markdown_report = md_match.group(1)
        else:
            # Если нет markdown блока, используем весь текст после JSON
            markdown_report = result_text.split('```json')[-1].split('```')[-1].strip()

        # Сохраняем markdown отчет
        md_output_file = action_items_dir / "tasks_report.md"
        with open(md_output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_report)

        print(f"📄 Markdown отчет сохранен: {md_output_file}")
        print()

        # Выводим статистику
        if json_match:
            result_json = json.loads(json_match.group(1))
            print("=" * 60)
            print("📊 Статистика:")
            print("=" * 60)
            print(f"   • Проанализировано встреч: {result_json.get('total_meetings', 0)}")
            print(f"   • Извлечено action items: {result_json.get('total_action_items', 0)}")
            print(f"   • Дата обработки: {result_json.get('processed_at', 'N/A')}")
            print()

        # Выводим отчет
        print("=" * 60)
        print("📋 Отчет по задачам:")
        print("=" * 60)
        print(markdown_report)

    except Exception as e:
        print(f"❌ Ошибка при обработке: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    print()
    print("=" * 60)
    print("✅ Обработка завершена успешно!")
    print("=" * 60)


def main():
    """Главная функция"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Обработка встреч healthy4u через Fireflies MCP",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:

  # Обработать последние 20 встреч
  python process_meetings_mcp.py

  # Обработать последние 50 встреч
  python process_meetings_mcp.py --limit 50

Требования:
  - Установленный и настроенный Fireflies MCP сервер
  - API ключ Anthropic (ANTHROPIC_API_KEY)
  - API ключ Fireflies (FIREFLIES_API_KEY)
  - Настроенный config.json с team_members
        """
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Количество последних встреч для анализа (по умолчанию: 20)"
    )

    args = parser.parse_args()

    process_meetings_with_mcp(limit=args.limit)


if __name__ == "__main__":
    main()
