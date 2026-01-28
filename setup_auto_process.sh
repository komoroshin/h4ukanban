#!/bin/bash
# Настройка автоматической обработки встреч

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🔧 Настройка автоматической обработки встреч healthy4u${NC}"
echo ""

# Получаем полный путь к проекту
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
echo -e "📁 Директория проекта: ${PROJECT_DIR}"
echo ""

# Проверяем виртуальное окружение
if [ ! -d "$PROJECT_DIR/venv" ]; then
    echo -e "${RED}❌ Виртуальное окружение не найдено${NC}"
    echo "Создайте его командой: python3 -m venv venv"
    exit 1
fi

# Проверяем .env
if [ ! -f "$PROJECT_DIR/.env" ]; then
    echo -e "${RED}❌ Файл .env не найден${NC}"
    echo "Создайте его и добавьте API ключи"
    exit 1
fi

# Создаем папки для логов
mkdir -p "$PROJECT_DIR/logs"
mkdir -p "$PROJECT_DIR/meetings/action_items"

# Делаем скрипт исполняемым
chmod +x "$PROJECT_DIR/auto_process_meetings.py"

echo -e "${GREEN}✅ Проверки пройдены${NC}"
echo ""

# Создаем скрипт-обертку для cron
WRAPPER_SCRIPT="$PROJECT_DIR/run_auto_process.sh"
cat > "$WRAPPER_SCRIPT" << 'EOF'
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
EOF

chmod +x "$WRAPPER_SCRIPT"

echo -e "${GREEN}✅ Создан скрипт-обертка: ${WRAPPER_SCRIPT}${NC}"
echo ""

# Проверяем тестовый запуск
echo -e "${YELLOW}🧪 Тестовый запуск...${NC}"
"$WRAPPER_SCRIPT"
echo ""

# Проверяем систему
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS - используем launchd
    echo -e "${YELLOW}Обнаружена macOS - настройка через launchd${NC}"
    echo ""

    PLIST_FILE="$HOME/Library/LaunchAgents/com.healthy4u.autoprocess.plist"

    cat > "$PLIST_FILE" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.healthy4u.autoprocess</string>
    <key>ProgramArguments</key>
    <array>
        <string>${WRAPPER_SCRIPT}</string>
    </array>
    <key>StartInterval</key>
    <integer>3600</integer>
    <key>RunAtLoad</key>
    <true/>
    <key>StandardOutPath</key>
    <string>${PROJECT_DIR}/logs/launchd.out.log</string>
    <key>StandardErrorPath</key>
    <string>${PROJECT_DIR}/logs/launchd.err.log</string>
    <key>WorkingDirectory</key>
    <string>${PROJECT_DIR}</string>
</dict>
</plist>
EOF

    # Загружаем задание
    launchctl unload "$PLIST_FILE" 2>/dev/null
    launchctl load "$PLIST_FILE"

    echo -e "${GREEN}✅ Задание launchd создано: ${PLIST_FILE}${NC}"
    echo -e "${GREEN}✅ Автоматическая обработка будет запускаться каждый час${NC}"
    echo ""
    echo "📋 Управление:"
    echo "   • Остановить:  launchctl unload $PLIST_FILE"
    echo "   • Запустить:   launchctl load $PLIST_FILE"
    echo "   • Статус:      launchctl list | grep healthy4u"
    echo ""

elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux - используем cron
    echo -e "${YELLOW}Обнаружен Linux - настройка через cron${NC}"
    echo ""

    # Создаем временный файл для crontab
    TEMP_CRON=$(mktemp)

    # Экспортируем текущий crontab
    crontab -l > "$TEMP_CRON" 2>/dev/null || true

    # Удаляем старую запись если есть
    sed -i '/healthy4u.*auto_process/d' "$TEMP_CRON"

    # Добавляем новую запись (каждый час)
    echo "0 * * * * $WRAPPER_SCRIPT" >> "$TEMP_CRON"

    # Устанавливаем новый crontab
    crontab "$TEMP_CRON"
    rm "$TEMP_CRON"

    echo -e "${GREEN}✅ Задание cron создано${NC}"
    echo -e "${GREEN}✅ Автоматическая обработка будет запускаться каждый час${NC}"
    echo ""
    echo "📋 Управление:"
    echo "   • Просмотр:    crontab -l"
    echo "   • Редактор:    crontab -e"
    echo ""

else
    echo -e "${YELLOW}⚠️  Неизвестная система - настройте запуск вручную${NC}"
    echo ""
    echo "Запускайте скрипт вручную: $WRAPPER_SCRIPT"
    echo ""
fi

echo -e "${GREEN}🎉 Настройка завершена!${NC}"
echo ""
echo "📊 Результаты:"
echo "   • Задачи:       $PROJECT_DIR/meetings/action_items/tasks_clean.json"
echo "   • Канбан:       $PROJECT_DIR/meetings/action_items/kanban.html"
echo "   • Логи:         $PROJECT_DIR/logs/auto_process.log"
echo "   • Состояние:    $PROJECT_DIR/meetings/.auto_process_state.json"
echo ""
echo "💡 Совет: Задачи появятся в канбане через ~1 час после встречи"
