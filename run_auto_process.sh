#!/bin/bash
# Обертка для запуска автоматической обработки встреч

# Получаем директорию проекта
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Переходим в директорию проекта
cd "$PROJECT_DIR"

# Активируем виртуальное окружение
source "$PROJECT_DIR/venv/bin/activate"

# Загружаем переменные окружения
set -a
source "$PROJECT_DIR/.env"
set +a

# Запускаем обработку
python3 "$PROJECT_DIR/auto_process_meetings.py"
