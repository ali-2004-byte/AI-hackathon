"""Export functionality for Opportunity Inbox Copilot.

This module provides export functions for ranked opportunities:
- PDF export (single and multi-page)
- CSV export
- Clipboard copy (markdown)
- Calendar ICS generation

All exports follow the design_system.md specifications for colors and styling.
"""

import csv
import io
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    Image,
    PageBreak,
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfgen import canvas

from src.models import RankedOpportunity, UrgencyTier, OpportunityType


# =============================================================================
# DESIGN SYSTEM COLORS
# =============================================================================

COLORS = {
    # Primary palette
    "background": "#F8F9FB",
    "surface": "#FFFFFF",
    "brand": "#4F46E5",  # Indigo
    "brand_dark": "#4338CA",
    "text_primary": "#1A1D23",
    "text_secondary": "#6B7280",
    "border": "#E5E7EB",

    # Urgency colors
    "critical": "#EF4444",
    "critical_bg": "#FEF2F2",
    "urgent": "#F59E0B",
    "urgent_bg": "#FFFBEB",
    "moderate": "#84CC16",
    "moderate_bg": "#F7FEE7",
    "comfortable": "#10B981",
    "comfortable_bg": "#ECFDF5",
    "rolling": "#6366F1",
    "rolling_bg": "#EEF2FF",
    "unknown": "#94A3B8",
    "unknown_bg": "#F8FAFC",

    # Match score colors
    "match_high": "#10B981",
    "match_medium": "#F59E0B",
    "match_low": "#6B7280",
}


def _hex_to_reportlab(hex_color: str) -> colors.Color:
    """Convert hex color to reportlab Color."""
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16) / 256.0
    g = int(hex_color[2:4], 16) / 256.0
    b = int(hex_color[4:6], 16) / 256.0
    return colors.Color(r, g, b)


def _get_urgency_color(urgency_tier: Optional[UrgencyTier]) -> str:
    """Get urgency color hex code."""
    if urgency_tier is None:
        return COLORS["unknown"]
    tier_map = {
        UrgencyTier.CRITICAL: COLORS["critical"],
        UrgencyTier.URGENT: COLORS["urgent"],
        UrgencyTier.MODERATE: COLORS["moderate"],
        UrgencyTier.COMFORTABLE: COLORS["comfortable"],
        UrgencyTier.ROLLING: COLORS["rolling"],
        UrgencyTier.UNKNOWN: COLORS["unknown"],
    }
    return tier_map.get(urgency_tier, COLORS["unknown"])


def _get_urgency_bg_color(urgency_tier: Optional[UrgencyTier]) -> str:
    """Get urgency background color hex code."""
    if urgency_tier is None:
        return COLORS["unknown_bg"]
    tier_map = {
        UrgencyTier.CRITICAL: COLORS["critical_bg"],
        UrgencyTier.URGENT: COLORS["urgent_bg"],
        UrgencyTier.MODERATE: COLORS["moderate_bg"],
        UrgencyTier.COMFORTABLE: COLORS["comfortable_bg"],
        UrgencyTier.ROLLING: COLORS["rolling_bg"],
        UrgencyTier.UNKNOWN: COLORS["unknown_bg"],
    }
    return tier_map.get(urgency_tier, COLORS["unknown_bg"])


def _get_match_color(score: float) -> str:
    """Get match score color."""
    if score >= 80:
        return COLORS["match_high"]
    elif score >= 60:
        return COLORS["match_medium"]
    else:
        return COLORS["match_low"]


def _get_urgency_label(urgency_tier: Optional[UrgencyTier]) -> str:
    """Get urgency tier label."""
    if urgency_tier is None:
        return "UNKNOWN"
    return urgency_tier.value.upper()


# =============================================================================
# EXPORT TO PDF - SINGLE OPPORTUNITY
# =============================================================================

def export_to_pdf(opportunity: RankedOpportunity) -> io.BytesIO:
    """Export a single opportunity to a professional PDF.

    Features:
    - Professional layout matching design_system.md
    - Header with opportunity title
    - Summary section (match score, deadline, award)
    - Action checklist with checkboxes
    - Evidence quotes section
    - Color-coded by urgency

    Args:
        opportunity: RankedOpportunity to export

    Returns:
        BytesIO buffer containing the PDF
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )

    elements = []
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Heading1"],
        fontSize=24,
        textColor=_hex_to_reportlab(COLORS["text_primary"]),
        spaceAfter=12,
        fontName="Helvetica-Bold",
    )

    heading_style = ParagraphStyle(
        "CustomHeading",
        parent=styles["Heading2"],
        fontSize=16,
        textColor=_hex_to_reportlab(COLORS["text_primary"]),
        spaceAfter=10,
        spaceBefore=12,
        fontName="Helvetica-Bold",
    )

    normal_style = ParagraphStyle(
        "CustomNormal",
        parent=styles["Normal"],
        fontSize=11,
        textColor=_hex_to_reportlab(COLORS["text_secondary"]),
        fontName="Helvetica",
    )

    # Get opportunity data
    opp = opportunity.opportunity
    urgency_color = _get_urgency_color(opportunity.urgency_tier)
    urgency_bg = _get_urgency_bg_color(opportunity.urgency_tier)
    match_color = _get_match_color(opportunity.composite_score)

    # Header with left accent bar
    header_data = [
        [Paragraph(f"<b>{opp.title or 'Untitled Opportunity'}</b>", title_style)],
    ]
    header_table = Table(header_data, colWidths=[6.5 * inch])
    header_table.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("LEFTLINE", (0, 0), (0, 0), 4, _hex_to_reportlab(urgency_color)),
    ]))
    elements.append(header_table)

    # Summary bar with urgency badge and match score
    summary_data = [
        [
            Paragraph(
                f'<b><font color="{urgency_color}">{_get_urgency_label(opportunity.urgency_tier)}</font></b>',
                normal_style
            ),
            Paragraph(
                f'<b><font color="{match_color}">{opportunity.composite_score:.0f}% Match</font></b>',
                normal_style
            ),
            Paragraph(
                f"<b>Type:</b> {opp.opportunity_type.value.title() if opp.opportunity_type else 'Unknown'}",
                normal_style
            ),
        ]
    ]
    summary_table = Table(summary_data, colWidths=[2 * inch, 2 * inch, 2.5 * inch])
    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), _hex_to_reportlab(urgency_bg)),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("ROUNDEDCORNERS", [0, 0, -1, -1], 8),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 0.25 * inch))

    # Details section
    elements.append(Paragraph("Opportunity Details", heading_style))

    details_data = []

    if opp.organization:
        details_data.append(["Organization:", opp.organization])

    if opp.location:
        details_data.append(["Location:", opp.location])

    if opp.benefits:
        details_data.append(["Award/Benefits:", opp.benefits])

    # Deadline info
    deadline_text = opp.deadline_text or "No deadline specified"
    if opportunity.days_left is not None:
        deadline_text += f" ({opportunity.days_left} days left)"
    details_data.append(["Deadline:", deadline_text])

    if opp.duration:
        details_data.append(["Duration:", opp.duration])

    if opp.application_link:
        details_data.append(["Application Link:", opp.application_link])

    if details_data:
        details_table = Table(details_data, colWidths=[2 * inch, 4.5 * inch])
        details_table.setStyle(TableStyle([
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("FONT", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONT", (1, 0), (1, -1), "Helvetica"),
            ("TEXTFONT", (0, 0), (-1, -1), "Helvetica"),
        ]))
        elements.append(details_table)

    elements.append(Spacer(1, 0.25 * inch))

    # Why this rank section
    if opportunity.ranking_reasons:
        elements.append(Paragraph("Why This Rank?", heading_style))
        for reason in opportunity.ranking_reasons:
            elements.append(Paragraph(f"&bull; {reason}", normal_style))
        elements.append(Spacer(1, 0.2 * inch))

    # Action checklist section
    if opportunity.action_checklist:
        elements.append(Paragraph("Action Checklist", heading_style))

        checklist_data = []
        for i, action in enumerate(opportunity.action_checklist, 1):
            action_text = action.get("action", str(action))
            priority = action.get("priority", "medium")
            priority_color = {"high": COLORS["critical"], "medium": COLORS["urgent"], "low": COLORS["text_secondary"]}.get(priority, COLORS["text_secondary"])
            checkbox = "[ ]"  # Empty checkbox
            checklist_data.append([
                Paragraph(f'<font color="{priority_color}">{checkbox}</font>', normal_style),
                Paragraph(action_text, normal_style),
            ])

        checklist_table = Table(checklist_data, colWidths=[0.4 * inch, 6.1 * inch])
        checklist_table.setStyle(TableStyle([
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))
        elements.append(checklist_table)
        elements.append(Spacer(1, 0.25 * inch))

    # Required documents section
    if opp.required_documents:
        elements.append(Paragraph("Required Documents", heading_style))
        for doc in opp.required_documents:
            elements.append(Paragraph(f"&square; {doc}", normal_style))
        elements.append(Spacer(1, 0.2 * inch))

    # Evidence quotes section
    if opp.raw_excerpts:
        elements.append(Paragraph("Evidence from Email", heading_style))
        for excerpt in opp.raw_excerpts:
            quote_style = ParagraphStyle(
                "Quote",
                parent=normal_style,
                leftIndent=20,
                borderColor=_hex_to_reportlab(COLORS["border"]),
                borderWidth=3,
                borderPadding=(10, 0, 0, 10),
                fontStyle="italic",
            )
            elements.append(Paragraph(f'"{excerpt}"', quote_style))
            elements.append(Spacer(1, 6))

    # Footer
    elements.append(Spacer(1, 0.5 * inch))
    footer_style = ParagraphStyle(
        "Footer",
        parent=normal_style,
        fontSize=9,
        alignment=TA_CENTER,
    )
    elements.append(Paragraph(
        f"Generated by Opportunity Inbox Copilot | {datetime.now().strftime('%B %d, %Y')}",
        footer_style
    ))

    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer


# =============================================================================
# EXPORT TO CSV
# =============================================================================

def export_to_csv(opportunities: List[RankedOpportunity]) -> str:
    """Export all opportunities to CSV format.

    Columns: Rank, Title, Type, Organization, Deadline, Days Left,
             Match Score, Award, Link

    Args:
        opportunities: List of RankedOpportunity objects

    Returns:
        CSV string
    """
    output = io.StringIO()
    writer = csv.writer(output)

    # Header row
    writer.writerow([
        "Rank",
        "Title",
        "Type",
        "Organization",
        "Deadline",
        "Days Left",
        "Match Score",
        "Award",
        "Application Link",
        "Urgency Tier",
        "Location",
    ])

    # Data rows
    for i, opp in enumerate(opportunities, 1):
        opportunity = opp.opportunity
        writer.writerow([
            i,
            opportunity.title or "Untitled",
            opportunity.opportunity_type.value.title() if opportunity.opportunity_type else "Unknown",
            opportunity.organization or "",
            opportunity.deadline_text or (opportunity.deadline_date.isoformat() if opportunity.deadline_date else ""),
            opp.days_left if opp.days_left is not None else "",
            f"{opp.composite_score:.0f}%",
            opportunity.benefits or "",
            opportunity.application_link or "",
            _get_urgency_label(opp.urgency_tier),
            opportunity.location or "",
        ])

    return output.getvalue()


# =============================================================================
# COPY TO CLIPBOARD (MARKDOWN)
# =============================================================================

def copy_to_clipboard(opportunities: List[RankedOpportunity], top_n: int = 5) -> str:
    """Generate a formatted markdown summary for clipboard copy.

    Includes top N opportunities with key info.
    Easy to paste into Slack, email, docs.

    Args:
        opportunities: List of RankedOpportunity objects
        top_n: Number of top opportunities to include (default: 5)

    Returns:
        Markdown string
    """
    lines = []
    lines.append("# 🎯 Your Top Opportunities")
    lines.append("")
    lines.append(f"*Generated on {datetime.now().strftime('%B %d, %Y')}*")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Summary stats
    total = len(opportunities)
    if total > 0:
        avg_score = sum(o.composite_score for o in opportunities) / total
        critical_count = sum(1 for o in opportunities if o.urgency_tier == UrgencyTier.CRITICAL)
        urgent_count = sum(1 for o in opportunities if o.urgency_tier == UrgencyTier.URGENT)

        lines.append("**Summary:**")
        lines.append(f"- Total opportunities: {total}")
        lines.append(f"- Average match score: {avg_score:.0f}%")
        lines.append(f"- Critical/Urgent: {critical_count}/{urgent_count}")
        lines.append("")
        lines.append("---")
        lines.append("")

    # Top opportunities
    top_opportunities = opportunities[:top_n]

    for i, opp in enumerate(top_opportunities, 1):
        opportunity = opp.opportunity
        urgency_label = _get_urgency_label(opp.urgency_tier)
        urgency_emoji = {"CRITICAL": "🔴", "URGENT": "🟠", "MODERATE": "🟡", "COMFORTABLE": "🟢", "ROLLING": "🔵", "UNKNOWN": "⚪"}.get(urgency_label, "⚪")

        lines.append(f"## #{i} {opportunity.title or 'Untitled'}")
        lines.append("")
        lines.append(f"**Type:** {opportunity.opportunity_type.value.title() if opportunity.opportunity_type else 'Unknown'} | **Match:** {opp.composite_score:.0f}% | **Urgency:** {urgency_emoji} {urgency_label}")
        lines.append("")

        if opportunity.organization:
            lines.append(f"**Organization:** {opportunity.organization}")

        if opportunity.location:
            lines.append(f"**Location:** {opportunity.location}")

        if opportunity.benefits:
            lines.append(f"**Award:** {opportunity.benefits}")

        deadline_info = opportunity.deadline_text or (opportunity.deadline_date.isoformat() if opportunity.deadline_date else "No deadline")
        if opp.days_left is not None:
            deadline_info += f" ({opp.days_left} days left)"
        lines.append(f"**Deadline:** {deadline_info}")
        lines.append("")

        if opp.ranking_reasons:
            lines.append("**Why this rank:**")
            for reason in opp.ranking_reasons[:3]:  # Top 3 reasons
                lines.append(f"- {reason}")
            lines.append("")

        if opportunity.application_link:
            lines.append(f"**🔗 Apply:** {opportunity.application_link}")
            lines.append("")

        lines.append("---")
        lines.append("")

    # Footer
    lines.append("*Generated by Opportunity Inbox Copilot*")

    return "\n".join(lines)


# =============================================================================
# GENERATE CALENDAR ICS
# =============================================================================

def generate_calendar_ics(opportunities: List[RankedOpportunity]) -> str:
    """Generate .ics calendar events for opportunity deadlines.

    Creates events with:
    - Title: "Apply: {Opportunity Name}"
    - Due date: deadline_date
    - Reminders: 1 day before, 1 hour before
    - Description: application link + requirements

    Args:
        opportunities: List of RankedOpportunity objects

    Returns:
        ICS string
    """
    lines = []
    lines.append("BEGIN:VCALENDAR")
    lines.append("VERSION:2.0")
    lines.append("PRODID:-//Opportunity Inbox Copilot//EN")
    lines.append("CALSCALE:GREGORIAN")
    lines.append("METHOD:PUBLISH")
    lines.append("X-WR-CALNAME:Opportunity Deadlines")
    lines.append("X-WR-CALDESC:Application deadlines for your ranked opportunities")

    today = datetime.now().date()

    for opp in opportunities:
        opportunity = opp.opportunity

        # Determine event date
        event_date = None
        if opportunity.deadline_date:
            event_date = opportunity.deadline_date
        elif opp.days_left is not None and opp.days_left > 0:
            event_date = today + timedelta(days=opp.days_left)

        # Skip if no valid date
        if event_date is None:
            continue

        # Create event
        lines.append("BEGIN:VEVENT")
        lines.append(f"UID:{datetime.now().strftime('%Y%m%d%H%M%S')}-{opportunity.title or 'untitled'}@opportunity-copilot")
        lines.append(f"DTSTAMP:{datetime.now().strftime('%Y%m%dT%H%M%S')}Z")
        lines.append(f"DTSTART;VALUE=DATE:{event_date.strftime('%Y%m%d')}")
        lines.append(f"DTEND;VALUE=DATE:{event_date.strftime('%Y%m%d')}")
        lines.append(f"SUMMARY:Apply: {opportunity.title or 'Opportunity'}")

        # Build description
        desc_parts = []
        if opportunity.organization:
            desc_parts.append(f"Organization: {opportunity.organization}")
        if opportunity.application_link:
            desc_parts.append(f"Apply at: {opportunity.application_link}")
        if opp.action_checklist:
            desc_parts.append("Required actions:")
            for action in opp.action_checklist[:5]:
                action_text = action.get("action", str(action))
                desc_parts.append(f"  - {action_text}")
        if opp.days_left is not None:
            desc_parts.append(f"Days remaining: {opp.days_left}")

        description = "\\n".join(desc_parts) if desc_parts else "Application deadline"
        lines.append(f"DESCRIPTION:{description}")

        # Add priority based on urgency
        priority = 5  # Normal priority
        if opp.urgency_tier == UrgencyTier.CRITICAL:
            priority = 1  # Highest
        elif opp.urgency_tier == UrgencyTier.URGENT:
            priority = 2
        elif opp.urgency_tier == UrgencyTier.MODERATE:
            priority = 3
        lines.append(f"PRIORITY:{priority}")

        # Reminders (VALARM)
        lines.append("BEGIN:VALARM")
        lines.append("ACTION:DISPLAY")
        lines.append("DESCRIPTION:Reminder: Application due tomorrow")
        lines.append("TRIGGER:-P1D")  # 1 day before
        lines.append("END:VALARM")

        lines.append("BEGIN:VALARM")
        lines.append("ACTION:DISPLAY")
        lines.append("DESCRIPTION:Reminder: Application due in 1 hour")
        lines.append("TRIGGER:-PT1H")  # 1 hour before
        lines.append("END:VALARM")

        lines.append("END:VEVENT")

    lines.append("END:VCALENDAR")

    return "\r\n".join(lines)


# =============================================================================
# EXPORT ALL TO PDF (MULTI-PAGE)
# =============================================================================

def export_all_to_pdf(opportunities: List[RankedOpportunity]) -> io.BytesIO:
    """Export all opportunities to a multi-page PDF.

    Features:
    - Table of contents
    - Summary dashboard page
    - One page per opportunity
    - Appendix with action checklists

    Args:
        opportunities: List of RankedOpportunity objects

    Returns:
        BytesIO buffer containing the PDF
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )

    elements = []
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Heading1"],
        fontSize=28,
        textColor=_hex_to_reportlab(COLORS["brand"]),
        spaceAfter=6,
        fontName="Helvetica-Bold",
        alignment=TA_CENTER,
    )

    subtitle_style = ParagraphStyle(
        "ReportSubtitle",
        parent=styles["Normal"],
        fontSize=14,
        textColor=_hex_to_reportlab(COLORS["text_secondary"]),
        spaceAfter=24,
        fontName="Helvetica",
        alignment=TA_CENTER,
    )

    heading_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontSize=18,
        textColor=_hex_to_reportlab(COLORS["text_primary"]),
        spaceAfter=12,
        spaceBefore=12,
        fontName="Helvetica-Bold",
    )

    normal_style = ParagraphStyle(
        "BodyText",
        parent=styles["Normal"],
        fontSize=11,
        textColor=_hex_to_reportlab(COLORS["text_secondary"]),
        fontName="Helvetica",
    )

    # Title page
    elements.append(Spacer(1, 1.5 * inch))
    elements.append(Paragraph("Opportunity Dashboard", title_style))
    elements.append(Paragraph(f"Generated on {datetime.now().strftime('%B %d, %Y')}", subtitle_style))
    elements.append(Spacer(1, 0.5 * inch))

    # Summary stats
    total = len(opportunities)
    if total > 0:
        avg_score = sum(o.composite_score for o in opportunities) / total
        critical_count = sum(1 for o in opportunities if o.urgency_tier == UrgencyTier.CRITICAL)
        urgent_count = sum(1 for o in opportunities if o.urgency_tier == UrgencyTier.URGENT)
        moderate_count = sum(1 for o in opportunities if o.urgency_tier == UrgencyTier.MODERATE)
        comfortable_count = sum(1 for o in opportunities if o.urgency_tier == UrgencyTier.COMFORTABLE)
        rolling_count = sum(1 for o in opportunities if o.urgency_tier == UrgencyTier.ROLLING)

        summary_data = [
            ["Total Opportunities", str(total)],
            ["Average Match Score", f"{avg_score:.0f}%"],
            ["Critical", str(critical_count)],
            ["Urgent", str(urgent_count)],
            ["Moderate", str(moderate_count)],
            ["Comfortable", str(comfortable_count)],
            ["Rolling", str(rolling_count)],
        ]

        summary_table = Table(summary_data, colWidths=[3 * inch, 2 * inch])
        summary_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), _hex_to_reportlab(COLORS["brand"])),
            ("BACKGROUND", (1, 0), (1, -1), _hex_to_reportlab(COLORS["surface"])),
            ("TEXTCOLOR", (0, 0), (0, -1), colors.white),
            ("TEXTCOLOR", (1, 0), (1, -1), _hex_to_reportlab(COLORS["text_primary"])),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 12),
            ("RIGHTPADDING", (0, 0), (-1, -1), 12),
            ("TOPPADDING", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ("FONT", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONT", (1, 0), (1, -1), "Helvetica"),
            ("ROUNDEDCORNERS", [0, 0, -1, -1], 8),
        ]))

        elements.append(summary_table)

    elements.append(PageBreak())

    # Table of Contents
    elements.append(Paragraph("Table of Contents", heading_style))

    toc_data = []
    for i, opp in enumerate(opportunities, 1):
        title = opp.opportunity.title or f"Opportunity {i}"
        urgency = _get_urgency_label(opp.urgency_tier)
        score = opp.composite_score
        toc_data.append([f"{i}.", title, f"{score:.0f}% Match", urgency])

    toc_table = Table(toc_data, colWidths=[0.4 * inch, 4.5 * inch, 1 * inch, 1 * inch])
    toc_table.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("FONT", (0, 0), (0, -1), "Helvetica-Bold"),
        ("LINEBELOW", (0, 0), (-1, -1), 1, _hex_to_reportlab(COLORS["border"])),
    ]))
    elements.append(toc_table)

    elements.append(PageBreak())

    # Individual opportunity pages
    for i, opp in enumerate(opportunities, 1):
        # Page header with rank
        header_data = [[Paragraph(f"<b>#{i}: {opp.opportunity.title or 'Untitled'}</b>", heading_style)]]
        header_table = Table(header_data, colWidths=[6.5 * inch])
        header_table.setStyle(TableStyle([
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
            ("LEFTLINE", (0, 0), (0, 0), 4, _hex_to_reportlab(_get_urgency_color(opp.urgency_tier))),
        ]))
        elements.append(header_table)

        # Quick stats bar
        urgency_color = _get_urgency_color(opp.urgency_tier)
        match_color = _get_match_color(opp.composite_score)
        stats_data = [[
            Paragraph(f'<b><font color="{urgency_color}">{_get_urgency_label(opp.urgency_tier)}</font></b>', normal_style),
            Paragraph(f'<b><font color="{match_color}">{opp.composite_score:.0f}% Match</font></b>', normal_style),
            Paragraph(f"<b>Type:</b> {opp.opportunity_type.value.title() if opp.opportunity_type else 'Unknown'}", normal_style),
        ]]
        stats_table = Table(stats_data, colWidths=[2 * inch, 2 * inch, 2.5 * inch])
        stats_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), _hex_to_reportlab(_get_urgency_bg_color(opp.urgency_tier))),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 12),
            ("RIGHTPADDING", (0, 0), (-1, -1), 12),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("ROUNDEDCORNERS", [0, 0, -1, -1], 6),
        ]))
        elements.append(stats_table)
        elements.append(Spacer(1, 0.2 * inch))

        # Opportunity details
        opp_data = opp.opportunity
        details_data = []

        if opp_data.organization:
            details_data.append(["Organization:", opp_data.organization])
        if opp_data.location:
            details_data.append(["Location:", opp_data.location])
        if opp_data.benefits:
            details_data.append(["Award:", opp_data.benefits])

        deadline_info = opp_data.deadline_text or "No deadline"
        if opp.days_left is not None:
            deadline_info += f" ({opp.days_left} days left)"
        details_data.append(["Deadline:", deadline_info])

        if opp_data.application_link:
            details_data.append(["Link:", opp_data.application_link])

        if details_data:
            details_table = Table(details_data, colWidths=[1.5 * inch, 5 * inch])
            details_table.setStyle(TableStyle([
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("FONT", (0, 0), (0, -1), "Helvetica-Bold"),
            ]))
            elements.append(details_table)

        elements.append(Spacer(1, 0.2 * inch))

        # Why this rank
        if opp.ranking_reasons:
            elements.append(Paragraph("Why This Rank?", heading_style))
            for reason in opp.ranking_reasons:
                elements.append(Paragraph(f"&bull; {reason}", normal_style))
            elements.append(Spacer(1, 0.2 * inch))

        # Action checklist
        if opp.action_checklist:
            elements.append(Paragraph("Action Checklist", heading_style))
            for action in opp.action_checklist:
                action_text = action.get("action", str(action))
                elements.append(Paragraph(f"&square; {action_text}", normal_style))
            elements.append(Spacer(1, 0.2 * inch))

        # Required documents
        if opp_data.required_documents:
            elements.append(Paragraph("Required Documents", heading_style))
            for doc in opp_data.required_documents:
                elements.append(Paragraph(f"&square; {doc}", normal_style))

        elements.append(PageBreak())

    # Appendix with all action checklists
    elements.append(Paragraph("Appendix: Complete Action Checklists", heading_style))
    elements.append(Spacer(1, 0.2 * inch))

    for i, opp in enumerate(opportunities, 1):
        elements.append(Paragraph(f"#{i} {opp.opportunity.title or 'Untitled'}", heading_style))

        if opp.action_checklist:
            for action in opp.action_checklist:
                action_text = action.get("action", str(action))
                priority = action.get("priority", "medium")
                elements.append(Paragraph(f"  &bull; [{priority.title()}] {action_text}", normal_style))

        if opp.opportunity.required_documents:
            elements.append(Paragraph("  Documents:", normal_style))
            for doc in opp.opportunity.required_documents:
                elements.append(Paragraph(f"    &square; {doc}", normal_style))

        elements.append(Spacer(1, 0.15 * inch))

    # Footer
    elements.append(Spacer(1, 0.5 * inch))
    footer_style = ParagraphStyle(
        "ReportFooter",
        parent=normal_style,
        fontSize=9,
        alignment=TA_CENTER,
    )
    elements.append(Paragraph(
        "Generated by Opportunity Inbox Copilot",
        footer_style
    ))

    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def download_pdf(buffer: io.BytesIO, filename: str) -> None:
    """Helper to download PDF buffer to file (for testing).

    Args:
        buffer: BytesIO buffer containing PDF
        filename: Output filename
    """
    with open(filename, "wb") as f:
        f.write(buffer.getvalue())


def download_ics(ics_string: str, filename: str) -> None:
    """Helper to download ICS string to file (for testing).

    Args:
        ics_string: ICS calendar string
        filename: Output filename
    """
    with open(filename, "w", encoding="utf-8") as f:
        f.write(ics_string)


def download_csv(csv_string: str, filename: str) -> None:
    """Helper to download CSV string to file (for testing).

    Args:
        csv_string: CSV string
        filename: Output filename
    """
    with open(filename, "w", encoding="utf-8", newline="") as f:
        f.write(csv_string)
