# Healthy4U Sales Tools

## ROI Calculator - Two Versions

### Overview
Interactive tools for calculating ROI of Healthy4U platform implementation.

**Two versions available:**
1. **HTML Version (NEW!)** - Interactive web page, runs in browser
2. **Python Version** - Generates Excel reports for email/sharing

---

## HTML Version (Recommended for Workshops)

### Quick Start
**Just open the file in your browser:**
```bash
open roi_calculator.html
```
Or double-click the file in Finder.

### Features
✅ **Real-time calculations** - Results update as you type
✅ **Interactive UI** - Beautiful gradient design, easy to use
✅ **Print-ready** - Use browser print (Cmd+P) to create PDF
✅ **No installation** - Works in any modern browser
✅ **Perfect for demos** - Show results live during workshops

### When to Use
- ✅ **During workshops** - Interactive demo in "Use Cases & Quick Wins" section
- ✅ **On-site visits** - Open on laptop, enter clinic's numbers live
- ✅ **Screen sharing** - Show during Zoom/Teams calls
- ✅ **Quick calculations** - Fastest way to get ROI estimate

### How to Use
1. Open `roi_calculator.html` in Chrome, Safari, or Firefox
2. Enter practice details:
   - Number of physicians
   - Physician hourly rate ($)
   - Hours saved per week
   - Select pricing tier (Founder's Circle, Early Adopter, etc.)
   - Select implementation tier (DIY, Guided, Full-Service)
   - Current monthly costs to eliminate (optional)
3. Results update automatically in real-time
4. Print or save as PDF (Cmd+P → Save as PDF)

### Screenshot
```
┌─────────────────────────────────────────┐
│  Healthy4U ROI Calculator               │
├─────────────────────────────────────────┤
│  Practice Information    │   Results    │
│  • Physicians: 3         │ $2,400/mo   │
│  • Hourly Rate: $50      │ savings     │
│  • Hours Saved: 4        │             │
│  • Pricing: Founder's    │ 0.0 months  │
│    Circle ($174/mo)      │ payback     │
│                          │             │
│                          │ $67,608     │
│                          │ 3-year ROI  │
└─────────────────────────────────────────┘
```

---

## Python Version (For Excel Reports)

### Requirements
```bash
pip install openpyxl
```

### Basic Usage

**Simple example (3 physicians, $50/hour, 4 hours saved/week):**
```bash
python roi_calculator.py --physicians 3 --hourly-rate 50 --hours-saved 4
```

This generates `roi_analysis.xlsx` with:
- ROI Summary (executive summary)
- Detailed Analysis (36-month projection)
- Competitor Comparison (Healthy4U vs Freed, Suki, DeepScribe, Custom)

### Advanced Usage

**With custom pricing tier:**
```bash
python roi_calculator.py \
  --physicians 5 \
  --hourly-rate 60 \
  --hours-saved 6 \
  --pricing-tier early_adopter \
  --implementation tier2_guided \
  --current-costs 500 \
  --output clinic_xyz_roi.xlsx
```

### Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--physicians` | ✅ Yes | - | Number of physicians in practice |
| `--hourly-rate` | ✅ Yes | - | Physician hourly rate ($/hour) |
| `--hours-saved` | ✅ Yes | - | Hours saved per physician per week |
| `--pricing-tier` | No | `founders_circle` | `standard`, `founders_circle`, `early_adopter`, `launch_partner` |
| `--implementation` | No | `tier1_diy` | `tier1_diy` (free), `tier2_guided` ($5K), `tier3_full` ($15K) |
| `--current-costs` | No | 0 | Current monthly costs to be eliminated ($/month) |
| `--output` | No | `roi_analysis.xlsx` | Output filename |

### Pricing Tiers

From [PRICING_STRATEGY_UPDATED.md](../../PRICING_STRATEGY_UPDATED.md):

| Tier | Price/Physician | Discount | Use Case |
|------|----------------|----------|----------|
| **Standard** | $249/month | None | Regular customers |
| **Founder's Circle** | $174/month | 30% | First 3 clients |
| **Early Adopter** | $199/month | 20% | Clients 4-10 |
| **Launch Partner** | $224/month | 10% | Clients 11-20 |

### Implementation Tiers

| Tier | Cost | What's Included |
|------|------|-----------------|
| **Tier 1 (DIY)** | FREE | Healthy4U onboarding, email support |
| **Tier 2 (Guided)** | $5,000 | + 2 on-site visits, custom training, weekly check-ins |
| **Tier 3 (Full-Service)** | $10K-20K | + EHR integration, patient onboarding, 90-day support |

### Example Scenarios

**Scenario 1: Small practice (3 physicians, conservative)**
```bash
python roi_calculator.py \
  --physicians 3 \
  --hourly-rate 50 \
  --hours-saved 4 \
  --pricing-tier founders_circle \
  --output small_clinic_roi.xlsx
```

Expected results:
- Monthly savings: $2,400 (3 × 4 hours × 4 weeks × $50)
- Monthly cost: $522 (3 × $174)
- Net monthly savings: $1,878
- Payback: Immediate (no implementation cost)
- 3-year ROI: $67,608

**Scenario 2: Medium practice (10 physicians, aggressive)**
```bash
python roi_calculator.py \
  --physicians 10 \
  --hourly-rate 75 \
  --hours-saved 6 \
  --pricing-tier early_adopter \
  --implementation tier2_guided \
  --current-costs 900 \
  --output medium_clinic_roi.xlsx
```

Expected results:
- Monthly savings: $18,000 (10 × 6 hours × 4 weeks × $75)
- Monthly cost: $1,990 (10 × $199)
- Eliminated costs: $900
- Net monthly savings: $16,910
- Implementation cost: $5,000
- Payback: 0.3 months (10 days!)
- 3-year ROI: $604,760

**Scenario 3: Large practice with existing solution**
```bash
python roi_calculator.py \
  --physicians 20 \
  --hourly-rate 80 \
  --hours-saved 5 \
  --pricing-tier launch_partner \
  --implementation tier3_full \
  --current-costs 2000 \
  --output large_clinic_roi.xlsx
```

### Output Files

**ROI Summary Sheet:**
- Input assumptions
- Key results (monthly savings, costs, payback, 3-year ROI)
- Recommendation (color-coded based on payback period)

**Detailed Analysis Sheet:**
- 36-month projection
- Cumulative savings vs cumulative costs
- Month-by-month payback status

**Competitor Comparison Sheet:**
- Healthy4U vs Freed.ai, Suki, DeepScribe, Custom Build
- Annual costs for your clinic size
- Feature comparison

### Tips for Use

**Which Version to Use When:**

| Scenario | HTML Version | Python Version | Why |
|----------|--------------|----------------|-----|
| **Workshop demo** | ✅ Best | ❌ Too slow | Real-time interactivity, audience can see results instantly |
| **On-site visit** | ✅ Best | ⚠️ OK | No setup needed, just open in browser |
| **Screen sharing** | ✅ Best | ⚠️ OK | More engaging, visual, interactive |
| **Email to clinic** | ⚠️ OK | ✅ Best | Excel file more professional for email attachments |
| **Audit report** | ⚠️ OK | ✅ Best | Excel embeds better in reports, looks more formal |
| **Proposal** | ⚠️ OK | ✅ Best | Multiple tabs (summary, details, comparison) more complete |

**During Workshop:**
- **Use HTML version** during "Use Cases & Quick Wins" session
- Project on screen, enter clinic's numbers live
- Let participants see results update in real-time
- More engaging than static slides

**During Audit:**
- **Use Python version** for final report
- Use actual time-tracking data from shadowing
- Refine hourly rate based on physician compensation
- Include current costs they'll eliminate
- Generate Excel for Recommendations section

**For Proposals:**
- **Use Python version** (more professional for email)
- Create multiple scenarios (conservative, expected, aggressive)
- Show sensitivity analysis
- Include competitor comparison

### Customization

To modify pricing or assumptions, edit constants in `roi_calculator.py`:

```python
# Line 25-30: Pricing tiers
PRICING = {
    'standard': 249,
    'founders_circle': 174,
    # ...
}

# Line 33-37: Implementation costs
IMPLEMENTATION_COSTS = {
    'tier1_diy': 0,
    'tier2_guided': 5000,
    # ...
}
```

### Troubleshooting

**Error: "No module named 'openpyxl'"**
```bash
pip install openpyxl
```

**Error: "Permission denied"**
```bash
chmod +x roi_calculator.py
```

**Want PDF output?**
Use Excel's "Save As PDF" feature or integrate reportlab library (future enhancement).

---

## Future Tools (Coming Soon)

- [ ] **Email Template Generator** - Personalized cold outreach emails
- [ ] **Proposal Builder** - Auto-generate consulting proposals from audit data
- [ ] **Case Study Template** - Structured client success story format
- [ ] **Slide Deck Generator** - Auto-populate workshop slides with client data
