#!/usr/bin/env python3
"""
AI Agency Revenue Recovery & Lost Client Win-Back Automation Tool
R.E.C.O.V.E.R. Framework — Re-engage, Convert, Optimize, Value, Execute, Retain

Zero dependencies (stdlib only). Python 3.8+.
Generates personalized win-back campaigns, re-engagement sequences,
revenue recovery projections, and transition audit reports.

Usage:
  python ai_revenue_recovery.py                  # Interactive mode
  python ai_revenue_recovery.py --industry saas --output md,html,csv
  python ai_revenue_recovery.py --batch sample_clients.json
"""

import argparse
import csv
import json
import os
import random
import sys
import textwrap
from datetime import datetime, timedelta
from pathlib import Path

# ─────────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────────
VERSION = "1.0.0"
DATE = datetime.now().strftime("%Y-%m-%d")

INDUSTRIES = [
    "saas", "agency", "consulting", "ecommerce", "healthcare",
    "realestate", "nonprofit", "education", "finance", "legal",
    "manufacturing", "hospitality", "technology", "professional_services", "media"
]

SERVICE_LINES = [
    "digital_marketing", "web_development", "software_engineering", "content_marketing",
    "seo_sem", "social_media", "brand_strategy", "ui_ux_design", "video_production",
    "email_marketing", "crm_integration", "data_analytics", "consulting_advisory",
    "lead_generation", "customer_success"
]

LOSS_REASONS = [
    "budget_cuts", "switched_competitor", "internal_takeover", "scope_mismatch",
    "poor_roi_perception", "relationship_breakdown", "leadership_change",
    "acquisition_merger", "reduced_priority", "dissatisfaction_quality",
    "pricing_disagreement", "changed_business_model", "pivot_away_from_service",
    "seasonal_pause", "contract_expiry_no_renewal"
]

LOSS_REASON_LABELS = {
    "budget_cuts": "Budget Cuts / Cost Reduction",
    "switched_competitor": "Switched to Competitor",
    "internal_takeover": "Moved Work In-House",
    "scope_mismatch": "Scope / Service Mismatch",
    "poor_roi_perception": "Perceived Poor ROI",
    "relationship_breakdown": "Key Relationship Breakdown",
    "leadership_change": "Client Leadership Change",
    "acquisition_merger": "Acquisition / Merger",
    "reduced_priority": "Reduced Strategic Priority",
    "dissatisfaction_quality": "Dissatisfaction with Quality",
    "pricing_disagreement": "Pricing Disagreement",
    "changed_business_model": "Changed Business Model",
    "pivot_away_from_service": "Pivoted Away from Service Category",
    "seasonal_pause": "Seasonal / Temporary Pause",
    "contract_expiry_no_renewal": "Contract Expiry — No Renewal"
}

RECOVERY_STRATEGIES = {
    "budget_cuts": [
        ("Value-Engineered Retainer", "Propose a scaled-down retainer at 60% of original scope, preserving the highest-ROI services. Include a 90-day reactivation clause."),
        ("Deferred Engagement", "Offer a 6-month deferred engagement with 20% prepay discount. Lock current rates for future restart."),
        ("A La Carte Menu", "Convert to hourly/project basis with pre-paid block pricing. Minimum 10-hour commitment."),
    ],
    "switched_competitor": [
        ("Win-Back Audit", "Perform a free 1-week audit of competitor's work quality. Present 3 concrete improvement opportunities."),
        ("Superior Outcome Guarantee", "Offer 30% first-month discount + money-back guarantee if results don't beat competitor's by 20% in 90 days."),
        ("Technology Edge", "Showcase new AI capabilities/tools since they left. Offer exclusive early access pricing."),
    ],
    "internal_takeover": [
        ("Hybrid Support Retainer", "Offer fractional support retainer (8-16 hrs/month) to supplement their internal team. Knowledge transfer + quality assurance."),
        ("Tool & Systems Package", "Sell them your SOPs, dashboards, and systems for $2,000-$5,000 flat fee. Includes 6 months of support."),
        ("Staff Augmentation", "Offer white-label staff augmentation for overflow work. Their internal team extends with your bench."),
    ],
    "scope_mismatch": [
        ("Redesigned Engagement", "Propose a completely rebuilt SOW based on current needs. Include discovery workshop at no cost."),
        ("Consulting-Only Option", "Shift from execution to advisory. Monthly strategy sessions + quarterly workshops ($2K-$5K/month)."),
        ("Referral to Specialist", "Refer to a specialist partner (you get referral fee). Keep relationship warm for future re-engagement."),
    ],
    "poor_roi_perception": [
        ("ROI Retrospective", "Conduct a free comprehensive ROI analysis of past work. Use hard metrics, benchmarks, and industry comparisons."),
        ("Outcome-Based Pricing", "Propose new engagement with outcome-based pricing. Fees tied to KPIs they care about most."),
        ("Case Study Co-Creation", "Offer to co-create a public case study of their past results. Positions them as industry leader, demonstrates value."),
    ],
    "relationship_breakdown": [
        ("Fresh Start Meeting", "New account team introduction. 30-minute 'clean slate' conversation. Acknowledge past issues, present new approach."),
        ("Executive Alignment", "Schedule quarterly executive alignment meetings between leadership teams. Strategic partnership, not vendor relationship."),
        ("Service Recovery Package", "Offer 2 months of enhanced service at no extra cost. Dedicated account manager + weekly check-ins."),
    ],
    "leadership_change": [
        ("Executive Briefing", "Prepare a 30-minute executive briefing for new leadership. Past wins, current industry trends, 3 quick-win opportunities."),
        ("Leadership Onboarding", "Offer structured leadership onboarding session: strategy overview, current initiatives, recommended next steps."),
        ("New Vision Alignment", "Map your capabilities to new leadership's stated priorities. Present as strategic enabler, not vendor."),
    ],
    "acquisition_merger": [
        ("Integration Assessment", "Offer free assessment of how your services fit the new combined entity. Identify quick wins and cost synergies."),
        ("Consolidation Pitch", "Present bundled service offering that reduces vendor count. Volume discount for combined entity."),
        ("New Leadership Briefing", "Executive presentation to new leadership team. Highlight past value, future potential, and M&A integration experience."),
    ],
    "reduced_priority": [
        ("Minimum Viable Engagement", "Propose 4-hour/month 'hotline' retainer. Keep relationship alive, jump on opportunities quickly."),
        ("Quarterly Pulse Check", "Schedule quarterly strategy sessions ($750/session). Stay top of mind, ready to scale when priority returns."),
        ("Thought Leadership Access", "Invite to exclusive events, research reports, and strategy days. Maintain relationship without active engagement."),
    ],
    "dissatisfaction_quality": [
        ("Quality Improvement Plan", "Present a written plan addressing each quality concern. Offer 60-day quality guarantee with compensation for missed SLAs."),
        ("Team Refresh", "Propose new team composition with senior-heavy staffing. Free senior oversight for first 90 days."),
        ("Process Transparency", "Open access to all project management tools, daily standup recordings, and quality dashboards. Full transparency rebuilds trust."),
    ],
    "pricing_disagreement": [
        ("Value-Based Pricing", "Redesign pricing around outcomes delivered rather than hours. Clients pay for results, not time."),
        ("Flexible Payment Terms", "Offer net-60 payment terms, monthly billing, or milestone-based payments. Reduce cash flow friction."),
        ("Tiered Retainer Options", "Present 3 retainer tiers (Essential $X, Growth $2X, Premier $3X). Let them self-select. Middle option usually wins."),
    ],
    "changed_business_model": [
        ("Model Alignment Workshop", "Free 1-day workshop mapping how your services adapt to their new business model. Deliver within 2 weeks."),
        ("Pilot Engagement", "Propose 60-day pilot at 50% of projected cost. Prove your model works in their new context."),
        ("Advisory Transition", "Offer monthly advisory during their transition period. Help them navigate change, position for re-engagement post-transition."),
    ],
    "pivot_away_from_service": [
        ("Capability Expansion", "Showcase new service lines that align with their pivot. 30-minute capability demo."),
        ("Strategic Referral", "Refer them to a specialist in their new focus area. Keep relationship warm through quarterly check-ins."),
        ("Reverse Referral Deal", "Offer to send them 3-5 qualified leads in their new space if they send you referrals in your core areas."),
    ],
    "seasonal_pause": [
        ("Pre-Season Planning", "Offer 50% off a pre-season strategy session to plan their next campaign. First month back at locked-in rates."),
        ("Retainer Hold", "Hold their retainer slot open with a $500/month 'hold fee' (credited toward first month back full-time)."),
        ("Seasonal Intelligence", "During pause, send monthly industry intelligence reports. Stay valuable and visible without active engagement."),
    ],
    "contract_expiry_no_renewal": [
        ("Contract Refresh", "Propose updated contract with modern terms, flexible commitments, and new service options. 10% loyalty discount."),
        ("Multi-Year Incentive", "Offer 15% discount for 2-year commitment + quarterly business reviews. Lock in partnership."),
        ("Alumni Program", "Enroll them in your client alumni program. Access to resources, events, and rapid re-engagement when ready."),
    ],
}

WIN_BACK_SEQUENCES = {
    "lost_1_30_days": [
        ("Day 3", "Thank-you note + feedback survey", "Professional gratitude, no sales pitch. Learn why they left."),
        ("Day 14", "Share relevant industry insight/article", "Position yourself as helpful resource, not salesperson."),
        ("Day 30", "30-day check-in + 'how's it going?'", "Casual reach out, no agenda. Demonstrate genuine care."),
    ],
    "lost_30_90_days": [
        ("Day 45", "New case study / success story from similar client", "Show you're delivering results for peers."),
        ("Day 60", "Invite to exclusive webinar/event", "Bring them into your community, rebuild connection."),
        ("Day 90", "90-day re-engagement opportunity offer", "Time-sensitive offer to restart at preferred terms."),
    ],
    "lost_90_plus_days": [
        ("Month 4", "New service announcement relevant to their business", "Something new to talk about — break the silence."),
        ("Month 5", "Personalized value assessment", "Show what they've missed in quantifiable terms."),
        ("Month 6", '"We miss you" — exclusive comeback offer', "Final outreach with best possible terms. 30% off first 3 months."),
    ],
}

CLIENT_TEMPLATES = [
    {"name": "TechFlow SaaS", "industry": "saas", "service": "digital_marketing", "reason": "budget_cuts",
     "months_since_loss": 2, "prior_annual_value": 120000, "recovery_probability": 0.65,
     "key_contacts": [{"name": "Sarah Chen", "role": "VP Marketing", "strength": "strong"},
                      {"name": "Mike Torres", "role": "CEO", "strength": "moderate"}]},
    {"name": "Premier Consulting Group", "industry": "consulting", "service": "brand_strategy", "reason": "leadership_change",
     "months_since_loss": 4, "prior_annual_value": 85000, "recovery_probability": 0.45,
     "key_contacts": [{"name": "James Wilson", "role": "New CEO", "strength": "none"}]},
    {"name": "GreenLeaf Nonprofit", "industry": "nonprofit", "service": "content_marketing", "reason": "reduced_priority",
     "months_since_loss": 8, "prior_annual_value": 36000, "recovery_probability": 0.30,
     "key_contacts": [{"name": "Ana Rodriguez", "role": "Development Director", "strength": "moderate"}]},
    {"name": "Coastal Realty Partners", "industry": "realestate", "service": "social_media", "reason": "switched_competitor",
     "months_since_loss": 3, "prior_annual_value": 48000, "recovery_probability": 0.55,
     "key_contacts": [{"name": "David Kim", "role": "Principal Broker", "strength": "moderate"}]},
    {"name": "MedCore Healthcare", "industry": "healthcare", "service": "ui_ux_design", "reason": "contract_expiry_no_renewal",
     "months_since_loss": 1, "prior_annual_value": 96000, "recovery_probability": 0.75,
     "key_contacts": [{"name": "Dr. Lisa Park", "role": "CMO", "strength": "strong"},
                      {"name": "Tom Baker", "role": "IT Director", "strength": "strong"}]},
    {"name": "BrightPath Education", "industry": "education", "service": "web_development", "reason": "scope_mismatch",
     "months_since_loss": 6, "prior_annual_value": 55000, "recovery_probability": 0.40,
     "key_contacts": [{"name": "Rachel Adams", "role": "Dean of Operations", "strength": "moderate"}]},
    {"name": "Nova Financial", "industry": "finance", "service": "crm_integration", "reason": "acquisition_merger",
     "months_since_loss": 5, "prior_annual_value": 150000, "recovery_probability": 0.35,
     "key_contacts": [{"name": "Kevin Wright", "role": "New COO", "strength": "none"}]},
    {"name": "StyleLab E-Commerce", "industry": "ecommerce", "service": "email_marketing", "reason": "dissatisfaction_quality",
     "months_since_loss": 2, "prior_annual_value": 72000, "recovery_probability": 0.60,
     "key_contacts": [{"name": "Maya Patel", "role": "Head of E-Commerce", "strength": "weak"}]},
]

REVENUE_RECOVERY_FRAMEWORK = """
╔══════════════════════════════════════════════════════════╗
║           R.E.C.O.V.E.R. FRAMEWORK                      ║
╠══════════════════════════════════════════════════════════╣
║ R — Research & Analyze Loss Root Cause                  ║
║ E — Evaluate Recovery Potential & Score                 ║
║ C — Craft Personalized Win-Back Strategy                ║
║ O — Orchestrate Multi-Channel Outreach Sequence         ║
║ V — Verify Engagement & Adjust Approach                 ║
║ E — Execute Re-Engagement with Incentive                ║
║ R — Retain with Renewed Terms & Monitoring              ║
╚══════════════════════════════════════════════════════════╝
"""

# ─────────────────────────────────────────────────────────
# Core Classes
# ─────────────────────────────────────────────────────────

class ClientLost:
    """Represents a lost client with recovery intelligence."""

    def __init__(self, name, industry, service, reason, months_since_loss,
                 prior_annual_value, recovery_probability=0.5, key_contacts=None):
        self.name = name
        self.industry = industry
        self.service = service
        self.reason = reason
        self.months_since_loss = months_since_loss
        self.prior_annual_value = prior_annual_value
        self.recovery_probability = recovery_probability
        self.key_contacts = key_contacts or []

    @property
    def recovery_score(self):
        """0-100 score based on multiple factors."""
        base = self.recovery_probability * 100
        time_penalty = min(self.months_since_loss * 3, 30)
        value_bonus = min(self.prior_annual_value / 5000, 15)
        contact_bonus = sum(
            10 if c["strength"] == "strong" else 5 if c["strength"] == "moderate" else 0
            for c in self.key_contacts
        )
        return max(0, min(100, round(base - time_penalty + value_bonus + contact_bonus, 1)))

    @property
    def recovery_tier(self):
        score = self.recovery_score
        if score >= 70:
            return "Hot Lead"
        elif score >= 50:
            return "Warm Prospect"
        elif score >= 30:
            return "Lukewarm"
        else:
            return "Cold Re-Engagement"

    def get_recovery_strategies(self):
        return RECOVERY_STRATEGIES.get(self.reason, RECOVERY_STRATEGIES["contract_expiry_no_renewal"])

    def get_win_back_sequence(self):
        if self.months_since_loss <= 1:
            return WIN_BACK_SEQUENCES["lost_1_30_days"]
        elif self.months_since_loss <= 3:
            return WIN_BACK_SEQUENCES["lost_30_90_days"]
        else:
            return WIN_BACK_SEQUENCES["lost_90_plus_days"]

    def estimated_recovery_value(self, recovery_rate=0.4):
        """Estimated annual value if recovered, with realism factor."""
        if self.recovery_probability < 0.2:
            return 0
        likely_amount = self.prior_annual_value * recovery_rate * random.uniform(0.8, 1.2)
        return round(likely_amount, -2)

    def to_dict(self):
        return {
            "name": self.name,
            "industry": self.industry,
            "service": self.service,
            "reason": self.reason,
            "reason_label": LOSS_REASON_LABELS.get(self.reason, self.reason),
            "months_since_loss": self.months_since_loss,
            "prior_annual_value": self.prior_annual_value,
            "recovery_probability": self.recovery_probability,
            "recovery_score": self.recovery_score,
            "recovery_tier": self.recovery_tier,
            "key_contacts": self.key_contacts,
            "estimated_recovery_value": self.estimated_recovery_value(),
        }


class RecoveryProgram:
    """Generates loss analysis, recovery plans, and reports."""

    def __init__(self, clients):
        self.clients = clients

    def aggregate_metrics(self):
        total_lost = sum(c.prior_annual_value for c in self.clients)
        total_recoverable = sum(c.estimated_recovery_value() for c in self.clients)
        avg_score = sum(c.recovery_score for c in self.clients) / max(len(self.clients), 1)
        return {
            "total_clients_lost": len(self.clients),
            "total_annual_value_lost": total_lost,
            "total_recoverable_annual_value": total_recoverable,
            "recovery_rate_pct": round(total_recoverable / total_lost * 100, 1) if total_lost else 0,
            "average_recovery_score": round(avg_score, 1),
            "hot_leads": sum(1 for c in self.clients if c.recovery_tier == "Hot Lead"),
            "warm_prospects": sum(1 for c in self.clients if c.recovery_tier == "Warm Prospect"),
            "lukewarm": sum(1 for c in self.clients if c.recovery_tier == "Lukewarm"),
            "cold": sum(1 for c in self.clients if c.recovery_tier == "Cold Re-Engagement"),
        }

    def get_loss_reason_breakdown(self):
        counts = {}
        for c in self.clients:
            reason = c.reason
            counts[reason] = counts.get(reason, 0) + 1
        return [
            {"reason": LOSS_REASON_LABELS.get(r, r), "count": v,
             "pct": round(v / len(self.clients) * 100, 1)}
            for r, v in sorted(counts.items(), key=lambda x: -x[1])
        ]

    def generate_recovery_report_markdown(self):
        metrics = self.aggregate_metrics()
        lines = [
            f"# Revenue Recovery & Win-Back Analysis Report",
            f"**Generated:** {DATE}",
            f"**Framework:** R.E.C.O.V.E.R. — Research, Evaluate, Craft, Orchestrate, Verify, Execute, Retain",
            "",
            "---",
            "",
            "## Executive Summary",
            "",
            f"| Metric | Value |",
            f"|---|---|",
            f"| Lost Clients Analyzed | {metrics['total_clients_lost']} |",
            f"| Total Annual Value Lost | ${metrics['total_annual_value_lost']:,} |",
            f"| Estimated Recoverable Value | ${metrics['total_recoverable_annual_value']:,} |",
            f"| Recovery Rate | {metrics['recovery_rate_pct']}% |",
            f"| Average Recovery Score | {metrics['average_recovery_score']}/100 |",
            "",
            "### Lead Pipeline",
            "",
            f"| Tier | Count | Priority |",
            f"|---|---|---|",
            f"| 🔥 Hot Lead (70-100) | {metrics['hot_leads']} | Immediate outreach |",
            f"| 🔶 Warm Prospect (50-69) | {metrics['warm_prospects']} | This week |",
            f"| 🔸 Lukewarm (30-49) | {metrics['lukewarm']} | This month |",
            f"| 🔵 Cold Re-Engagement (0-29) | {metrics['cold']} | Quarterly nurture |",
            "",
            "---",
            "",
            "## Loss Reason Analysis",
            "",
            "| Loss Reason | Count | % of Total |",
            "|---|---|---|",
        ]
        for item in self.get_loss_reason_breakdown():
            lines.append(
                f"| {item['reason']} | {item['count']} | {item['pct']}% |")

        lines.extend([
            "",
            "---",
            "",
            "## Client Recovery Plans",
            "",
        ])

        for i, client in enumerate(sorted(self.clients, key=lambda c: -c.recovery_score), 1):
            lines.extend(self._client_recovery_plan_md(client, i))

        lines.extend([
            "",
            "---",
            "",
            "## R.E.C.O.V.E.R. Action Plan",
            "",
            "### Week 1-2: Hot Lead Onslaught",
            "- Reach out to all Hot Lead tier clients personally",
            "- Prepare customized pitch for each based on loss reason",
            "- Offer time-sensitive recovery incentive (20% off first 3 months)",
            "",
            "### Week 3-4: Warm Prospect Nurturing",
            "- Execute win-back sequences for Warm Prospect tier",
            "- Send relevant industry insights before making contact",
            "- Schedule 30-minute discovery calls",
            "",
            "### Month 2: Lukewarm Campaign",
            "- Begin multi-touch nurture sequences",
            "- Invite to exclusive events/webinars",
            "- Share new capabilities and case studies",
            "",
            "### Quarter 2: Cold Re-Engagement",
            "- Quarterly newsletter with high-value content",
            "- Alumni program benefits and community access",
            "- Reassess recovery scores and adjust strategy",
            "",
            "---",
            "",
            "## Win-Back Email Templates",
            "",
            "### Template A: Recent Loss (1-30 days) — Gratitude & Feedback",
            "",
            "```",
            "Subject: Thank you — and a quick question",
            "",
            "Hi [Name],",
            "",
            "I wanted to personally thank you for the partnership we've had.",
            "Every client relationship teaches us something, and I'd love to",
            "learn from yours.",
            "",
            "Would you be open to a 10-minute call to share feedback on",
            "what worked, what didn't, and what we could improve?",
            "",
            "No pitch — just listening.",
            "",
            "Best,",
            "[Your Name]",
            "```",
            "",
            "### Template B: Mid-Loss (30-90 days) — Value Insight",
            "",
            "```",
            "Subject: Thought you'd find this interesting",
            "",
            "Hi [Name],",
            "",
            "Came across this [industry insight/article] and immediately",
            "thought of [Client Company]. Thought you might find it relevant",
            "to what you're working on.",
            "",
            "Hope everything's going well on your end.",
            "",
            "Best,",
            "[Your Name]",
            "```",
            "",
            "### Template C: Long-Term (90+ days) — Comeback Offer",
            "",
            "```",
            "Subject: A proposal worth reconsidering",
            "",
            "Hi [Name],",
            "",
            "It's been a while, and I'll be upfront — we'd love to work",
            "with [Client Company] again.",
            "",
            "We've made some significant improvements since we last worked",
            "together: [2-3 specific upgrades/capabilities].",
            "",
            "As a token of our commitment to rebuilding this relationship,",
            "I'd like to offer you 30% off your first 3 months back — no",
            "minimum commitment required.",
            "",
            "Would you be open to a 20-minute discussion next week?",
            "",
            "Best,",
            "[Your Name]",
            "```",
        ])
        return "\n".join(lines)

    def _client_recovery_plan_md(self, client, index):
        strategies = client.get_recovery_strategies()
        sequence = client.get_win_back_sequence()
        rec_value = client.estimated_recovery_value()
        lines = [
            f"### {index}. {client.name}",
            f"**Industry:** {client.industry.replace('_',' ').title()}",
            f"**Lost Service:** {client.service.replace('_',' ').title()}",
            f"**Loss Reason:** {LOSS_REASON_LABELS.get(client.reason, client.reason)}",
            f"**Months Since Loss:** {client.months_since_loss}",
            f"**Prior Annual Value:** ${client.prior_annual_value:,}",
            f"**Recovery Score:** {client.recovery_score}/100 — **{client.recovery_tier}**",
            f"**Estimated Recoverable Value:** ${rec_value:,}/year",
            "",
            "#### Win-Back Sequence",
            "",
            "| Timing | Action | Goal |",
            "|---|---|---|",
        ]
        for timing, action, goal in sequence:
            lines.append(f"| {timing} | {action} | {goal} |")

        lines.extend([
            "",
            "#### Top Recovery Strategies",
            "",
        ])
        for i, (name, desc) in enumerate(strategies[:3], 1):
            lines.append(f"{i}. **{name}:** {desc}")

        lines.append("")
        contacts = client.key_contacts
        if contacts:
            lines.append("#### Key Contacts")
            for c in contacts:
                strength_icon = {"strong": "🟢", "moderate": "🟡", "weak": "🔴", "none": "⚪"}
                icon = strength_icon.get(c["strength"], "⚪")
                lines.append(f"- {icon} {c['name']} — {c['role']} ({c['strength']})")
        lines.append("")
        return lines

    def generate_report_html(self):
        md = self.generate_recovery_report_markdown()
        # Simple HTML conversion
        import html
        html_body = "<pre>" + html.escape(md) + "</pre>"
        return f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Revenue Recovery Report</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
       max-width: 960px; margin: 2rem auto; padding: 0 1rem; line-height: 1.6; color: #e0e0e0; background: #111; }}
h1 {{ color: #ff6b35; border-bottom: 2px solid #333; padding-bottom: 0.5rem; }}
h2 {{ color: #ff8c42; margin-top: 2rem; }}
h3 {{ color: #ffa766; }}
pre {{ background: #1a1a1a; border: 1px solid #333; border-radius: 8px; padding: 1rem; overflow-x: auto; white-space: pre-wrap; }}
table {{ border-collapse: collapse; width: 100%; margin: 1rem 0; }}
th, td {{ border: 1px solid #333; padding: 0.5rem; text-align: left; }}
th {{ background: #222; color: #ff8c42; }}
code {{ background: #222; padding: 0.1rem 0.3rem; border-radius: 3px; }}
hr {{ border: 1px solid #333; margin: 2rem 0; }}
.container {{ background: #1a1a1a; border-radius: 12px; padding: 2rem; }}
.generated {{ text-align: center; color: #666; margin-top: 2rem; font-size: 0.8rem; }}
</style>
</head>
<body>
<div class="container">
{html_body}
<p class="generated">Generated by AI Agency Revenue Recovery Tool v{VERSION} | {DATE}</p>
</div>
</body>
</html>"""

    def generate_report_csv(self):
        rows = []
        for c in sorted(self.clients, key=lambda c: -c.recovery_score):
            rows.append({
                "Client Name": c.name,
                "Industry": c.industry,
                "Service": c.service,
                "Loss Reason": LOSS_REASON_LABELS.get(c.reason, c.reason),
                "Months Since Loss": c.months_since_loss,
                "Prior Annual Value": c.prior_annual_value,
                "Recovery Score": c.recovery_score,
                "Recovery Tier": c.recovery_tier,
                "Recoverable Value": c.estimated_recovery_value(),
                "Key Contacts": "; ".join(f"{x['name']} ({x['role']})" for x in c.key_contacts),
            })
        return rows

    def generate_report_json(self):
        return {
            "report_metadata": {
                "title": "Revenue Recovery & Win-Back Analysis",
                "framework": "R.E.C.O.V.E.R.",
                "generated": DATE,
                "version": VERSION,
            },
            "aggregate_metrics": self.aggregate_metrics(),
            "loss_reason_breakdown": self.get_loss_reason_breakdown(),
            "clients": [c.to_dict() for c in self.clients],
            "recovery_framework": "R.E.C.O.V.E.R. — Research, Evaluate, Craft, Orchestrate, Verify, Execute, Retain",
        }


# ─────────────────────────────────────────────────────────
# Interactive Mode
# ─────────────────────────────────────────────────────────

def interactive_mode():
    print("\n" + "=" * 60)
    print("  AI Agency Revenue Recovery & Win-Back Automation Tool")
    print("  R.E.C.O.V.E.R. Framework")
    print("=" * 60 + "\n")

    print(REVENUE_RECOVERY_FRAMEWORK)
    print()

    # Collect client info
    print("--- Enter Lost Client Information ---")
    print("(Press Enter at name to finish)\n")

    clients = []
    client_num = 1

    while True:
        print(f"\n--- Client #{client_num} ---")
        default_name = CLIENT_TEMPLATES[client_num - 1]['name'] if client_num <= len(CLIENT_TEMPLATES) else ''
        name = input(f"  Client name [{default_name}]: ").strip()
        if not name and client_num > len(CLIENT_TEMPLATES):
            if clients:
                break
            # Use sample
                print("  Using sample client data...")
            for t in CLIENT_TEMPLATES:
                clients.append(ClientLost(**t))
            break
        elif not name:
            name = CLIENT_TEMPLATES[client_num - 1]["name"] if client_num <= len(CLIENT_TEMPLATES) else f"Client {client_num}"

        industry = input(f"  Industry ({', '.join(INDUSTRIES[:8])}...) [{CLIENT_TEMPLATES[client_num-1]['industry'] if client_num <= len(CLIENT_TEMPLATES) else 'saas'}]: ").strip() or \
            (CLIENT_TEMPLATES[client_num-1]['industry'] if client_num <= len(CLIENT_TEMPLATES) else 'saas')
        if industry not in INDUSTRIES:
            industry = "saas"

        service = input(f"  Service Line ({', '.join(SERVICE_LINES[:5])}...) [{CLIENT_TEMPLATES[client_num-1]['service'] if client_num <= len(CLIENT_TEMPLATES) else 'digital_marketing'}]: ").strip() or \
            (CLIENT_TEMPLATES[client_num-1]['service'] if client_num <= len(CLIENT_TEMPLATES) else 'digital_marketing')

        print("  Loss Reasons:")
        for k, v in list(LOSS_REASON_LABELS.items())[:10]:
            print(f"    {k}: {v}")
        reason = input(f"  Loss reason [{CLIENT_TEMPLATES[client_num-1]['reason'] if client_num <= len(CLIENT_TEMPLATES) else 'budget_cuts'}]: ").strip() or \
            (CLIENT_TEMPLATES[client_num-1]['reason'] if client_num <= len(CLIENT_TEMPLATES) else 'budget_cuts')

        months = input(f"  Months since loss [{CLIENT_TEMPLATES[client_num-1]['months_since_loss'] if client_num <= len(CLIENT_TEMPLATES) else '3'}]: ").strip()
        months = int(months) if months else (CLIENT_TEMPLATES[client_num-1]['months_since_loss'] if client_num <= len(CLIENT_TEMPLATES) else 3)

        value = input(f"  Prior annual contract value ($) [{CLIENT_TEMPLATES[client_num-1]['prior_annual_value'] if client_num <= len(CLIENT_TEMPLATES) else '50000'}]: ").strip()
        value = int(value.replace(",", "")) if value else (CLIENT_TEMPLATES[client_num-1]['prior_annual_value'] if client_num <= len(CLIENT_TEMPLATES) else 50000)

        prob_str = input(f"  Recovery probability (0.0-1.0) [{CLIENT_TEMPLATES[client_num-1]['recovery_probability'] if client_num <= len(CLIENT_TEMPLATES) else '0.5'}]: ").strip()
        prob = float(prob_str) if prob_str else (CLIENT_TEMPLATES[client_num-1]['recovery_probability'] if client_num <= len(CLIENT_TEMPLATES) else 0.5)

        clients.append(ClientLost(name, industry, service, reason, months, value, prob))
        client_num += 1

        more = input("\n  Add another client? (Y/n): ").strip().lower()
        if more == 'n':
            break

    if not clients:
        print("  Using sample client data...")
        for t in CLIENT_TEMPLATES:
            clients.append(ClientLost(**t))

    program = RecoveryProgram(clients)

    # Generate outputs
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "recovery_outputs")
    os.makedirs(output_dir, exist_ok=True)

    # Markdown
    md_path = os.path.join(output_dir, f"revenue_recovery_report_{DATE}.md")
    with open(md_path, "w") as f:
        f.write(program.generate_recovery_report_markdown())
    print(f"\n✅ Report saved: {md_path}")

    # HTML
    html_path = os.path.join(output_dir, f"revenue_recovery_report_{DATE}.html")
    with open(html_path, "w") as f:
        f.write(program.generate_report_html())
    print(f"✅ HTML report: {html_path}")

    # CSV
    csv_path = os.path.join(output_dir, f"revenue_recovery_clients_{DATE}.csv")
    csv_rows = program.generate_report_csv()
    with open(csv_path, "w", newline="") as f:
        if csv_rows:
            writer = csv.DictWriter(f, fieldnames=csv_rows[0].keys())
            writer.writeheader()
            writer.writerows(csv_rows)
    print(f"✅ CSV export: {csv_path}")

    # JSON
    json_path = os.path.join(output_dir, f"revenue_recovery_report_{DATE}.json")
    with open(json_path, "w") as f:
        json.dump(program.generate_report_json(), f, indent=2)
    print(f"✅ JSON export: {json_path}")

    metrics = program.aggregate_metrics()
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                     RECOVERY SUMMARY                        ║
╠══════════════════════════════════════════════════════════════╣
║  Clients Analyzed:          {metrics['total_clients_lost']:>5d}                        ║
║  Total Value Lost:       ${metrics['total_annual_value_lost']:>8,}                     ║
║  Recoverable Value:      ${metrics['total_recoverable_annual_value']:>8,}                     ║
║  Recovery Rate:            {metrics['recovery_rate_pct']:>5.1f}%                        ║
║  Avg Recovery Score:       {metrics['average_recovery_score']:>5.1f}/100                    ║
║  Hot Leads:               {metrics['hot_leads']:>5d}                        ║
║  Warm Prospects:          {metrics['warm_prospects']:>5d}                        ║
╚══════════════════════════════════════════════════════════════╝
    """)
    print(f"All outputs in: {output_dir}/")
    return program


def batch_mode(batch_file):
    """Process client data from a JSON file."""
    with open(batch_file) as f:
        data = json.load(f)

    clients = []
    for item in data.get("clients", data):
        if isinstance(item, dict):
            name = item.get("name", item.get("client_name", "Unknown"))
            industry = item.get("industry", "saas")
            service = item.get("service", item.get("service_line", "digital_marketing"))
            reason = item.get("reason", item.get("loss_reason", "budget_cuts"))
            months = int(item.get("months_since_loss", item.get("months", 3)))
            value = int(item.get("prior_annual_value", item.get("annual_value", 50000)))
            prob = float(item.get("recovery_probability", item.get("probability", 0.5)))
            contacts = item.get("key_contacts", [])
            clients.append(ClientLost(name, industry, service, reason, months, value, prob, contacts))

    if not clients:
        print("No valid client data found in batch file.")
        sys.exit(1)

    program = RecoveryProgram(clients)
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "recovery_outputs")
    os.makedirs(output_dir, exist_ok=True)

    base_name = os.path.splitext(os.path.basename(batch_file))[0]
    formats = data.get("output_formats", ["md", "html", "csv", "json"])

    if "md" in formats:
        path = os.path.join(output_dir, f"{base_name}_report.md")
        with open(path, "w") as f:
            f.write(program.generate_recovery_report_markdown())
        print(f"✅ {path}")

    if "html" in formats:
        path = os.path.join(output_dir, f"{base_name}_report.html")
        with open(path, "w") as f:
            f.write(program.generate_report_html())
        print(f"✅ {path}")

    if "csv" in formats:
        path = os.path.join(output_dir, f"{base_name}_clients.csv")
        csv_rows = program.generate_report_csv()
        with open(path, "w", newline="") as f:
            if csv_rows:
                writer = csv.DictWriter(f, fieldnames=csv_rows[0].keys())
                writer.writeheader()
                writer.writerows(csv_rows)
        print(f"✅ {path}")

    if "json" in formats:
        path = os.path.join(output_dir, f"{base_name}_report.json")
        with open(path, "w") as f:
            json.dump(program.generate_report_json(), f, indent=2)
        print(f"✅ {path}")

    return program


# ─────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="AI Agency Revenue Recovery & Lost Client Win-Back Automation Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Examples:
              %(prog)s                           # Interactive mode with sample data
              %(prog)s --industry saas --output md,html
              %(prog)s --batch clients.json
              %(prog)s --batch clients.json --output json
        """)
    )
    parser.add_argument("--industry", "-i", help="Industry filter")
    parser.add_argument("--output", "-o", default="md,html,csv,json",
                        help="Output formats: md,html,csv,json (comma-separated)")
    parser.add_argument("--batch", "-b", help="Batch file path (JSON)")
    parser.add_argument("--version", "-v", action="store_true", help="Show version")

    args = parser.parse_args()

    if args.version:
        print(f"AI Agency Revenue Recovery Tool v{VERSION}")
        return

    if args.batch:
        batch_mode(args.batch)
    else:
        interactive_mode()


if __name__ == "__main__":
    main()