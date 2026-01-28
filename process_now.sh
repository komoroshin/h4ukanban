#!/bin/bash
# Запуск обработки встреч вручную (без ожидания)

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}🚀 Запуск обработки встреч healthy4u${NC}"
echo ""

# Получаем директорию проекта
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Переходим в директорию
cd "$PROJECT_DIR"

# Активируем виртуальное окружение
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo -e "${GREEN}✅ Виртуальное окружение активировано${NC}"
fi

# Загружаем переменные окружения
if [ -f ".env" ]; then
    set -a
    source .env
    set +a
    echo -e "${GREEN}✅ Переменные окружения загружены${NC}"
fi

echo ""
echo -e "${YELLOW}⚙️  Обработка встреч...${NC}"
echo ""

# Запускаем обработку
python3 auto_process_meetings.py

echo ""
echo -e "${GREEN}✅ Готово!${NC}"
echo ""
echo "📊 Результаты:"
echo "   • Канбан: open meetings/action_items/kanban.html"
echo "   • Задачи: cat meetings/action_items/tasks_clean.json"
echo "   • Логи:   tail -f logs/auto_process.log"
