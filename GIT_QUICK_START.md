# 🚀 Быстрый старт с Git и GitHub Pages

## 1. Инициализируйте репозиторий

```bash
# Инициализация
git init
git add .
git commit -m "feat: automated meeting processing system with kanban

- Process Fireflies transcripts automatically
- Extract action items using Claude AI
- Generate interactive drag-and-drop kanban
- Auto-update every hour
- Published on GitHub Pages"

# Создайте репозиторий на GitHub: https://github.com/new
# Название: healthy4u

# Подключите репозиторий
git remote add origin https://github.com/YOUR_USERNAME/healthy4u.git
git branch -M main
git push -u origin main
```

## 2. Включите GitHub Pages

1. Откройте: https://github.com/YOUR_USERNAME/healthy4u/settings/pages
2. Source: `Deploy from a branch`
3. Branch: `main`
4. Folder: `/docs`
5. Save

## 3. Ваш канбан будет доступен

```
https://YOUR_USERNAME.github.io/healthy4u/
```

## 4. Автообновление

Канбан будет автоматически обновляться каждый час!

📖 Подробная инструкция: [GITHUB_PAGES_SETUP.md](GITHUB_PAGES_SETUP.md)
