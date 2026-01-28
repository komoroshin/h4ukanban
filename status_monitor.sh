#!/bin/bash
# Скрипт для проверки статуса мониторинга

# Цвета для вывода
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}📊 Статус мониторинга встреч healthy4u${NC}"
echo "=================================================="
echo ""

PID_FILE="logs/monitor.pid"
STATE_FILE="meetings/.monitor_state.json"

# Проверяем процесс
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")

    if ps -p "$PID" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Мониторинг запущен${NC}"
        echo -e "   PID: ${GREEN}$PID${NC}"

        # Показываем использование ресурсов
        ps -p "$PID" -o %cpu,%mem,etime,cmd | tail -1 | while read cpu mem time cmd; do
            echo -e "   CPU: ${cpu}%"
            echo -e "   Memory: ${mem}%"
            echo -e "   Uptime: ${time}"
        done
    else
        echo -e "${RED}❌ Мониторинг не запущен${NC}"
        echo -e "   (найден старый PID файл: $PID)"
        rm "$PID_FILE"
    fi
else
    echo -e "${RED}❌ Мониторинг не запущен${NC}"
fi

echo ""

# Статистика из state файла
if [ -f "$STATE_FILE" ]; then
    echo -e "${BLUE}📈 Статистика обработки:${NC}"

    # Извлекаем данные из JSON
    TOTAL_MEETINGS=$(cat "$STATE_FILE" | grep -o '"total_meetings_processed": [0-9]*' | grep -o '[0-9]*')
    TOTAL_TASKS=$(cat "$STATE_FILE" | grep -o '"total_action_items": [0-9]*' | grep -o '[0-9]*')
    LAST_CHECK=$(cat "$STATE_FILE" | grep -o '"last_check": "[^"]*"' | cut -d'"' -f4)

    echo -e "   Обработано встреч: ${GREEN}$TOTAL_MEETINGS${NC}"
    echo -e "   Извлечено задач: ${GREEN}$TOTAL_TASKS${NC}"

    if [ ! -z "$LAST_CHECK" ] && [ "$LAST_CHECK" != "null" ]; then
        echo -e "   Последняя проверка: ${LAST_CHECK}"
    fi
else
    echo -e "${YELLOW}⚠️  Файл состояния не найден${NC}"
fi

echo ""

# Последние строки из лога
if [ -f "logs/monitor.log" ]; then
    echo -e "${BLUE}📝 Последние записи лога:${NC}"
    echo "--------------------------------------------------"
    tail -5 logs/monitor.log
    echo "--------------------------------------------------"
    echo ""
    echo -e "Полный лог: ${YELLOW}tail -f logs/monitor.log${NC}"
fi

echo ""
echo "=================================================="
