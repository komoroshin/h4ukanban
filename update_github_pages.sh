#!/bin/bash
# Автообновление канбана на GitHub Pages

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}🚀 Обновление канбана на GitHub Pages${NC}"
echo ""

# Копируем kanban в docs
cp meetings/action_items/kanban.html docs/index.html

# Обновляем дату в README
DATE=$(date +"%Y-%m-%d %H:%M")
sed -i '' "s/Последнее обновление:.*/Последнее обновление: $DATE/" docs/README.md

echo -e "${GREEN}✅ Файлы обновлены${NC}"
echo ""

# Проверяем, есть ли git репозиторий
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}⚠️  Git репозиторий не инициализирован${NC}"
    echo "Инициализируйте репозиторий командой:"
    echo "  git init"
    echo "  git add ."
    echo "  git commit -m 'Initial commit'"
    exit 0
fi

# Коммитим изменения
echo -e "${YELLOW}📝 Коммит изменений...${NC}"

git add docs/

if git diff-index --quiet HEAD --; then
    echo -e "${YELLOW}Нет изменений для коммита${NC}"
else
    git commit -m "Update kanban: $DATE"
    echo -e "${GREEN}✅ Изменения закоммичены${NC}"
fi

echo ""
echo "📋 Следующие шаги:"
echo "   1. Отправить на GitHub: git push"
echo "   2. Канбан будет доступен на: https://YOUR_USERNAME.github.io/healthy4u/"
