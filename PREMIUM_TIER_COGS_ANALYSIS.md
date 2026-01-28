# Premium Tier COGS Analysis: Проверка Unit Economics

**Дата:** 27 января 2026
**Вопрос:** Не вылетим ли из бюджета если Premium пользователи будут использовать unlimited функции?

---

## TL;DR: Есть риск! Рекомендую soft caps даже в Premium

**Ключевые выводы:**
- ✅ Типичный Premium пользователь: COGS $4.35, прибыль $5.64 (56% margin)
- ⚠️ Power user (злоупотребление): COGS $19.70, убыток -$9.71 (-97% margin)
- 🚨 Даже 10% power users могут съесть всю прибыль
- ✅ **Решение:** Generous но не unlimited лимиты для Premium

---

## 1. Детальный расчет COGS по компонентам

### AI Chat/Voice Assistant

**API pricing (OpenAI GPT-4o):**
- Input: $2.50 per 1M tokens
- Output: $10.00 per 1M tokens
- Average chat: ~500 tokens input + 500 tokens output = 1000 tokens total

**Альтернатива (Anthropic Claude Sonnet):**
- Input: $3.00 per 1M tokens
- Output: $15.00 per 1M tokens
- Дороже на 20-50%

**Расчет стоимости:**

| User type | Messages/month | Total tokens | Input cost | Output cost | **Total** |
|-----------|---------------|--------------|------------|-------------|-----------|
| Free (limit) | 50 | 50,000 | $0.01 | $0.05 | **$0.06** |
| Premium typical | 200 | 200,000 | $0.50 | $2.00 | **$2.50** |
| Premium active | 500 | 500,000 | $1.25 | $5.00 | **$6.25** |
| Power user abuse | 1000 | 1,000,000 | $2.50 | $10.00 | **$12.50** |

**Реалистичный сценарий Premium:** $2.50-3.50/month

---

### Food Photo Analysis (AI Vision)

**API pricing (OpenAI Vision):**
- GPT-4o vision: ~$0.01-0.02 per image (зависит от resolution)
- Калорийность + макросы + рекомендации: 1 vision call

**Альтернатива (custom model):**
- Google Vision API: $1.50 per 1000 images = $0.0015/image (дешевле!)
- Но нужна своя модель для nutrition analysis

**Расчет стоимости:**

| User type | Photos/month | Cost per photo | **Total** |
|-----------|--------------|----------------|-----------|
| Free (limit) | 10 | $0.02 | **$0.20** |
| Premium typical (2/day) | 60 | $0.02 | **$1.20** |
| Premium active (5/day) | 150 | $0.02 | **$3.00** |
| Power user (10/day) | 300 | $0.02 | **$6.00** |

**Реалистичный сценарий Premium:** $1.20-2.00/month

---

### Lab Results Analysis (PDF + AI interpretation)

**API pricing:**
- Vision API (PDF parsing): $0.02 per page × avg 2 pages = $0.04
- GPT-4 analysis: ~2000 tokens × $0.0025 = $0.005
- Total per lab: ~$0.05

**Расчет стоимости:**

| User type | Labs/month | Cost per lab | **Total** |
|-----------|------------|--------------|-----------|
| Free (limit) | 5 | $0.05 | **$0.25** |
| Premium typical | 10 | $0.05 | **$0.50** |
| Premium active | 20 | $0.05 | **$1.00** |
| Power user | 30 | $0.05 | **$1.50** |

**Реалистичный сценарий Premium:** $0.50/month

---

### Apple Health / Google Fit Data Sync

**Infrastructure costs:**
- Storage: Minimal (mostly time-series metadata, compressed)
- API calls: Incremental sync, не полный download
- Processing: Batch analytics на backend

**Estimated costs:**
- Storage: $0.05/user/month (50MB avg)
- Processing: $0.05/user/month
- API overhead: $0.05/user/month

**Total:** $0.15/user/month (фиксированно, не зависит от usage)

---

### AI Health Reports & Insights

**Frequency:**
- Weekly summary: 4 reports/month
- Monthly comprehensive: 1 report/month
- Total: 5 AI-generated reports/month

**Cost per report:**
- Data aggregation: minimal
- GPT-4 generation: ~3000 tokens = $0.04
- Total: 5 reports × $0.04 = $0.20/month

**Total:** $0.20/user/month (фиксированно)

---

### Превентивные Risk Alerts

**Модель:**
- Continuous monitoring (background job)
- Alerts only когда thresholds crossed
- Expected: 2-5 alerts/user/month

**Cost:**
- Background analytics: $0.05/user/month
- Alert generation: 3 alerts × $0.02 = $0.06
- **Total:** $0.11/user/month

---

## 2. Общая себестоимость: Scenarios

### Scenario A: Free Tier User (realistic usage)

| Component | Cost |
|-----------|------|
| AI Chat (50 messages) | $0.06 |
| Food photos (10) | $0.20 |
| Lab analysis (5) | $0.25 |
| Health sync | $0.15 |
| Reports | $0.20 |
| Risk alerts | $0.11 |
| **TOTAL COGS** | **$0.97/month** |
| Revenue | $0 |
| **Profit/Loss** | **-$0.97** ❌ |

**Margin:** -100% (ожидаемо, это lead generation)

---

### Scenario B: Premium Tier - Typical User

**Assumed usage:**
- 200 AI messages/month (~7/day)
- 60 food photos/month (~2/day)
- 10 lab analyses/month
- All other features: standard

| Component | Cost |
|-----------|------|
| AI Chat (200 messages) | $2.50 |
| Food photos (60) | $1.20 |
| Lab analysis (10) | $0.50 |
| Health sync | $0.15 |
| Reports | $0.20 |
| Risk alerts | $0.11 |
| **TOTAL COGS** | **$4.66/month** |
| Revenue | $9.99 |
| **Profit** | **$5.33** ✅ |

**Margin:** 53% (отлично!)

---

### Scenario C: Premium Tier - Active User

**Assumed usage:**
- 500 AI messages/month (~16/day)
- 150 food photos/month (~5/day)
- 20 lab analyses/month
- Heavy usage всех функций

| Component | Cost |
|-----------|------|
| AI Chat (500 messages) | $6.25 |
| Food photos (150) | $3.00 |
| Lab analysis (20) | $1.00 |
| Health sync | $0.15 |
| Reports | $0.20 |
| Risk alerts | $0.11 |
| **TOTAL COGS** | **$10.71/month** |
| Revenue | $9.99 |
| **Profit/Loss** | **-$0.72** ⚠️ |

**Margin:** -7% (убыточно!)

---

### Scenario D: Premium Tier - Power User (злоупотребление)

**Assumed usage:**
- 1000 AI messages/month (~33/day) - явно злоупотребление
- 300 food photos/month (~10/day) - аномально
- 30 lab analyses/month
- Максимальное использование

| Component | Cost |
|-----------|------|
| AI Chat (1000 messages) | $12.50 |
| Food photos (300) | $6.00 |
| Lab analysis (30) | $1.50 |
| Health sync | $0.15 |
| Reports | $0.20 |
| Risk alerts | $0.11 |
| **TOTAL COGS** | **$20.46/month** |
| Revenue | $9.99 |
| **Profit/Loss** | **-$10.47** 🚨 |

**Margin:** -105% (катастрофа!)

---

## 3. Distribution Analysis: Что если есть power users?

### Реалистичное распределение Premium пользователей:

| User type | % of Premium | COGS | Profit | Weighted profit |
|-----------|--------------|------|--------|----------------|
| Typical (200 msg, 60 photos) | 70% | $4.66 | $5.33 | $3.73 |
| Active (500 msg, 150 photos) | 25% | $10.71 | -$0.72 | -$0.18 |
| Power users (1000 msg, 300 photos) | 5% | $20.46 | -$10.47 | -$0.52 |
| **WEIGHTED AVERAGE** | **100%** | **$6.82** | **$3.17** | **$3.03** |

**Blended margin:** 30% (приемлемо, но не отлично)

### Что если больше power users?

| Power user % | Weighted COGS | Weighted profit | Margin |
|--------------|---------------|-----------------|--------|
| 0% | $6.02 | $3.97 | 40% ✅ |
| 5% | $6.82 | $3.17 | 32% ✅ |
| 10% | $7.62 | $2.37 | 24% ⚠️ |
| 15% | $8.42 | $1.57 | 16% ⚠️ |
| 20% | $9.22 | $0.77 | 8% 🚨 |

**Вывод:** Уже при 10% power users маржа падает до 24% - это риск!

---

## 4. Риски и митигация

### 🚨 Выявленные риски:

1. **Unlimited AI chat - основной риск**
   - Power user может сгенерировать $12.50/месяц только на chat
   - Это 125% от всей выручки Premium tier!

2. **Unlimited food photos - средний риск**
   - 10 фото/день = $6/месяц
   - Технически возможно, но маловероятно устойчиво

3. **Злоупотребление lab analysis - низкий риск**
   - Сложно делать 30+ анализов в месяц
   - Ограничено реальными медицинскими событиями

4. **Apple Health sync - нет риска**
   - Фиксированная стоимость, не зависит от usage

### ✅ Стратегии митигации:

#### Опция 1: Generous Soft Caps (РЕКОМЕНДУЮ)

**Premium tier с разумными лимитами:**
- AI Chat: **500 messages/month** (16/day - более чем достаточно)
- Food photos: **150/month** (5/day - generous)
- Lab analysis: **20/month**
- Health sync: Unlimited
- Reports: Unlimited
- Risk alerts: Unlimited

**Превышение лимитов:**
- Top-up packs: +100 messages за $2.99
- Top-up packs: +50 photos за $1.99
- Или автоматический upgrade в Premium Pro (если создадим)

**Экономика:**
- Типичный user: uses 200-300 messages, 60-80 photos → вписывается
- Active user: uses 400-500 messages, 100-120 photos → вписывается
- Power user: хочет больше → платит за top-ups ИЛИ честно использует в рамках лимита

**Расчет с лимитами:**
- Max COGS: AI (500 msg) + Photos (150) + Labs (20) = $6.25 + $3 + $1 + $0.66 = **$10.91**
- Revenue: $9.99
- **Worst case loss: -$0.92** (управляемо!)

---

#### Опция 2: Fair Use Policy + Monitoring

**Premium остается "unlimited"**, но с условиями:

> "Premium tier включает unlimited доступ ко всем функциям при fair use. Мы автоматически мониторим аномальное использование и можем связаться с пользователями, чьи паттерны указывают на злоупотребление или коммерческое использование."

**Триггеры для review:**
- >1000 AI messages/month (33/day)
- >300 food photos/month (10/day)
- >30 lab analyses/month

**Действия:**
- Automated email: "Мы заметили необычно высокое использование. Всё ли у вас в порядке?"
- Если продолжается: Throttling (rate limiting)
- Крайний случай: Suspend account с возможностью appeal

**Плюсы:**
- Marketing message: "Truly unlimited"
- Flexibility для легитимных power users
- Минимальные tech changes

**Минусы:**
- Нужен manual review process
- Может создать негативный UX для некоторых
- Сложнее предсказать COGS

---

#### Опция 3: Tiered Premium (Basic + Pro)

**Premium Basic: $9.99/month**
- 500 AI messages/month
- 150 food photos/month
- 20 lab analyses/month
- Все остальное unlimited

**Premium Pro: $19.99/month**
- Unlimited AI messages
- Unlimited food photos
- Unlimited lab analyses
- Priority support
- Advanced analytics

**Экономика:**
- Basic: Max COGS $10.91, margin -9% to 53% → acceptable
- Pro: Max COGS $20.46, margin 2% → borderline acceptable
- Pro users платят 2x → компенсирует риск

**Плюсы:**
- Ясная структура, нет сюрпризов
- Upsell path для heavy users
- Лучшая revenue potential

**Минусы:**
- Усложняет product positioning
- Может запутать пользователей
- Требует A/B testing для оптимизации цен

---

#### Опция 4: Cost Optimization (в параллель с любой опцией)

**Снизить COGS через tech improvements:**

1. **Cheaper AI models где возможно:**
   - GPT-4o-mini: 15x дешевле чем GPT-4o ($0.15 vs $2.50 per 1M input)
   - Use case: Simple questions, routine summaries
   - Keep GPT-4o для: Complex medical analysis, reports

2. **Caching для повторяющихся запросов:**
   - Общие вопросы о wellness ("what is BMI?")
   - Cached responses: 50% discount от OpenAI
   - Потенциальная экономия: 20-30% на AI costs

3. **Batch processing для food photos:**
   - Накапливать photos, process batches
   - Используйте Google Vision ($0.0015/image) + custom model вместо GPT-4 Vision ($0.02/image)
   - Экономия: 92%! ($0.20 → $0.015 за 10 photos)

4. **Smart rate limiting:**
   - 5 messages per minute (prevents spam)
   - 10 food photos per hour (realistic usage pattern)
   - Не блокирует легитимных пользователей, но prevents abuse

**Estimated impact:**
- AI chat: -30% через GPT-4o-mini + caching → $2.50 становится $1.75
- Food photos: -90% через Google Vision + custom model → $1.20 становится $0.12
- **New typical COGS: $2.52** (было $4.66)
- **New margin: 75%** (было 53%) 🚀

---

## 5. Итоговые рекомендации

### 🎯 Recommended approach: Опция 1 + Опция 4

**Premium tier: $9.99/month с generous но не unlimited лимитами**

**Лимиты:**
- ✅ 500 AI messages/month (16/day)
- ✅ 150 food photos/month (5/day)
- ✅ 20 lab analyses/month
- ✅ Unlimited: Health sync, reports, risk alerts, все остальное

**+ Tech optimization:**
- GPT-4o-mini для простых запросов
- Google Vision API для food photos
- Caching для общих вопросов
- Smart rate limiting

**Экономика после оптимизации:**

| User type | COGS (optimized) | Revenue | Profit | Margin |
|-----------|------------------|---------|--------|--------|
| Typical (200 msg, 60 photos) | $2.02 | $9.99 | $7.97 | 80% |
| Active (500 msg, 150 photos) | $4.73 | $9.99 | $5.26 | 53% |
| Max usage (caps hit) | $4.73 | $9.99 | $5.26 | 53% |

**Weighted average (70% typical, 25% active, 5% max):**
- COGS: $2.83/month
- Profit: $7.16/month
- **Margin: 72%** 🎉

---

### Marketing messaging для лимитов:

**НЕ говорите:**
> ❌ "Premium имеет лимиты: 500 сообщений, 150 фото..."

**Говорите:**
> ✅ "Premium включает generous access: до 500 AI консультаций (16 в день!), до 150 анализов фото еды (5 в день!), до 20 лабораторных анализов в месяц, плюс unlimited доступ к health tracking, insights и reports."

**Positioning:**
- 500 messages - это больше чем 99% пользователей когда-либо используют
- Emphasize "generous", не "limited"
- Сравните с Free tier (50 messages) - это 10x больше!

---

### Top-up packs (если нужно больше):

**Premium Add-ons:**
- +100 AI messages: $2.99
- +50 food photo analyses: $1.99
- +10 lab analyses: $1.99

**Или Auto-upgrade сообщение:**
> "Вы использовали 500 AI консультаций в этом месяце! Для unlimited доступа рассмотрите Premium Pro за $19.99/мес, или купите top-up pack +100 сообщений за $2.99."

---

## 6. Updated Premium Tier Description

### Free Tier (Always free)

**AI Health Assistant:**
- ✅ 50 AI messages/month
- ✅ Basic health insights
- ✅ Connection to your doctor

**Food & Nutrition:**
- ✅ 10 food photo analyses/month
- ✅ Basic calorie tracking

**Health Tracking:**
- ✅ Apple Health / Google Fit sync
- ✅ Manual data entry
- ✅ Basic activity tracking

**Lab Results:**
- ✅ 5 lab analyses/month
- ✅ Result storage

**Reports:**
- ✅ Monthly summary reports

---

### Premium Tier: $9.99/month

**AI Health Assistant:**
- ✅ **500 AI messages/month** (16/day - more than you'll ever need!)
- ✅ Advanced AI insights & recommendations
- ✅ Unlimited voice messages
- ✅ Priority response time

**Food & Nutrition:**
- ✅ **150 food photo analyses/month** (5/day - track every meal!)
- ✅ Detailed macro & micronutrient breakdown
- ✅ Personalized meal recommendations
- ✅ Recipe suggestions based on your goals

**Health Tracking:**
- ✅ **Unlimited** comprehensive health tracking
- ✅ **Unlimited** Apple Health / Google Fit sync
- ✅ Advanced analytics & trends
- ✅ Custom health metrics

**Lab Results:**
- ✅ **20 lab analyses/month** with AI interpretation
- ✅ Trend analysis across time
- ✅ Automatic health risk detection

**Reports & Alerts:**
- ✅ **Unlimited** weekly & monthly reports
- ✅ **Unlimited** preventive risk alerts
- ✅ Personalized wellness action plans
- ✅ Progress tracking & goal setting

**Support:**
- ✅ Priority customer support
- ✅ Direct connection to your healthcare provider

**Data & Privacy:**
- ✅ **Unlimited** data export anytime
- ✅ Enhanced privacy controls

**Need more?**
- Top-up packs available if you exceed limits
- Or upgrade to Premium Pro (coming soon) for truly unlimited access

---

## 7. Мониторинг и adjustments

### KPIs для отслеживания (first 3 months):

**Cost metrics:**
- Average COGS per Free user
- Average COGS per Premium user
- % Premium users hitting caps
- Distribution: typical vs active vs power users

**Target benchmarks:**
- Free COGS: <$1/month ✅ ($0.97 current)
- Premium COGS: <$5/month ✅ ($2.83 optimized)
- Premium margin: >60% ✅ (72% optimized)
- % hitting caps: <10% (если больше - лимиты слишком жёсткие)

**Red flags:**
- Premium COGS >$7: Проблема с optimization или abuse
- >20% hitting caps: Лимиты слишком низкие, users frustrated
- Premium churn >15%/month: Возможно из-за лимитов

### When to adjust:

**If avg COGS >$6:**
- Investigate: abuse или проблемы с optimization?
- Implement stricter rate limiting
- Consider lowering caps (400 messages, 100 photos)

**If >15% users hitting caps:**
- Raise caps (600 messages, 200 photos)
- Или introduce Premium Pro tier
- Survey users: are caps frustrating?

**If margin <40%:**
- Либо поднять цену Premium до $12.99
- Либо снизить caps
- Либо агрессивнее optimize tech costs

---

## 8. Comparison с Free tier после оптимизации

| Metric | Free Tier | Premium Tier |
|--------|-----------|--------------|
| AI messages | 50/month | 500/month (10x) |
| Food photos | 10/month | 150/month (15x) |
| Lab analyses | 5/month | 20/month (4x) |
| Features | Basic | Advanced + Unlimited others |
| COGS | $0.97 | $2.83 (optimized avg) |
| Revenue | $0 | $9.99 |
| Profit | -$0.97 | $7.16 |
| Margin | -100% | 72% |

**Free tier ROI:**
- Acquisition tool, leads to Premium conversion
- Target 10-15% conversion → каждые 100 Free users = 10-15 Premium
- Free users cost: 100 × $0.97 = $97/month
- Premium revenue: 15 × $9.99 = $149.85/month
- Premium profit: 15 × $7.16 = $107.40/month
- **Net profit: $107.40 - $97 = $10.40/month** от cohort 100 users
- **Blended margin: 7%** (low но acceptable для growth stage)

---

## Final Answer

### ❓ Исходный вопрос:
> "а мы из бюджета не вылетим по себестоимости если пользователь на премиуме будет анлим использовать прям бесконечно?"

### ✅ Короткий ответ:
**ДА, вылетим!** Unlimited Premium - это риск.

**Решение:** Generous лимиты (500 messages/month, 150 photos/month) + tech optimization → margin 72% ✅

---

### 📊 Ключевые цифры:

| Scenario | COGS | Margin | Risk |
|----------|------|--------|------|
| True unlimited (power users) | $20.46 | -105% | 🚨 Катастрофа |
| Unlimited (typical users) | $4.66 | 53% | ⚠️ Приемлемо, но уязвимо |
| **Soft caps + optimization** | **$2.83** | **72%** | ✅ **Безопасно** |

---

### 🎯 Рекомендация:

**Premium: $9.99/month**
- 500 AI messages/month (не unlimited)
- 150 food photos/month (не unlimited)
- 20 lab analyses/month (не unlimited)
- Unlimited всё остальное (tracking, reports, sync)

**+ Tech optimization:**
- GPT-4o-mini для simple queries
- Google Vision для food photos (-90% cost)
- Caching для common questions

**= Margin 72% при generous UX** 🎉

---

### 📝 Next steps:

1. ✅ Update [PATIENT_APP_TIERS_DETAILED.md](PATIENT_APP_TIERS_DETAILED.md) с новыми лимитами
2. Document tech optimization strategy
3. Implement monitoring dashboard для COGS tracking
4. Set alerts для anomalous usage
5. Prepare top-up pack pricing

**Файлы для обновления:**
- PATIENT_APP_TIERS_DETAILED.md (caps в Premium tier)
- финмодель (COGS assumptions)
- Tech roadmap (optimization priorities)
