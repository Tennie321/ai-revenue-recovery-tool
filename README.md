# AI Agency Revenue Recovery & Win-Back Automation Tool

**Turn lost clients into recovered revenue.** The R.E.C.O.V.E.R. framework helps agencies systematically analyze client losses, score recovery potential, and execute personalized win-back campaigns.

## Features

- **8-Dimension Recovery Scoring** — 0-100 score based on loss reason, time elapsed, prior value, relationship strength, and industry factors
- **4-Tier Prioritization** — Hot Lead (70+), Warm Prospect (50-69), Lukewarm (30-49), Cold Re-Engagement (0-29)
- **15 Loss Reasons** — Budget cuts, competitor switch, internal takeover, scope mismatch, leadership change, and more
- **45 Recovery Strategies** — 3 tailored strategies per loss reason
- **3 Win-Back Sequences** — Customized outreach cadences based on time since loss (1-30d, 30-90d, 90d+)
- **15 Industries × 15 Service Lines** — SaaS, Agency, Consulting, E-Commerce, Healthcare, Real Estate, and more
- **Revenue Recovery Projections** — Realistic estimates with probability adjustments
- **3 Ready-to-Use Email Templates** — For recent, mid-term, and long-term re-engagement
- **4 Output Formats** — HTML dashboard, Markdown report, CSV export, JSON data

## Quick Start

```bash
# Interactive mode (with sample data)
python ai_revenue_recovery.py

# Batch mode with your own client data
python ai_revenue_recovery.py --batch your_clients.json

# Version
python ai_revenue_recovery.py --version
```

## Batch Input Format

Create a JSON file with your lost clients:

```json
{
  "clients": [
    {
      "name": "Client Name",
      "industry": "saas",
      "service": "digital_marketing",
      "loss_reason": "budget_cuts",
      "months_since_loss": 3,
      "annual_value": 120000,
      "probability": 0.65,
      "key_contacts": [
        {"name": "Contact Name", "role": "VP Marketing", "strength": "strong"}
      ]
    }
  ],
  "output_formats": ["md", "html", "csv", "json"]
}
```

## Required Industries

saas, agency, consulting, ecommerce, healthcare, realestate, nonprofit, education, finance, legal, manufacturing, hospitality, technology, professional_services, media

## Required Service Lines

digital_marketing, web_development, software_engineering, content_marketing, seo_sem, social_media, brand_strategy, ui_ux_design, video_production, email_marketing, crm_integration, data_analytics, consulting_advisory, lead_generation, customer_success

## Outputs

- `recovery_outputs/` — All generated reports
- `*_report.md` — Full recovery analysis in Markdown
- `*_report.html` — Dark-themed dashboard HTML
- `*_clients.csv` — Client-level data for spreadsheets
- `*_report.json` — Machine-readable complete report

## Pricing

| License | Price | Includes |
|---------|-------|----------|
| Standalone | $14 | Single tool, lifetime updates |
| AI Revenue Toolkit Bundle | $37 | All 20+ tools (36% off) |
| Agency License | $97 | All tools + white-label rights |

## The R.E.C.O.V.E.R. Framework

- **R** — Research & Analyze Loss Root Cause
- **E** — Evaluate Recovery Potential & Score
- **C** — Craft Personalized Win-Back Strategy
- **O** — Orchestrate Multi-Channel Outreach Sequence
- **V** — Verify Engagement & Adjust Approach
- **E** — Execute Re-Engagement with Incentive
- **R** — Retain with Renewed Terms & Monitoring