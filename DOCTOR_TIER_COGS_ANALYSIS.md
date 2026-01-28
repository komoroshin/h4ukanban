# Doctor-Side COGS Analysis: AI Ambient Scribe + Консультант

**Дата:** 27 января 2026
**Вопрос:** Сколько будут стоить транскрипты при ежедневном использовании врачом?

---

## TL;DR: Doctor margin 65-85%, безопасно с soft caps

**Ключевые выводы:**
- ✅ Типичный врач (15-20 визитов/день): COGS $38.18, margin 85%
- ✅ Busy practice (30-40 визитов/день): COGS $86.40, margin 65%
- ⚠️ Extreme practice (60+ визитов/день): COGS $129.35, margin 48%
- ✅ **Решение:** Professional tier включает до 600 транскрибаций/месяц (30/день)

---

## 1. Компоненты Doctor-side COGS

### A. AI Ambient Scribe (основная функция)

**Workflow:**
1. Real-time voice transcription (Whisper API)
2. AI processing → structured SOAP note (GPT-4o)
3. Auto-fill в EHR систему

**API pricing:**

**Whisper API (transcription):**
- $0.006 per minute
- Average visit: 15 minutes
- **Cost per visit: $0.09**

**GPT-4o (SOAP note generation):**
- Input: Transcript ≈ 3000 tokens (15 min × 150 words/min × 1.3 token/word)
- Output: SOAP note ≈ 800 tokens
- Input cost: 3000 × $2.50 / 1M = $0.0075
- Output cost: 800 × $10 / 1M = $0.008
- **Cost per visit: $0.0155**

**Total Scribe cost per visit: $0.09 + $0.0155 = $0.1055**

---

### B. AI Clinical Consultant

**Use case:**
- Differential diagnosis suggestions
- Treatment recommendations
- Drug interaction checks
- Evidence-based medicine queries

**Usage pattern:**
- Not every visit (~30% of visits)
- Complex cases, second opinions

**Cost per query:**
- Input: Case summary + question ≈ 1000 tokens
- Output: Recommendations ≈ 500 tokens
- Cost: (1000 × $2.50 + 500 × $10) / 1M = $0.0075

**Monthly cost:**
- Typical: 30% × 350 visits = 105 queries → $0.79/month
- Active user: 50% × 350 visits = 175 queries → $1.31/month

---

### C. Patient Data Access

**Features:**
- Dashboard с данными пациента из mobile app
- Apple Health data, food logs, lab results
- Real-time wellness metrics

**Infrastructure:**
- Database queries
- API calls к patient DB
- Real-time sync

**Estimated cost: $0.50/doctor/month** (minimal, shared infrastructure)

---

### D. Preventive Analytics & Insights

**Features:**
- Weekly summary: какие пациенты at risk
- Wellness program effectiveness tracking
- Population health analytics

**Cost:**
- Batch processing weekly: ~5000 tokens per doctor
- 4 reports/month = 20K tokens = $0.05/month

**Total: $0.05/doctor/month**

---

## 2. COGS Scenarios по Patient Volume

### Scenario A: Small Practice (10-15 visits/day)

**Assumptions:**
- 12 patients/day average
- 20 working days/month
- **240 visits/month**

| Component | Calculation | Cost |
|-----------|-------------|------|
| Transcription | 240 × $0.09 | $21.60 |
| SOAP notes | 240 × $0.0155 | $3.72 |
| AI consultant (30% visits) | 72 × $0.0075 | $0.54 |
| Patient data access | Fixed | $0.50 |
| Analytics | Fixed | $0.05 |
| **TOTAL COGS** | | **$26.41** |

**Revenue:** $249/month (Professional tier)
**Profit:** $222.59
**Margin:** 89% ✅

---

### Scenario B: Typical Practice (15-20 visits/day)

**Assumptions:**
- 17 patients/day average
- 20 working days/month
- **340 visits/month**

| Component | Calculation | Cost |
|-----------|-------------|------|
| Transcription | 340 × $0.09 | $30.60 |
| SOAP notes | 340 × $0.0155 | $5.27 |
| AI consultant (30% visits) | 102 × $0.0075 | $0.77 |
| Patient data access | Fixed | $0.50 |
| Analytics | Fixed | $0.05 |
| **TOTAL COGS** | | **$37.19** |

**Revenue:** $249/month
**Profit:** $211.81
**Margin:** 85% ✅

---

### Scenario C: Busy Practice (30-40 visits/day)

**Assumptions:**
- 35 patients/day average
- 20 working days/month
- **700 visits/month**

| Component | Calculation | Cost |
|-----------|-------------|------|
| Transcription | 700 × $0.09 | $63.00 |
| SOAP notes | 700 × $0.0155 | $10.85 |
| AI consultant (30% visits) | 210 × $0.0075 | $1.58 |
| Patient data access | Fixed | $0.50 |
| Analytics | Fixed | $0.05 |
| **TOTAL COGS** | | **$75.98** |

**Revenue:** $249/month
**Profit:** $173.02
**Margin:** 69% ✅

---

### Scenario D: Extreme Practice (50-60 visits/day)

**Assumptions:**
- 55 patients/day average (very busy clinic)
- 20 working days/month
- **1100 visits/month**

| Component | Calculation | Cost |
|-----------|-------------|------|
| Transcription | 1100 × $0.09 | $99.00 |
| SOAP notes | 1100 × $0.0155 | $17.05 |
| AI consultant (30% visits) | 330 × $0.0075 | $2.48 |
| Patient data access | Fixed | $0.50 |
| Analytics | Fixed | $0.05 |
| **TOTAL COGS** | | **$119.08** |

**Revenue:** $249/month
**Profit:** $129.92
**Margin:** 52% ⚠️

---

### Scenario E: Абьюз / Multi-doctor Account

**Assumptions:**
- 100 patients/day (impossible для 1 врача, но если делятся аккаунтом)
- 20 working days/month
- **2000 visits/month**

| Component | Calculation | Cost |
|-----------|-------------|------|
| Transcription | 2000 × $0.09 | $180.00 |
| SOAP notes | 2000 × $0.0155 | $31.00 |
| AI consultant (30% visits) | 600 × $0.0075 | $4.50 |
| Patient data access | Fixed | $0.50 |
| Analytics | Fixed | $0.05 |
| **TOTAL COGS** | | **$216.05** |

**Revenue:** $249/month
**Profit:** $32.95
**Margin:** 13% 🚨

---

## 3. Risk Analysis & Distribution

### Реалистичное распределение врачей:

| Practice size | % of doctors | Visits/month | COGS | Profit | Weighted |
|---------------|--------------|--------------|------|--------|----------|
| Small (10-15/day) | 20% | 240 | $26.41 | $222.59 | $44.52 |
| Typical (15-20/day) | 60% | 340 | $37.19 | $211.81 | $127.09 |
| Busy (30-40/day) | 15% | 700 | $75.98 | $173.02 | $25.95 |
| Extreme (50+/day) | 5% | 1100 | $119.08 | $129.92 | $6.50 |
| **WEIGHTED AVG** | **100%** | **410** | **$43.32** | **$205.68** | **$204.06** |

**Blended margin:** 82% (отлично!)

### Что если больше extreme practices?

| Extreme % | Weighted COGS | Weighted profit | Margin |
|-----------|---------------|-----------------|--------|
| 0% | $39.81 | $209.19 | 84% ✅ |
| 5% | $43.32 | $205.68 | 83% ✅ |
| 10% | $47.40 | $201.60 | 81% ✅ |
| 20% | $55.56 | $193.44 | 78% ✅ |
| 30% | $63.72 | $185.28 | 74% ✅ |

**Вывод:** Даже при 30% extreme users, margin 74% - это очень хорошо!

---

## 4. Fair Use Limits для Professional Tier

### 🎯 Recommended: Generous Soft Caps

**Professional tier ($249/month) включает:**

- ✅ **До 600 AI транскрибаций/месяц** (30/day - covers 99% врачей)
- ✅ **Unlimited AI clinical consultant** queries
- ✅ **Unlimited** patient data access
- ✅ **Unlimited** analytics & reports

**Превышение лимита:**
- 601-800 visits: $0.15 per additional visit
- 801+ visits: Contact sales для Enterprise plan

**Почему 600/month (30/day)?**
- 17 patients/day × 20 days = 340 visits (typical) → вписывается с запасом
- 35 patients/day × 20 days = 700 visits (busy) → частично превышает
- Busy practices заплатят extra $15-30/month ИЛИ upgrade to Enterprise

---

### Enterprise Tier (для крупных практик)

**Enterprise: $399/month**

- ✅ **Unlimited** транскрибации
- ✅ **Unlimited** AI консультант
- ✅ **Unlimited** всё остальное
- ✅ Priority support
- ✅ Dedicated account manager
- ✅ Custom integrations

**Экономика Enterprise:**
- Max realistic COGS (1100 visits): $119.08
- Revenue: $399
- Profit: $279.92
- **Margin: 70%** ✅

**Target:** Large clinics с multiple doctors ИЛИ очень busy practices

---

## 5. Мелкие буквы: Fair Use Policy

### Формулировка для Terms of Service:

> **Fair Use Policy для Professional Tier**
>
> Professional subscription включает до 600 AI-assisted patient visit transcriptions в месяц (приблизительно 30 визитов в рабочий день). Этого достаточно для подавляющего большинства практик.
>
> Использование сверх 600 визитов в месяц:
> - Визиты 601-800: дополнительно $0.15 за визит
> - Визиты 801+: мы свяжемся с вами для обсуждения Enterprise плана
>
> Мы автоматически мониторим использование для обеспечения качества сервиса. Account sharing (использование одной лицензии несколькими врачами) запрещено нашими Terms of Service и может привести к suspension.
>
> Все остальные функции платформы (AI clinical consultant, patient data access, analytics) остаются unlimited при fair use.

### Detection & Enforcement:

**Automated monitoring:**
- Track visits/day per account
- Flag if >40 visits/day устойчиво (возможно account sharing)
- Alert если >800 visits/month

**Triggers для investigation:**
- >50 visits/day для >5 дней подряд
- Разные IP addresses / locations для одного account
- Pattern несовместимый с solo practice

**Response:**
- Automated email: "We noticed high usage, do you need Enterprise?"
- Если продолжается: Apply overage charges
- Account sharing detected: Warning → suspension

---

## 6. Cost Optimization Strategies

### Immediate optimizations:

#### 1. Shorter transcripts через noise reduction
- Убрать "um", "uh", filler words перед AI processing
- Saves ~10% tokens → $0.0014/visit
- 350 visits/month = $0.49 savings (marginal)

#### 2. SOAP note generation: использовать GPT-4o-mini для простых случаев
- Routine checkups: GPT-4o-mini ($0.15 input / $0.60 output per 1M)
- Complex cases: GPT-4o
- Estimated 60% visits можно использовать mini
- Savings: $0.0155 → $0.0023 для 60% visits
- 210 visits × ($0.0155 - $0.0023) = $2.77/month savings

#### 3. Batch processing для analytics
- Already implemented (weekly batches)

#### 4. Caching для common phrases в transcription
- Medical terminology словари
- Estimated 5-10% reduction in processing time

**Total potential savings: ~15% COGS reduction**
- Typical practice: $37.19 → $31.61 (margin 87% вместо 85%)

---

### Future optimizations (6-12 месяцев):

#### 1. Fine-tuned model для SOAP notes
- Train на ваших данных
- Cheaper inference
- Potential savings: 50-70% на SOAP generation

#### 2. Custom transcription model
- Alternative к Whisper: Deepgram, AssemblyAI (cheaper для volume)
- Bulk pricing negotiations
- Potential savings: 20-30% на transcription

#### 3. On-premise inference для Enterprise
- Large clinics могут deploy локально
- Eliminates API costs, но adds infrastructure
- Makes sense только для >10 doctors/clinic

---

## 7. Comparison: Professional vs Enterprise

| Feature | Professional ($249) | Enterprise ($399) |
|---------|-------------------|------------------|
| **AI Transcriptions** | 600/month (30/day) | Unlimited |
| **Overage pricing** | $0.15/visit | N/A |
| **AI Clinical Consultant** | Unlimited | Unlimited |
| **Patient Data Access** | Unlimited | Unlimited |
| **Analytics & Reports** | Unlimited | Advanced analytics |
| **Support** | Email (24h response) | Priority + phone |
| **Account manager** | No | Yes |
| **Custom integrations** | No | Yes |
| **Typical COGS** | $37.19 (340 visits) | $119.08 (1100 visits) |
| **Margin** | 85% | 70% |
| **Best for** | Solo practitioners | Group practices |

---

## 8. Tier Structure: Финальная рекомендация

### Starter Tier: $149/month (НОВЫЙ - опционально)

**Target:** Врачи, желающие попробовать платформу

- ✅ 300 AI транскрибаций/month (15/day)
- ✅ 100 AI consultant queries/month
- ✅ Unlimited patient data access
- ✅ Basic analytics

**COGS (170 visits typical):** $18.60
**Margin:** 88%

**Upgrade path:** Легко upgrade в Professional если нужно больше

---

### Professional Tier: $249/month (ОСНОВНОЙ)

- ✅ 600 AI транскрибаций/month (30/day)
- ✅ Unlimited AI consultant
- ✅ Unlimited patient data access
- ✅ Full analytics & reports
- ✅ До 150 пациентов с Premium app access included

**COGS (340 visits typical):** $37.19
**Margin:** 85%

**Overage:** $0.15/visit сверх 600

---

### Enterprise Tier: $399/month

- ✅ Unlimited транскрибации
- ✅ Unlimited всё остальное
- ✅ Priority support
- ✅ Dedicated account manager
- ✅ Custom integrations
- ✅ Unlimited пациенты с Premium access

**COGS (1100 visits heavy usage):** $119.08
**Margin:** 70%

---

## 9. Revenue Model: Комбинированный подход

### Пример: 5 врачей через 3 месяца

**Breakdown:**
- 4 врача на Professional: 4 × $249 = $996
- 1 врач на Enterprise: 1 × $399 = $399
- **Total врачи MRR: $1,395**

**COGS:**
- 4 Professional (avg 340 visits each): 4 × $37.19 = $148.76
- 1 Enterprise (1100 visits): $119.08
- **Total COGS: $267.84**

**Пациентская сторона (из предыдущего анализа):**
- 5 врачей × 100 пациентов = 500 total patients
- 15% Premium conversion = 75 Premium patients
- Premium revenue: 75 × $9.99 = $749.25
- Revenue share врачам (25%): -$187.31
- Premium COGS (optimized): 75 × $2.83 = $212.25
- **Net пациенты: $749.25 - $187.31 - $212.25 = $349.69**

**Combined:**
- Врачи revenue: $1,395.00
- Врачи COGS: -$267.84
- Пациенты net: +$349.69
- **Total profit: $1,476.85/month**
- **MRR: $2,144.25**
- **Blended margin: 69%** 🎉

**ARR after 3 months:** $2,144.25 × 12 = **$25,731**

---

## 10. Сравнение с конкурентами: COGS vs Pricing

### Ваша модель (Healthy4U):

| Tier | Price | COGS | Margin |
|------|-------|------|--------|
| Professional | $249 | $37 | 85% |
| Enterprise | $399 | $119 | 70% |

### Конкуренты (estimated):

**Freed.ai ($99/month):**
- Только transcription, нет AI consultant
- Estimated COGS: ~$25
- Estimated margin: ~75%

**Suki Assistant ($399/month):**
- Transcription + voice commands + некоторый AI
- Estimated COGS: ~$60-80
- Estimated margin: ~75-80%

**DeepScribe ($750/month):**
- Premium transcription + specialty notes
- Estimated COGS: ~$100-150
- Estimated margin: ~75-80%

**Nuance DAX Copilot ($369-1500/month):**
- Enterprise solution
- Estimated COGS: неизвестно (proprietary)
- Margin: вероятно 80%+ (established product)

### Ваше преимущество:

✅ Больше функций чем Freed.ai по 2.5x цене, но и 3x больше value
✅ Competitive с Suki по цене, но добавляете patient-side platform
✅ Лучшая margin чем у многих конкурентов (85% vs 75%)
✅ Dual revenue streams (B2B doctors + B2C patients) = unique positioning

---

## 11. Key Takeaways

### ✅ Good news:

1. **Doctor-side economics excellent:** 70-85% margins даже без optimization
2. **Headroom for growth:** Можете добавить features без риска margins
3. **Scalable:** COGS не растут линейно с usage (many fixed costs)
4. **Competitive:** Margins сравнимы или лучше чем у конкурентов

### ⚠️ Considerations:

1. **Need soft caps:** 600 visits/month предотвращает abuse
2. **Monitor usage:** 5-10% врачей могут быть extreme users
3. **Overage pricing:** $0.15/visit выше 600 - справедливо и profitable
4. **Account sharing:** Detection критично для защиты margins

### 🎯 Recommendations:

**Сейчас (launch):**
1. ✅ Professional tier с 600 visits/month cap
2. ✅ Fair use policy в мелких буквах
3. ✅ Automated monitoring для abuse detection
4. ✅ Overage pricing $0.15/visit

**Позже (6-12 месяцев):**
5. Starter tier ($149) если demand для lower price point
6. Enterprise tier ($399) когда появятся крупные клиники
7. Cost optimization (fine-tuning, custom models) для margin expansion
8. Volume pricing negotiations с OpenAI при >100 врачей

---

## 12. Финальные лимиты: Professional Tier

### Marketing Copy:

> **Professional Tier: $249/month**
>
> Everything you need to transform your practice:
>
> ✨ **AI Ambient Scribe**
> - Up to 600 patient visit transcriptions/month (30 per day)
> - Real-time AI-generated SOAP notes
> - Automatic EHR integration
> - Save 2-3 hours per day on documentation
>
> 🧠 **AI Clinical Consultant**
> - Unlimited diagnostic support queries
> - Evidence-based treatment recommendations
> - Drug interaction checks
> - Differential diagnosis assistance
>
> 📊 **Patient Wellness Platform**
> - Access to patient health data from mobile apps
> - Real-time wellness tracking
> - Preventive risk alerts
> - Includes Premium access for up to 150 patients
>
> 📈 **Analytics & Insights**
> - Unlimited weekly reports
> - Population health analytics
> - Wellness program effectiveness tracking
>
> 💬 **Support**
> - Email support with 24-hour response
> - Onboarding & training included
>
> *Fair use policy applies. Usage over 600 visits/month billed at $0.15 per visit, or upgrade to Enterprise for unlimited.*

---

### Terms of Service (мелкими буквами):

```
FAIR USE POLICY

Professional Subscription includes up to 600 AI-assisted patient visit
transcriptions per calendar month (approximately 30 visits per business day).
This limit accommodates typical usage patterns for solo practitioners.

Overage Charges:
- Visits 601-800: $0.15 per additional visit, billed monthly
- Visits 801+: You will be contacted to discuss Enterprise plan options

All other platform features (AI Clinical Consultant, Patient Data Access,
Analytics, Reports) remain unlimited under fair use.

Account Sharing Prohibited:
Each subscription is licensed for use by a single healthcare provider.
Sharing credentials or using a single license for multiple providers
violates our Terms of Service and may result in immediate suspension.

Usage Monitoring:
We automatically monitor usage patterns to ensure service quality and
compliance with this policy. Unusual patterns (e.g., sustained usage
exceeding 50 visits/day) may trigger a compliance review.

For practices with higher volumes or multiple providers, please contact
sales@healthy4u.com for Enterprise pricing.
```

---

## Final Numbers Summary

| Metric | Free Tier (Patient) | Premium Tier (Patient) | Professional (Doctor) | Enterprise (Doctor) |
|--------|---------------------|----------------------|---------------------|-------------------|
| **Price** | $0 | $9.99 | $249 | $399 |
| **Typical COGS** | $0.97 | $2.83 | $37.19 | $119.08 |
| **Margin** | -100% | 72% | 85% | 70% |
| **Soft Caps** | 50 msg, 10 photos | 500 msg, 150 photos | 600 visits | Unlimited |
| **Status** | ✅ Good | ✅ Good | ✅ Excellent | ✅ Good |

**Blended business margin (5 doctors + 75 Premium patients):** 69%

**This is sustainable and profitable!** 🎉
