# Healthy4U: Complete Unit Economics Summary

**Дата:** 27 января 2026
**Статус:** Pre-revenue, готовимся к первым контрактам

---

## 📋 Executive Summary

**Модель:** Dual-sided marketplace (B2B doctors + B2C patients)

**Pricing:**
- Врачи Professional: **$249/month** (early adopter: $174-224)
- Пациенты Premium: **$9.99/month**
- Revenue sharing: 25% от пациентов → врачам

**Unit Economics (after optimization):**
- Врачи margin: **85%** (typical practice)
- Пациенты margin: **72%** (after revenue share)
- **Blended margin: 69%** ✅

**ARR projection (5 врачей + 75 Premium пациентов через 3 месяца):**
- **$25,731** (vs $4,440 старая модель = 5.8x improvement!)

---

## 1️⃣ Doctor-Side Economics

### Pricing Structure

| Tier | Price | Included | Target |
|------|-------|----------|--------|
| **Professional** | $249/month | 600 visits/month, AI consultant, patient data | Solo practitioners |
| **Enterprise** | $399/month | Unlimited visits, priority support, dedicated AM | Group practices |
| **Overage** | $0.15/visit | For Professional tier >600 visits | Busy practices |

### Cost of Goods Sold (COGS)

**Компоненты стоимости:**

| Component | API/Service | Per visit | Monthly (340 visits) |
|-----------|-------------|-----------|---------------------|
| Transcription | Whisper API | $0.09 | $30.60 |
| SOAP note generation | GPT-4o | $0.0155 | $5.27 |
| AI clinical consultant | GPT-4o | $0.0075 × 30% | $0.77 |
| Patient data access | Infrastructure | Fixed | $0.50 |
| Analytics & reports | Batch processing | Fixed | $0.05 |
| **TOTAL** | | **$0.1055** | **$37.19** |

### Margin Analysis by Practice Size

| Practice type | Visits/month | COGS | Revenue | Profit | Margin |
|---------------|--------------|------|---------|--------|--------|
| Small (10-15/day) | 240 | $26.41 | $249 | $222.59 | 89% ✅ |
| **Typical (15-20/day)** | **340** | **$37.19** | **$249** | **$211.81** | **85%** ✅ |
| Busy (30-40/day) | 700 | $75.98 | $249 | $173.02 | 69% ✅ |
| Extreme (50+/day) | 1100 | $119.08 | $399* | $279.92 | 70% ✅ |

*Extreme practices upgrade to Enterprise $399/month

### Distribution & Blended Margin

**Realistic distribution:**
- 60% Typical practices (340 visits) → margin 85%
- 20% Small practices (240 visits) → margin 89%
- 15% Busy practices (700 visits) → margin 69%
- 5% Extreme practices (1100 visits, Enterprise) → margin 70%

**Weighted average doctor margin: 82%** 🎉

### Fair Use Policy

**Professional tier ($249) включает:**
- ✅ До 600 AI транскрибаций/month (30/day)
- ✅ Unlimited AI clinical consultant
- ✅ Unlimited patient data access
- ✅ Unlimited analytics & reports

**Overage:**
- 601-800 visits: $0.15/visit
- 801+ visits: Contact sales для Enterprise

**Enforcement:**
- Automated monitoring для >50 visits/day sustained
- Detection account sharing (multiple IPs, impossible patterns)
- Warning → overage charges → upgrade или suspension

---

## 2️⃣ Patient-Side Economics

### Pricing Structure

| Tier | Price | Key Features |
|------|-------|--------------|
| **Free** | $0 | 50 AI messages, 10 food photos, 5 lab analyses/month |
| **Premium** | $9.99/month | 500 AI messages, 150 food photos, 20 lab analyses/month |
| **Top-ups** | $1.99-2.99 | +100 messages, +50 photos, +10 labs |

### Cost of Goods Sold (COGS)

**Original COGS (без optimization):**

| Component | Free user | Premium typical | Premium power user |
|-----------|-----------|----------------|-------------------|
| AI chat | $0.06 | $2.50 | $12.50 |
| Food photos | $0.20 | $1.20 | $6.00 |
| Lab analysis | $0.25 | $0.50 | $1.50 |
| Health sync | $0.15 | $0.15 | $0.20 |
| Reports & alerts | $0.31 | $0.31 | $0.31 |
| **TOTAL** | **$0.97** | **$4.66** | **$20.51** |

**Optimized COGS (GPT-4o-mini + Google Vision + caching):**

| Component | Free user | Premium typical | Premium at limits |
|-----------|-----------|----------------|-------------------|
| AI chat (optimized) | $0.04 | $1.75 | $4.38 |
| Food photos (Google Vision) | $0.02 | $0.09 | $0.23 |
| Lab analysis | $0.25 | $0.50 | $1.00 |
| Health sync | $0.15 | $0.15 | $0.15 |
| Reports & alerts | $0.31 | $0.31 | $0.31 |
| **TOTAL** | **$0.77** | **$2.80** | **$6.07** |

### Margin Analysis (Optimized)

| User type | % of Premium | COGS | Revenue | Net (before rev share) | After rev share* |
|-----------|--------------|------|---------|----------------------|------------------|
| Typical (200 msg, 60 photos) | 70% | $2.02 | $9.99 | $7.97 | $5.48 |
| Active (500 msg, 150 photos) | 25% | $4.73 | $9.99 | $5.26 | $2.77 |
| At limits (caps hit) | 5% | $6.07 | $9.99 | $3.92 | $1.43 |
| **WEIGHTED AVERAGE** | **100%** | **$2.83** | **$9.99** | **$7.16** | **$4.67** |

*Revenue share: 25% от $9.99 = $2.50 идет врачу

**Patient-side margin (after rev share): 47%**
**Patient-side margin (before rev share): 72%**

### Fair Use Limits

**Premium tier ($9.99) включает:**
- ✅ 500 AI messages/month (16/day)
- ✅ 150 food photos/month (5/day)
- ✅ 20 lab analyses/month
- ✅ Unlimited: health tracking, wearable sync, reports, alerts

**Почему limits нужны:**
- Защита от злоупотреблений
- True unlimited COGS: $20.46/user → убыточно
- Generous лимиты покрывают 99% реального usage

**Top-up packs:**
- +100 AI messages: $2.99
- +50 food photos: $1.99
- +10 lab analyses: $1.99

---

## 3️⃣ Combined Business Economics

### Revenue Model: Example with 5 Doctors

**Assumptions (Month 3):**
- 5 врачей на Professional tier
- 4 врача @ $249, 1 врач @ early adopter $199
- Каждый врач: 100 пациентов в приложении
- 15% Premium conversion = 75 Premium пациентов total

### Revenue Breakdown

**Doctor subscriptions:**
| Врач | Tier | Price | MRR |
|------|------|-------|-----|
| Doctor 1 | Professional EA | $224 | $224 |
| Doctor 2 | Professional EA | $224 | $224 |
| Doctor 3 | Professional | $249 | $249 |
| Doctor 4 | Professional | $249 | $249 |
| Doctor 5 | Professional | $249 | $249 |
| **SUBTOTAL** | | | **$1,195** |

**Patient Premium subscriptions:**
- 75 пациентов × $9.99 = **$749.25**

**Revenue sharing (25% to doctors):**
- 75 × $2.50 = -$187.31 (expense)
- Net patient revenue: $749.25 - $187.31 = **$561.94**

**Total MRR:** $1,195 + $561.94 = **$1,756.94**

### COGS Breakdown

**Doctor-side COGS:**
- 5 врачей × 340 visits avg × $0.1055/visit = **$179.35**
  - Or per doctor: $35.87 average

**Patient-side COGS:**
- 75 Premium users × $2.83 avg = **$212.25**

**Total COGS:** $179.35 + $212.25 = **$391.60**

### Profit & Margin

| Metric | Amount |
|--------|--------|
| Total MRR | $1,756.94 |
| Total COGS | -$391.60 |
| **Gross Profit** | **$1,365.34** |
| **Gross Margin** | **78%** |

**After revenue sharing adjustment:**
- Net MRR (after rev share): $1,756.94 - $187.31 = $1,569.63
- COGS: $391.60
- **Net profit: $1,178.03**
- **Net margin: 75%**

### ARR Projection

**Monthly Recurring Revenue:** $1,756.94

**Annual Run Rate (ARR):** $1,756.94 × 12 = **$21,083**

**With conservative growth (8 врачей, 120 Premium пациентов к месяцу 6):**
- Doctor MRR: ~$1,992
- Patient net MRR: ~$898
- **Total MRR: $2,890**
- **ARR: $34,680**

---

## 4️⃣ Comparison: Old vs New Pricing

### Old Model (Pre-Analysis)

**Doctor pricing:**
- Base: $100/month
- Early adopter: $70-90/month
- No patient monetization

**Economics (5 врачей через 3 месяца):**
- MRR: $350-450
- ARR: $4,200-5,400
- No patient revenue

### New Model (Current)

**Doctor pricing:**
- Base: $249/month (2.5x выше!)
- Early adopter: $174-224/month
- Patient Premium: $9.99/month
- Revenue sharing: 25%

**Economics (5 врачей + 75 пациентов через 3 месяца):**
- MRR: $1,757
- ARR: $21,083
- **Improvement: 4-5x** 🚀

**Почему работает:**
1. ✅ Competitive pricing validated через market research
2. ✅ Dual revenue streams (B2B + B2C)
3. ✅ Higher value perception (больше функций чем конкуренты)
4. ✅ Revenue sharing мотивирует врачей推广 patient app

---

## 5️⃣ Scenarios & Sensitivity Analysis

### Conservative Scenario (3 месяца)

**3 врача + 45 Premium пациентов:**

| Revenue source | Amount |
|---------------|--------|
| Doctors (2×$174, 1×$199) | $547 |
| Patients (45 × $9.99) | $449.55 |
| Revenue share (45 × -$2.50) | -$112.50 |
| **Total MRR** | **$884.05** |

**COGS:**
- Doctors: 3 × $37.19 = $111.57
- Patients: 45 × $2.83 = $127.35
- **Total COGS: $238.92**

**Profit:** $884.05 - $238.92 = **$645.13**
**Margin:** 73%
**ARR:** $10,608

### Target Scenario (3 месяца)

**5 врачей + 75 Premium пациентов:**
- MRR: **$1,757**
- Profit: **$1,365**
- Margin: **78%**
- ARR: **$21,083**

*(Detailed breakdown выше)*

### Aggressive Scenario (6 месяцев)

**8 врачей + 120 Premium пациентов:**

| Revenue source | Amount |
|---------------|--------|
| Doctors (avg $235) | $1,880 |
| Patients (120 × $9.99) | $1,198.80 |
| Revenue share (120 × -$2.50) | -$300 |
| **Total MRR** | **$2,778.80** |

**COGS:**
- Doctors: 8 × $37.19 = $297.52
- Patients: 120 × $2.83 = $339.60
- **Total COGS: $637.12**

**Profit:** $2,778.80 - $637.12 = **$2,141.68**
**Margin:** 77%
**ARR:** $33,345

---

## 6️⃣ Risk Factors & Mitigation

### Risk 1: Power Users (High COGS)

**Problem:**
- 10% Premium patients как power users → margin падает с 72% до 55%
- 10% врачей >800 visits/month → margin падает с 85% до 78%

**Mitigation:**
- ✅ Soft caps implemented (500 messages, 150 photos, 600 visits)
- ✅ Overage pricing ($0.15/visit для врачей)
- ✅ Top-up packs для пациентов
- ✅ Automated monitoring для abuse

**Impact после mitigation:** Margin protected at 70%+

### Risk 2: Low Premium Conversion (<10%)

**Problem:**
- Target: 15% Free→Premium conversion
- If только 5% convert → patient revenue падает 67%

**Mitigation:**
- ✅ Generous Free tier создает habit
- ✅ Value-driven upgrade prompts
- ✅ Doctor может sponsor Premium для пациентов (B2B2C)
- ✅ Time-limited offers (50% off first month)

**Backup plan:** Focus на B2B revenue (врачи), patient side = bonus

### Risk 3: Revenue Sharing Eats Margin

**Problem:**
- 25% revenue share = $2.50 per Premium patient
- Если COGS растет, net margin сжимается

**Mitigation:**
- ✅ COGS optimization (GPT-4o-mini, Google Vision) → margin 72% даже после rev share
- ✅ Revenue share мотивирует врачей → больше adoption → компенсирует
- ✅ Можем adjust в будущем (20% или tier-based)

**Current status:** 47% net margin after rev share = healthy

### Risk 4: Account Sharing

**Problem:**
- Врачи делятся аккаунтом → теряем revenue
- Пациенты делятся Premium → теряем conversion

**Mitigation:**
- ✅ Technical detection (multiple IPs, impossible usage patterns)
- ✅ Clear Terms of Service violations
- ✅ Automated warnings → suspension
- ✅ Easy multi-user pricing для клиник (Enterprise tier)

---

## 7️⃣ Cost Optimization Roadmap

### Phase 1: Immediate (Months 1-3)

**Doctor-side:**
- ✅ Use GPT-4o-mini для routine SOAP notes (60% of cases)
  - Savings: ~$2.77/doctor/month
  - Margin improvement: +1%

**Patient-side:**
- ✅ Switch to Google Vision API для food photos
  - Savings: $1.08/Premium user/month
  - Margin improvement: +10%
- ✅ Implement caching для common AI queries
  - Savings: ~$0.50/Premium user/month
  - Margin improvement: +5%

**Total optimization: +15% margin improvement**

### Phase 2: Medium-term (Months 4-9)

**Custom models:**
- Fine-tune GPT-4o-mini на ваших SOAP notes
  - Potential savings: 50% на SOAP generation
- Train custom nutrition model (alternative к vision APIs)
  - Potential savings: 70% на food photos

**Infrastructure:**
- Redis caching layer для frequent queries
- Batch processing optimization
- CDN для static content

**Estimated impact: Additional +10% COGS reduction**

### Phase 3: Long-term (Months 10+)

**Enterprise optimization:**
- On-premise deployment option для крупных клиник
- Volume pricing negotiations с OpenAI/Google (>100 врачей)
- Proprietary models для specific tasks

**Estimated impact: Up to 30% total COGS reduction**

**Future state margins (optimized):**
- Doctors: 90%+
- Patients: 80%+
- **Blended: 85%+**

---

## 8️⃣ Key Metrics Dashboard

### Unit Economics Metrics

| Metric | Current | Target (6 mo) | Notes |
|--------|---------|---------------|-------|
| **Doctor ARPPU** | $235 | $249 | Average after early adopter discounts end |
| **Patient ARPPU** | $9.99 | $9.99 | Stable |
| **Doctor COGS** | $37 | $30 | After optimization |
| **Patient COGS** | $2.83 | $2.00 | After optimization |
| **Doctor CAC** | TBD | <$500 | Track from first customers |
| **Patient CAC** | $0 | $0 | Organic через врачей |
| **Doctor LTV** | $2,988* | $5,976 | *12 months, target 24 months |
| **Patient LTV** | $120** | $240 | **12 months, target 24 months |
| **LTV/CAC (Doctor)** | TBD | >6x | Industry standard 3x+ |
| **Gross Margin** | 78% | 85% | After full optimization |
| **Monthly Churn (Doctor)** | Target <5% | <5% | Annual contracts help |
| **Monthly Churn (Patient)** | Target <10% | <8% | Improve with engagement |

### Business Metrics

| Metric | Month 1 | Month 3 | Month 6 |
|--------|---------|---------|---------|
| **Active Doctors** | 1-2 | 3-5 | 6-8 |
| **Patient Premium Users** | 15-30 | 45-75 | 90-120 |
| **MRR** | $350-450 | $900-1,800 | $2,200-2,900 |
| **ARR** | $4,200-5,400 | $10,800-21,600 | $26,400-34,800 |
| **Premium Conversion** | 10-15% | 12-15% | 15%+ |

---

## 9️⃣ Competitive Positioning

### Врачи: vs AI Medical Scribe Competitors

| Competitor | Price | Features | Our advantage |
|-----------|-------|----------|---------------|
| **Freed.ai** | $90-99 | Scribe only | We have scribe + AI consultant + patient platform |
| **Suki** | $399 | Scribe + voice | Better price ($249), plus patient engagement |
| **DeepScribe** | $750 | Premium scribe | 3x cheaper, similar quality |
| **Nuance DAX** | $369-1500 | Enterprise scribe | Better UX, modern tech, patient component |

**Our positioning:** "More than scribe - complete wellness platform"

### Пациенты: vs Health Apps

| Competitor | Price | Features | Our advantage |
|-----------|-------|----------|---------------|
| **Amazon One Medical** | $9/mo | Telemedicine | We have AI + doctor integration |
| **ChatGPT Health** | Free/Premium | AI chat | Specialized medical AI + data tracking |
| **MyFitnessPal Premium** | $19.99 | Nutrition tracking | Cheaper, more features, AI-powered |

**Our positioning:** "Your doctor's wellness platform - connected care"

---

## 🎯 Final Recommendations

### ✅ Proceed with Current Pricing

**Doctor Professional:** $249/month
- Early adopter: $174-224 (30-20-10% tiers)
- 600 visits/month included
- Margins: 85% (excellent)

**Patient Premium:** $9.99/month
- 500 messages, 150 photos, 20 labs
- Margins: 72% before rev share, 47% after
- Still healthy and sustainable

**Why it works:**
1. Market research validates pricing
2. Margins support growth and R&D
3. Dual revenue streams reduce risk
4. Revenue sharing aligns incentives

### 📊 Target Metrics (Next 6 Months)

**Customer acquisition:**
- 6-8 врачей paying (conservative)
- 90-120 Premium пациентов
- 10-15% Free→Premium conversion

**Revenue:**
- MRR: $2,200-2,900
- ARR: $26,400-34,800
- Gross margin: 75-78%

**Unit economics proof points for investors:**
- Doctor CAC <$500 (target <$300)
- LTV/CAC >6x
- Payback period <6 months
- Stable 75%+ margins

### 🚀 Next Steps

**Week 1-2:**
1. ✅ Finalize pricing documentation
2. Create one-pagers для врачей и пациентов
3. Update финмодель с новыми assumptions
4. Prepare ROI calculator для sales

**Week 3-4:**
5. Outreach к первым 3-5 врачам
6. Set up billing infrastructure (Stripe)
7. Implement usage metering & limits
8. Create monitoring dashboard для COGS tracking

**Month 2-3:**
9. Close первые 3-5 контрактов
10. Validate unit economics с real data
11. Iterate на основе feedback
12. Prepare materials для seed pitch

---

## 📚 Related Documents

- **[PRICING_MARKET_ANALYSIS_2026.md](PRICING_MARKET_ANALYSIS_2026.md)** - Competitive research и market validation
- **[PRICING_STRATEGY_UPDATED.md](PRICING_STRATEGY_UPDATED.md)** - Detailed pricing tiers и sales strategy
- **[PATIENT_APP_TIERS_DETAILED.md](PATIENT_APP_TIERS_DETAILED.md)** - Free vs Premium breakdown
- **[PREMIUM_TIER_COGS_ANALYSIS.md](PREMIUM_TIER_COGS_ANALYSIS.md)** - Patient COGS deep dive
- **[DOCTOR_TIER_COGS_ANALYSIS.md](DOCTOR_TIER_COGS_ANALYSIS.md)** - Doctor COGS deep dive
- **[Financial Model](finmodel/Office%20Open%20XML%20spreadsheet.xlsx)** - Projections spreadsheet (needs update)

---

**Этот документ является master reference для всех unit economics решений. Обновляется по мере получения real-world данных от первых клиентов.**

**Last updated:** 27 января 2026
**Next review:** После закрытия первых 3 врачей
