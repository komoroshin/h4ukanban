#!/usr/bin/env python3
"""
Главный скрипт для автоматизации обработки транскриптов встреч healthy4u
Синхронизирует встречи из Fireflies и извлекает action items с помощью Claude
"""

import argparse
import sys
from pathlib import Path
from fireflies_client import FirefliesClient
from transcript_processor import TranscriptProcessor


def setup_environment():
    """
    Проверяет наличие необходимых переменных окружения и конфигурации
    """
    import os

    missing_vars = []

    if not os.getenv("FIREFLIES_API_KEY"):
        missing_vars.append("FIREFLIES_API_KEY")

    if not os.getenv("ANTHROPIC_API_KEY"):
        missing_vars.append("ANTHROPIC_API_KEY")

    if missing_vars:
        print("❌ Отсутствуют обязательные переменные окружения:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n📋 Инструкция по настройке:")
        print("\n1. Создайте файл .env в корне проекта:")
        print("   FIREFLIES_API_KEY=ваш_ключ_fireflies")
        print("   ANTHROPIC_API_KEY=ваш_ключ_anthropic")
        print("\n2. Или установите переменные окружения:")
        print("   export FIREFLIES_API_KEY='ваш_ключ'")
        print("   export ANTHROPIC_API_KEY='ваш_ключ'")
        print("\n📖 Где получить ключи:")
        print("   • Fireflies API: https://app.fireflies.ai/integrations/custom/fireflies")
        print("   • Anthropic API: https://console.anthropic.com/")
        return False

    # Проверяем конфигурацию
    config_file = Path(__file__).parent / "config.json"
    if not config_file.exists():
        print(f"⚠️  Файл конфигурации не найден: {config_file}")
        print("Создайте config.json с настройками проекта")
        return False

    return True


def sync_and_process(limit: int = 20, force_reprocess: bool = False):
    """
    Синхронизирует транскрипты и обрабатывает их

    Args:
        limit: Количество последних транскриптов для синхронизации
        force_reprocess: Принудительно обработать даже уже обработанные транскрипты
    """
    print("=" * 60)
    print("🚀 Запуск обработки транскриптов healthy4u")
    print("=" * 60)
    print()

    # Инициализация клиентов
    print("🔧 Инициализация...")
    fireflies = FirefliesClient()
    processor = TranscriptProcessor()

    # Шаг 1: Синхронизация с Fireflies
    print("\n" + "=" * 60)
    print("📥 Шаг 1: Синхронизация транскриптов с Fireflies")
    print("=" * 60)

    saved_files = fireflies.sync_transcripts(limit=limit, filter_by_project=True)

    if not saved_files:
        print("\n⚠️  Не найдено новых транскриптов для обработки")
        print("💡 Проверьте:")
        print("   1. Правильность API ключа Fireflies")
        print("   2. Настройки фильтрации в config.json (team_members)")
        print("   3. Наличие встреч в Fireflies за последнее время")
        return

    # Шаг 2: Обработка транскриптов
    print("\n" + "=" * 60)
    print("🤖 Шаг 2: Извлечение action items с помощью Claude")
    print("=" * 60)

    transcripts_dir = Path(__file__).parent / "meetings" / "transcripts"
    processed_dir = Path(__file__).parent / "meetings" / "processed"

    transcript_files = list(transcripts_dir.glob("*.json"))
    print(f"📂 Найдено транскриптов: {len(transcript_files)}\n")

    processed_count = 0
    for filepath in transcript_files:
        # Проверяем, не обработан ли уже этот файл
        processed_filename = filepath.stem + "_processed.json"
        if (processed_dir / processed_filename).exists() and not force_reprocess:
            print(f"⏭️  Пропускаем (уже обработан): {filepath.name}")
            continue

        try:
            processor.process_transcript_file(str(filepath))
            processed_count += 1
        except Exception as e:
            print(f"❌ Ошибка при обработке {filepath.name}: {e}")

    # Шаг 3: Генерация отчета
    print("\n" + "=" * 60)
    print("📊 Шаг 3: Генерация отчета по задачам")
    print("=" * 60)

    report = processor.generate_tasks_report()
    print(report)

    # Сохраняем отчет
    report_path = Path(__file__).parent / "meetings" / "action_items" / "tasks_report.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)

    # Итоговая статистика
    print("\n" + "=" * 60)
    print("✅ Обработка завершена!")
    print("=" * 60)
    print(f"📊 Статистика:")
    print(f"   • Синхронизировано транскриптов: {len(saved_files)}")
    print(f"   • Обработано новых: {processed_count}")
    print(f"   • Открытых задач: {len(processor.get_open_tasks())}")
    print(f"\n📄 Отчет сохранен: {report_path}")
    print()


def show_tasks():
    """
    Показывает список открытых задач
    """
    processor = TranscriptProcessor()
    report = processor.generate_tasks_report()
    print(report)


def update_config():
    """
    Помогает обновить конфигурацию проекта
    """
    import json

    config_file = Path(__file__).parent / "config.json"

    print("🔧 Настройка конфигурации проекта")
    print("=" * 60)

    # Запрашиваем email участников команды
    print("\n📧 Введите email адреса участников команды healthy4u")
    print("(по одному на строку, пустая строка для завершения):")

    team_members = []
    while True:
        email = input("Email: ").strip()
        if not email:
            break
        team_members.append(email)

    if not team_members:
        print("⚠️  Не указаны участники команды")
        return

    # Загружаем существующую конфигурацию или создаем новую
    if config_file.exists():
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
    else:
        config = {
            "project_name": "healthy4u",
            "keywords": ["healthy4u", "H4U", "здоровье"],
            "fireflies": {
                "api_key_env": "FIREFLIES_API_KEY",
                "sync_limit": 20
            },
            "anthropic": {
                "api_key_env": "ANTHROPIC_API_KEY",
                "model": "claude-sonnet-4-5-20250929"
            }
        }

    # Обновляем список участников
    config["team_members"] = team_members

    # Сохраняем конфигурацию
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Конфигурация сохранена: {config_file}")
    print(f"👥 Участников команды: {len(team_members)}")


def main():
    """Основная функция с обработкой аргументов командной строки"""
    parser = argparse.ArgumentParser(
        description="Автоматизация обработки транскриптов встреч healthy4u",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:

  # Синхронизировать и обработать последние 20 встреч
  python process_meetings.py

  # Синхронизировать последние 50 встреч
  python process_meetings.py --limit 50

  # Показать список открытых задач
  python process_meetings.py --show-tasks

  # Настроить конфигурацию проекта
  python process_meetings.py --config

  # Принудительно переобработать все транскрипты
  python process_meetings.py --force-reprocess
        """
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Количество последних транскриптов для синхронизации (по умолчанию: 20)"
    )

    parser.add_argument(
        "--force-reprocess",
        action="store_true",
        help="Принудительно обработать даже уже обработанные транскрипты"
    )

    parser.add_argument(
        "--show-tasks",
        action="store_true",
        help="Показать список открытых задач без обработки"
    )

    parser.add_argument(
        "--config",
        action="store_true",
        help="Настроить конфигурацию проекта"
    )

    args = parser.parse_args()

    # Обработка команд
    if args.config:
        update_config()
        return

    if args.show_tasks:
        show_tasks()
        return

    # Проверка окружения перед основной работой
    if not setup_environment():
        sys.exit(1)

    # Основная обработка
    sync_and_process(limit=args.limit, force_reprocess=args.force_reprocess)


if __name__ == "__main__":
    main()
