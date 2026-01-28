# 🌐 Публикация канбана на GitHub Pages

Инструкция по публикации вашего канбана задач как публичного веб-сайта.

---

## 🚀 Быстрая настройка

### Шаг 1: Создайте GitHub репозиторий

```bash
# Инициализируйте git (если еще не сделали)
git init

# Добавьте все файлы
git add .

# Первый коммит
git commit -m "Initial commit: automated meeting processing system"

# Создайте репозиторий на GitHub через веб-интерфейс
# Затем подключите его:
git remote add origin https://github.com/YOUR_USERNAME/healthy4u.git
git branch -M main
git push -u origin main
```

### Шаг 2: Включите GitHub Pages

1. Откройте ваш репозиторий на GitHub
2. Перейдите в **Settings** (Настройки)
3. В левом меню выберите **Pages**
4. В разделе **Source**:
   - Выберите ветку: `main`
   - Выберите папку: `/docs`
   - Нажмите **Save**

5. Через 1-2 минуты ваш сайт будет доступен по адресу:
   ```
   https://YOUR_USERNAME.github.io/healthy4u/
   ```

### Шаг 3: Обновляйте канбан автоматически

Добавьте в конец файла `auto_process_meetings.py`:

```python
# После успешной обработки обновляем GitHub Pages
if total_tasks_added > 0:
    os.system('./update_github_pages.sh')
```

Теперь канбан будет автоматически обновляться на GitHub Pages каждый час!

---

## 📖 Подробная инструкция

### 1. Подготовка репозитория

#### Создание .gitignore

Создайте файл `.gitignore` чтобы не загружать лишние файлы:

```gitignore
# Python
venv/
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Environment
.env
*.local

# Logs
logs/
*.log

# State files
meetings/.auto_process_state.json
meetings/.monitor_state.json

# macOS
.DS_Store

# IDE
.vscode/
.idea/
```

#### Первый коммит

```bash
# Добавьте .gitignore
git add .gitignore

# Добавьте все остальные файлы
git add .

# Создайте коммит
git commit -m "feat: automated meeting processing with Fireflies + Claude AI

- Auto-process Fireflies transcripts
- Extract action items, decisions, key topics
- Generate interactive kanban board
- Hourly automatic updates
- GitHub Pages integration"
```

### 2. Создание GitHub репозитория

#### Через веб-интерфейс GitHub

1. Перейдите на https://github.com/new
2. Заполните:
   - **Repository name**: `healthy4u`
   - **Description**: `Automated meeting processing and task management for healthy4u project`
   - **Visibility**: Public (для GitHub Pages) или Private (если Pages Pro)
3. Не добавляйте README, .gitignore, license (уже есть локально)
4. Нажмите **Create repository**

#### Подключение репозитория

```bash
git remote add origin https://github.com/YOUR_USERNAME/healthy4u.git
git branch -M main
git push -u origin main
```

### 3. Настройка GitHub Pages

#### Включение Pages

1. Откройте https://github.com/YOUR_USERNAME/healthy4u/settings/pages
2. В **Build and deployment**:
   - Source: `Deploy from a branch`
   - Branch: `main`
   - Folder: `/docs`
3. Нажмите **Save**

#### Проверка

Через 1-2 минуты посетите:
```
https://YOUR_USERNAME.github.io/healthy4u/
```

Вы увидите ваш интерактивный канбан с drag-and-drop!

### 4. Автоматическое обновление

#### Вариант 1: Автокоммит после обработки (рекомендуется)

Отредактируйте `auto_process_meetings.py`, добавьте в конец функции `process_meetings()`:

```python
        # Если были добавлены задачи, обновляем канбан
        if total_tasks_added > 0:
            log(f"Всего добавлено задач: {total_tasks_added}")
            regenerate_kanban()

            # Обновляем GitHub Pages
            import subprocess
            try:
                subprocess.run(['./update_github_pages.sh'], check=True)
                log("GitHub Pages обновлены")
            except Exception as e:
                log(f"Ошибка обновления GitHub Pages: {e}")
        else:
            log("Новых задач не добавлено")
```

#### Вариант 2: Ручное обновление

Когда захотите обновить сайт:

```bash
./update_github_pages.sh
git push
```

#### Вариант 3: GitHub Actions (продвинутый)

Создайте `.github/workflows/update-kanban.yml`:

```yaml
name: Update Kanban

on:
  push:
    paths:
      - 'meetings/action_items/kanban.html'
      - 'docs/index.html'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Copy kanban to docs
        run: |
          cp meetings/action_items/kanban.html docs/index.html
          git config --global user.name 'GitHub Actions'
          git config --global user.email 'actions@github.com'
          git add docs/
          git diff-index --quiet HEAD || git commit -m "Auto-update kanban"
          git push
```

---

## 🔒 Безопасность

### Публичный vs Приватный репозиторий

**Публичный** (бесплатно):
- ✅ GitHub Pages работает из коробки
- ⚠️ Весь код виден всем
- ⚠️ Задачи в канбане видны всем

**Приватный** (требует GitHub Pro):
- ✅ Код скрыт
- ✅ GitHub Pages доступны с Pro
- 💰 $4/месяц

### Защита конфиденциальных данных

1. **Не коммитьте .env** - добавлен в .gitignore
2. **Не коммитьте state файлы** - содержат историю обработки
3. **Не коммитьте логи** - могут содержать чувствительную информацию

### Что безопасно публиковать

- ✅ Код скриптов (auto_process_meetings.py, etc.)
- ✅ Канбан HTML (если задачи не конфиденциальны)
- ✅ README и документация
- ❌ .env с API ключами
- ❌ Логи с персональными данными

---

## 🎨 Кастомизация

### Изменить название сайта

Отредактируйте `docs/index.html`:

```html
<title>Ваше Название - Канбан задач</title>
<h1>🎯 Ваше Название - Канбан задач</h1>
```

### Добавить свой домен

1. Купите домен (например, `tasks.healthy4u.com`)
2. В GitHub Settings → Pages → Custom domain укажите домен
3. Добавьте CNAME запись у регистратора домена:
   ```
   tasks.healthy4u.com → YOUR_USERNAME.github.io
   ```

### Добавить Google Analytics

В `docs/index.html` перед `</head>`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

---

## 🔧 Дополнительно

### Защита паролем

GitHub Pages не поддерживает встроенную аутентификацию. Варианты:

1. **Cloudflare Access** - бесплатная защита сайта
2. **Netlify** - альтернатива GitHub Pages с паролями
3. **Vercel** - еще одна альтернатива

### Кастомный URL для задач

Добавьте в канбан возможность открывать задачи по прямой ссылке:

```javascript
// В kanban.html добавьте:
const urlParams = new URLSearchParams(window.location.search);
const taskId = urlParams.get('task');
if (taskId) {
    const taskCard = document.querySelector(`[data-id="${taskId}"]`);
    if (taskCard) {
        taskCard.scrollIntoView({behavior: 'smooth'});
        taskCard.style.boxShadow = '0 0 20px rgba(255, 215, 0, 0.8)';
    }
}
```

Теперь можно делиться ссылками на конкретные задачи:
```
https://YOUR_USERNAME.github.io/healthy4u/?task=shturm_01
```

---

## 📚 Полезные ссылки

- [GitHub Pages документация](https://docs.github.com/en/pages)
- [Кастомные домены](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)
- [GitHub Actions](https://docs.github.com/en/actions)

---

## 🎯 Готово!

После настройки ваш канбан будет:
- ✅ Автоматически обновляться каждый час
- ✅ Доступен по красивому URL
- ✅ С drag-and-drop интерфейсом
- ✅ С автосохранением в браузере
- ✅ Адаптивным для мобильных устройств

Поделитесь ссылкой с командой и наслаждайтесь автоматизацией! 🚀
