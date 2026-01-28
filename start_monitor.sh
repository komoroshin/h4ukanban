#!/bin/bash
# Скрипт для запуска мониторинга встреч в фоне

# Цвета для вывода
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Запуск мониторинга встреч healthy4u${NC}"
echo ""

# Активируем виртуальное окружение
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo -e "${GREEN}✅ Виртуальное окружение активировано${NC}"
fi

# Загружаем переменные из .env
if [ -f ".env" ]; then
    set -a
    source .env
    set +a
    echo -e "${GREEN}✅ Переменные из .env загружены${NC}"
fi

# Проверка переменных окружения
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo -e "${RED}❌ ANTHROPIC_API_KEY не установлен${NC}"
    echo "Проверьте файл .env"
    exit 1
fi

if [ -z "$FIREFLIES_API_KEY" ]; then
    echo -e "${RED}❌ FIREFLIES_API_KEY не установлен${NC}"
    echo "Проверьте файл .env"
    exit 1
fi

# Создаем папку для логов
mkdir -p logs

# PID файл
PID_FILE="logs/monitor.pid"

# Проверяем, не запущен ли уже процесс
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if ps -p "$OLD_PID" > /dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  Мониторинг уже запущен (PID: $OLD_PID)${NC}"
        echo "Для остановки используйте: ./stop_monitor.sh"
        exit 1
    else
        # Старый PID файл, но процесс не запущен
        rm "$PID_FILE"
    fi
fi

# Интервал проверки (по умолчанию 30 минут)
INTERVAL=${1:-30}

# Запускаем мониторинг в фоне
echo -e "${GREEN}▶️  Запуск мониторинга с интервалом $INTERVAL минут...${NC}"

nohup python3 monitor_meetings.py --interval "$INTERVAL" > logs/monitor.log 2>&1 &

# Сохраняем PID
echo $! > "$PID_FILE"

echo -e "${GREEN}✅ Мониторинг запущен (PID: $(cat $PID_FILE))${NC}"
echo ""
echo "📋 Управление:"
echo "   • Просмотр логов:  tail -f logs/monitor.log"
echo "   • Остановка:       ./stop_monitor.sh"
echo "   • Статус:          ./status_monitor.sh"
echo ""
echo "📁 Результаты сохраняются в: meetings/action_items/"
