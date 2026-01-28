# Гайд по обновлению финансовой модели Healthy4U

**Дата:** 27 января 2026
**Файл:** Office Open XML spreadsheet.xlsx

---

## 📋 Что нужно обновить

### Критические изменения:
1. ✅ **Pricing:** $100 → $249 (врачи базовая цена)
2. ✅ **COGS:** Добавить реальные данные вместо estimates
3. ✅ **Dual revenue streams:** B2B (врачи) + B2C (пациенты)
4. ✅ **Margins:** Обновить с реальными расчетами
5. ✅ **Projections:** Новые scenarios с актуальными данными

---

## 1️⃣ Лист "Assumptions" (Предположения)

### Секция: Pricing

**СТАРЫЕ ЗНАЧЕНИЯ → НОВЫЕ ЗНАЧЕНИЯ:**

| Параметр | Старое | Новое | Обоснование |
|----------|--------|-------|-------------|
| Doctor Professional price | $100 | $249 | Market research показал - конкуренты $90-1500, мы в middle-premium |
| Early Adopter Tier 1 | $70 | $174 | 30% скидка от $249 |
| Early Adopter Tier 2 | $80 | $199 | 20% скидка от $249 |
| Early Adopter Tier 3 | $90 | $224 | 10% скидка от $249 |
| Patient Premium price | - | $9.99 | NEW: B2C monetization |
| Revenue share to doctors | - | 25% | NEW: $2.50 per Premium patient |

### Секция: COGS (Cost of Goods Sold)

**Добавить новые строки:**

#### Doctor-side COGS:
| Компонент | Per visit | Monthly (340 visits) | Notes |
|-----------|-----------|---------------------|-------|
| Whisper transcription | $0.09 | $30.60 | Per 15-min visit |
| GPT-4o SOAP notes | $0.0155 | $5.27 | AI-generated notes |
| AI clinical consultant | $0.0023 | $0.77 | 30% of visits use |
| Infrastructure (patient data) | - | $0.50 | Fixed cost |
| Analytics & reports | - | $0.05 | Batch processing |
| **TOTAL per typical doctor** | **$0.1055** | **$37.19** | **85% margin** |

#### Patient-side COGS (optimized):
| Компонент | Free user | Premium typical | Premium at limits |
|-----------|-----------|-----------------|-------------------|
| AI chat (GPT-4o-mini + cache) | $0.04 | $1.75 | $4.38 |
| Food photos (Google Vision) | $0.02 | $0.09 | $0.23 |
| Lab analysis | $0.25 | $0.50 | $1.00 |
| Health sync infrastructure | $0.15 | $0.15 | $0.15 |
| Reports & alerts | $0.31 | $0.31 | $0.31 |
| **TOTAL** | **$0.77** | **$2.80** | **$6.07** |

**Weighted average Premium COGS: $2.83** (предполагая 70% typical, 25% active, 5% at limits)

### Секция: Conversion & Adoption

**Добавить:**
- Free to Premium conversion: 10-15% (target: 12%)
- Patient adoption per doctor: 100 patients (conservative)
- Premium patient distribution: 70% typical, 25% active, 5% power users

### Секция: Fair Use Limits

**Добавить новую секцию:**

**Doctor Professional tier includes:**
- 600 AI transcriptions/month (30/day)
- Unlimited AI consultant
- Overage: $0.15/visit above 600

**Patient Premium tier includes:**
- 500 AI messages/month
- 150 food photos/month
- 20 lab analyses/month

---

## 2️⃣ Лист "Unit Economics"

### Обновить таблицу Doctor Unit Economics:

| Metric | Old Value | New Value | Change |
|--------|-----------|-----------|--------|
| **ARPPU (Average)** | $100 | $235 | +135% |
| ARPPU (Early Adopter Tier 1) | $70 | $174 | +149% |
| ARPPU (Early Adopter Tier 2) | $80 | $199 | +149% |
| ARPPU (Professional full price) | $100 | $249 | +149% |
| **COGS per doctor** | Estimate: $20-30 | $37.19 | Validated |
| **Gross Margin** | ~70-80% | 85% | ✅ Improved |
| **Visits included** | Unlimited? | 600/month | Capped |

### Добавить новую таблицу: Patient Unit Economics

| Metric | Value |
|--------|-------|
| **ARPPU** | $9.99 |
| **COGS (typical user)** | $2.80 |
| **Revenue share (25%)** | -$2.50 |
| **Net revenue per Premium patient** | $7.49 |
| **COGS as % of revenue** | 28% |
| **Net margin (after rev share)** | 47% |
| **Gross margin (before rev share)** | 72% |

### Добавить: Blended Unit Economics

| Metric | Value | Calculation |
|--------|-------|-------------|
| **Total MRR (5 doctors + 75 patients)** | $1,757 | ($1,195 doctors + $749 patients - $187 rev share) |
| **Total COGS** | $392 | ($179 doctors + $212 patients) |
| **Gross Profit** | $1,365 | $1,757 - $392 |
| **Blended Margin** | 78% | Before rev share adjustment |
| **Net Margin** | 75% | After rev share |

---

## 3️⃣ Лист "Projections" (Проекции)

### Scenario 1: Conservative (3 врача через 3 месяца)

**Месяц 1:**
| Revenue Source | Count | Price | MRR |
|----------------|-------|-------|-----|
| Doctors (Tier 1) | 1 | $174 | $174 |
| Patients Premium | 15 | $9.99 | $149.85 |
| Revenue share | 15 | -$2.50 | -$37.50 |
| **Total MRR** | | | **$286.35** |

**COGS:**
- Doctors: 1 × $37.19 = $37.19
- Patients: 15 × $2.83 = $42.45
- **Total COGS: $79.64**
- **Profit: $206.71**
- **Margin: 72%**

**Месяц 2:**
| Revenue Source | Count | Price | MRR |
|----------------|-------|-------|-----|
| Doctors | 2 | $174 avg | $348 |
| Patients Premium | 30 | $9.99 | $299.70 |
| Revenue share | 30 | -$2.50 | -$75 |
| **Total MRR** | | | **$572.70** |

**COGS: $159.28 | Profit: $413.42 | Margin: 72%**

**Месяц 3:**
| Revenue Source | Count | Price | MRR |
|----------------|-------|-------|-----|
| Doctors (2×T1, 1×T2) | 3 | Blended | $547 |
| Patients Premium | 45 | $9.99 | $449.55 |
| Revenue share | 45 | -$2.50 | -$112.50 |
| **Total MRR** | | | **$884.05** |

**COGS: $238.92 | Profit: $645.13 | Margin: 73%**

**Q1 Summary:**
- Total Revenue (sum 3 months): $1,743.10
- **ARR (Month 3 annualized): $10,608**
- Average margin: 72%

---

### Scenario 2: Target (5 врачей через 3 месяца)

**Месяц 1:**
| Revenue Source | Count | Price | MRR |
|----------------|-------|-------|-----|
| Doctors (2×Tier 1) | 2 | $174 | $348 |
| Patients Premium | 30 | $9.99 | $299.70 |
| Revenue share | 30 | -$2.50 | -$75 |
| **Total MRR** | | | **$572.70** |

**COGS: $159.28 | Profit: $413.42 | Margin: 72%**

**Месяц 2:**
| Revenue Source | Count | Price | MRR |
|----------------|-------|-------|-----|
| Doctors (3×T1, 1×T2) | 4 | Blended | $721 |
| Patients Premium | 60 | $9.99 | $599.40 |
| Revenue share | 60 | -$2.50 | -$150 |
| **Total MRR** | | | **$1,170.40** |

**COGS: $318.56 | Profit: $851.84 | Margin: 73%**

**Месяц 3:**
| Revenue Source | Count | Price | MRR |
|----------------|-------|-------|-----|
| Doctors (3×T1, 2×T2) | 5 | $920 | $920 |
| Patients Premium | 75 | $9.99 | $749.25 |
| Revenue share | 75 | -$2.50 | -$187.50 |
| **Total MRR** | | | **$1,481.75** |

**COGS: $391.60 | Profit: $1,090.15 | Margin: 74%**

**Q1 Summary:**
- Total Revenue (sum 3 months): $3,224.85
- **ARR (Month 3 annualized): $17,781**
- Average margin: 73%

*(Note: Документ в плане показывает MRR $1,757 для месяца 3 с другим врачебным распределением - использую более консервативную версию выше)*

---

### Scenario 3: Aggressive (8 врачей к месяцу 6)

**Месяц 6:**
| Revenue Source | Count | Price | MRR |
|----------------|-------|-------|-----|
| Doctors (avg $235) | 8 | $235 | $1,880 |
| Patients Premium | 120 | $9.99 | $1,198.80 |
| Revenue share | 120 | -$2.50 | -$300 |
| **Total MRR** | | | **$2,778.80** |

**COGS:**
- Doctors: 8 × $37.19 = $297.52
- Patients: 120 × $2.83 = $339.60
- **Total: $637.12**

**Profit: $2,141.68**
**Margin: 77%**
**ARR: $33,345**

---

## 4️⃣ Лист "Scenarios" (Сценарии)

### Обновить таблицу сравнения:

| Scenario | Month 3 Doctors | Month 3 Patients | MRR Month 3 | ARR | Margin |
|----------|----------------|------------------|-------------|-----|--------|
| **Conservative** | 3 | 45 | $884 | $10,608 | 73% |
| **Target** | 5 | 75 | $1,482 | $17,781 | 74% |
| **Aggressive** | 8 (M6) | 120 (M6) | $2,779 | $33,345 | 77% |

### Sensitivity Analysis: Добавить новую таблицу

**Impact of Premium Conversion Rate:**

| Free→Premium Conversion | Patients (from 500 free) | Patient MRR | Total MRR (5 docs) | ARR |
|------------------------|-------------------------|-------------|-------------------|-----|
| 5% | 25 | $187 | $1,307 | $15,684 |
| 10% | 50 | $374 | $1,494 | $17,928 |
| **15% (target)** | **75** | **$562** | **$1,682** | **$20,184** |
| 20% | 100 | $749 | $1,869 | $22,428 |

**Impact of Doctor Pricing:**

| Base Price | Early Adopter Avg | MRR (5 docs) | ARR | Notes |
|------------|------------------|--------------|-----|-------|
| $199 | $139-179 | $795 | $9,540 | Too low |
| **$249** | **$174-224** | **$995** | **$11,940** | **Current** |
| $299 | $209-269 | $1,195 | $14,340 | Premium positioning |

---

## 5️⃣ Лист "CAC & LTV" (Стоимость привлечения и пожизненная ценность)

### Customer Acquisition Cost (CAC)

**Estimates to track:**

| Customer Type | CAC Estimate | Method | Notes |
|--------------|--------------|--------|-------|
| **Doctor (direct)** | $300-500 | Sales effort | Track actual after first 5 |
| **Doctor (referral)** | $100-200 | Warm intro | From pilot network |
| **Patient** | $0 | Organic | Through doctor platform |

### Lifetime Value (LTV)

**Doctor LTV:**
- Monthly: $235 (blended ARPPU)
- Churn: 5%/month target → 20 months avg lifetime
- **LTV = $235 × 20 = $4,700**
- LTV/CAC target: >6x (with $500 CAC = 9.4x ✅)

**Patient LTV:**
- Monthly net (after rev share): $7.49
- Churn: 10%/month target → 10 months avg lifetime
- **LTV = $7.49 × 10 = $75**
- CAC: $0 (organic) → infinite LTV/CAC ✅

**Combined LTV per doctor:**
- Doctor subscription: $4,700
- 100 patients × 15% Premium × $75 LTV = $1,125
- **Total: $5,825 per doctor relationship**

---

## 6️⃣ Лист "KPIs" (Ключевые показатели)

### Обновить целевые метрики:

| KPI | Month 1 | Month 3 | Month 6 | Target |
|-----|---------|---------|---------|--------|
| **Active Paying Doctors** | 1-2 | 3-5 | 6-8 | 10 by M12 |
| **Premium Patients** | 15-30 | 45-75 | 90-120 | 200 by M12 |
| **Doctor ARPPU** | $174 | $200 | $235 | $249 |
| **Patient ARPPU** | $9.99 | $9.99 | $9.99 | $9.99 |
| **MRR** | $287-573 | $884-1,482 | $2,200-2,779 | $4,500 by M12 |
| **ARR** | $3,444-6,876 | $10,608-17,781 | $26,400-33,345 | $54,000 by M12 |
| **Doctor Gross Margin** | 85% | 85% | 85% | Maintain 80%+ |
| **Patient Gross Margin** | 72% | 72% | 72% | Maintain 70%+ |
| **Blended Margin** | 72-74% | 73-74% | 75-77% | 75%+ |
| **Doctor CAC** | Track | Track | <$400 | <$300 |
| **Doctor LTV/CAC** | TBD | >6x | >8x | >10x |
| **Premium Conversion** | 10-15% | 12-15% | 15%+ | 15-20% |
| **Doctor Churn** | 0% | <5% | <5% | <5% monthly |
| **Patient Churn** | 10-15% | <10% | <8% | <8% monthly |

### Добавить новые метрики:

**Revenue Mix:**
- Month 3: 62% doctors, 38% patients (net)
- Month 6: 68% doctors, 32% patients (net)
- Target: 70% doctors, 30% patients

**COGS Distribution:**
- Month 3: 46% doctors, 54% patients
- Month 6: 47% doctors, 53% patients

---

## 7️⃣ Создать новый лист: "COGS Breakdown"

### Doctor COGS Detail

| Component | Cost Driver | Per Visit | Monthly (340) | Optimization Potential |
|-----------|-------------|-----------|---------------|----------------------|
| Whisper API | $0.006/min × 15min | $0.090 | $30.60 | Low (already cheap) |
| GPT-4o SOAP | 3800 tokens avg | $0.0155 | $5.27 | **High: Use GPT-4o-mini (-60%)** |
| AI Consultant | 30% usage | $0.0023 | $0.77 | Medium: Caching |
| Infrastructure | Fixed | - | $0.50 | Low |
| Analytics | Batch | - | $0.05 | Low |
| **Current Total** | | **$0.1055** | **$37.19** | |
| **Optimized Total** | | **$0.089** | **$30.26** | **-18.6% savings** |

### Patient COGS Detail

| Component | Cost Driver | Free User | Premium Typical | Optimization Potential |
|-----------|-------------|-----------|----------------|----------------------|
| AI Chat | GPT-4o | $0.06 | $2.50 | **High: GPT-4o-mini + cache (-70%)** |
| Food Photos | GPT-4 Vision | $0.20 | $1.20 | **Very High: Google Vision (-92%)** |
| Lab Analysis | GPT-4o | $0.25 | $0.50 | Medium |
| Health Sync | Infrastructure | $0.15 | $0.15 | Low |
| Reports | Batch GPT-4o | $0.31 | $0.31 | Medium: Caching |
| **Current Total** | | **$0.97** | **$4.66** | |
| **Optimized Total** | | **$0.77** | **$2.80** | **-40% savings** |

### Optimization Roadmap

| Phase | Timeframe | Actions | Savings |
|-------|-----------|---------|---------|
| **Phase 1** | Months 1-3 | Google Vision for food, GPT-4o-mini for routine | -30% patient COGS |
| **Phase 2** | Months 4-6 | Aggressive caching, batch optimization | -10% additional |
| **Phase 3** | Months 7-12 | Fine-tuned models, volume discounts | -15% additional |
| **Target** | Month 12 | Blended margin 85%+ | Total -50% COGS |

---

## 8️⃣ Validation Checklist

После обновления проверьте:

### Внутренняя консистентность:
- [ ] MRR × 12 = ARR (проверить все scenarios)
- [ ] (Revenue - COGS) / Revenue = Margin (проверить расчет)
- [ ] Blended ARPPU соответствует weighted average по тирам
- [ ] Total COGS = Sum(Doctor COGS + Patient COGS)
- [ ] Revenue share правильно вычтен из patient revenue

### Реалистичность:
- [ ] Margins 70-85% (реалистично для SaaS)
- [ ] CAC payback <6 months (индустрия: <12 months)
- [ ] LTV/CAC >6x (индустрия: >3x)
- [ ] Churn rates <10% monthly (реалистично для healthcare B2B)
- [ ] Premium conversion 10-15% (реалистично для freemium health apps)

### Investor-ready metrics:
- [ ] ARR >$15K к концу Q1 (показывает traction)
- [ ] Gross margin >70% (показывает scalability)
- [ ] Четкий путь к $100K ARR в течение 12 месяцев
- [ ] Unit economics positive (LTV > CAC)
- [ ] ARPPU растет month-over-month

---

## 9️⃣ CSV Файлы для импорта

Я создам отдельные CSV файлы которые вы сможете скопировать/импортировать:

1. `assumptions_updated.csv` - Обновленные assumptions
2. `projections_conservative.csv` - Conservative scenario по месяцам
3. `projections_target.csv` - Target scenario по месяцам
4. `unit_economics.csv` - Doctor и Patient unit economics
5. `cogs_breakdown.csv` - Детальная разбивка COGS

---

## 🔟 Quick Reference: Key Numbers

**Для быстрого копирования:**

```
PRICING:
- Doctor Professional: $249/month
- Early Adopter T1: $174 (30% off)
- Early Adopter T2: $199 (20% off)
- Early Adopter T3: $224 (10% off)
- Patient Premium: $9.99/month
- Revenue share: 25% ($2.50/patient)

COGS:
- Doctor (typical): $37.19/month
- Patient Premium: $2.83/month
- Patient Free: $0.77/month

MARGINS:
- Doctor: 85%
- Patient (gross): 72%
- Patient (net after rev share): 47%
- Blended: 73-78%

ARR TARGETS:
- Conservative (3 docs, 45 patients): $10,608
- Target (5 docs, 75 patients): $17,781
- Aggressive (8 docs, 120 patients M6): $33,345

CONVERSION:
- Patient Free→Premium: 10-15% (target 12%)
- Patients per doctor: 100 (conservative)

LIMITS:
- Doctor: 600 visits/month included
- Patient Premium: 500 messages, 150 photos, 20 labs/month
```

---

## Файлы для справки

- **[UNIT_ECONOMICS_SUMMARY.md](../UNIT_ECONOMICS_SUMMARY.md)** - Master reference
- **[PREMIUM_TIER_COGS_ANALYSIS.md](../PREMIUM_TIER_COGS_ANALYSIS.md)** - Patient COGS details
- **[DOCTOR_TIER_COGS_ANALYSIS.md](../DOCTOR_TIER_COGS_ANALYSIS.md)** - Doctor COGS details
- **[PRICING_STRATEGY_UPDATED.md](../PRICING_STRATEGY_UPDATED.md)** - Full pricing strategy

---

**После обновления сохраните backup файл с датой в имени!**

Example: `Office Open XML spreadsheet_updated_20260127.xlsx`
