"""Design tokens for Opportunity Inbox Copilot.

This module contains all color constants, typography settings, and spacing values
defined in design_system.md for consistent UI implementation.
"""

# =============================================================================
# COLOR SYSTEM
# =============================================================================

# Primary Palette (Light Mode)
COLORS = {
    # Core theme colors
    "background": "#F8F9FB",      # Soft off-white background
    "surface": "#FFFFFF",          # Pure white cards/surfaces
    "brand": "#4F46E5",            # Indigo - primary brand color
    "brand_hover": "#4338CA",      # Darker indigo for hover states
    "brand_light": "#EEF2FF",      # Light indigo for backgrounds
    "text_primary": "#1A1D23",     # Near-black for primary text
    "text_secondary": "#6B7280",   # Gray for metadata/labels
    "text_tertiary": "#9CA3AF",    # Light gray for disabled text
    "border": "#E5E7EB",           # Subtle borders/dividers
    "border_focus": "#4F46E5",     # Indigo focus border

    # Urgency colors - CRITICAL (<=3 days)
    "critical": "#EF4444",
    "critical_bg": "#FEF2F2",
    "critical_border": "#FECACA",

    # Urgency colors - URGENT (4-7 days)
    "urgent": "#F59E0B",
    "urgent_bg": "#FFFBEB",
    "urgent_border": "#FDE68A",

    # Urgency colors - MODERATE (8-30 days)
    "moderate": "#84CC16",
    "moderate_bg": "#F7FEE7",
    "moderate_border": "#D9F99D",

    # Urgency colors - COMFORTABLE (31-60 days)
    "comfortable": "#10B981",
    "comfortable_bg": "#ECFDF5",
    "comfortable_border": "#A7F3D0",

    # Urgency colors - ROLLING (rolling basis)
    "rolling": "#6366F1",
    "rolling_bg": "#EEF2FF",
    "rolling_border": "#C7D2FE",

    # Urgency colors - UNKNOWN (no deadline)
    "unknown": "#94A3B8",
    "unknown_bg": "#F8FAFC",
    "unknown_border": "#CBD5E1",

    # Match score colors
    "match_high": "#10B981",       # 80-100% - Green
    "match_medium": "#F59E0B",     # 60-79% - Amber
    "match_low": "#6B7280",        # <60% - Gray

    # Feedback colors
    "success": "#10B981",
    "success_bg": "#ECFDF5",
    "warning": "#F59E0B",
    "warning_bg": "#FFFBEB",
    "error": "#EF4444",
    "error_bg": "#FEF2F2",
    "info": "#4F46E5",
    "info_bg": "#EEF2FF",
}

# =============================================================================
# TYPOGRAPHY
# =============================================================================

TYPOGRAPHY = {
    "font_family": "'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    "font_mono": "'JetBrains Mono', 'Fira Code', 'Courier New', monospace",

    # Font sizes (in pixels)
    "font_size_xs": "11px",
    "font_size_sm": "13px",
    "font_size_base": "15px",
    "font_size_md": "16px",
    "font_size_lg": "18px",
    "font_size_xl": "20px",
    "font_size_2xl": "24px",
    "font_size_3xl": "28px",
    "font_size_4xl": "32px",

    # Font weights
    "font_weight_normal": "400",
    "font_weight_medium": "500",
    "font_weight_semibold": "600",
    "font_weight_bold": "700",

    # Line heights
    "line_height_tight": "1.2",
    "line_height_normal": "1.5",
    "line_height_relaxed": "1.625",

    # Letter spacing
    "letter_spacing_tight": "-0.02em",
    "letter_spacing_normal": "0",
    "letter_spacing_wide": "0.025em",
    "letter_spacing_wider": "0.8px",
}

# =============================================================================
# SPACING (8px grid system)
# =============================================================================

SPACING = {
    "space_1": "4px",
    "space_2": "8px",
    "space_3": "12px",
    "space_4": "16px",
    "space_5": "20px",
    "space_6": "24px",
    "space_8": "32px",
    "space_10": "40px",
    "space_12": "48px",
    "space_16": "64px",
    "space_20": "80px",
}

# =============================================================================
# BORDER RADIUS
# =============================================================================

BORDER_RADIUS = {
    "none": "0",
    "sm": "6px",
    "md": "8px",
    "lg": "10px",
    "xl": "12px",
    "2xl": "16px",
    "3xl": "20px",
    "full": "9999px",
}

# =============================================================================
# SHADOWS
# =============================================================================

SHADOWS = {
    "none": "none",
    "sm": "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
    "md": "0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1)",
    "lg": "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1)",
    "xl": "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1)",
    "2xl": "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1)",
    "inner": "inset 0 2px 4px 0 rgba(0, 0, 0, 0.05)",
    "brand": "0 2px 4px rgba(79, 70, 229, 0.15)",
    "brand_hover": "0 8px 16px rgba(79, 70, 229, 0.25)",
}

# =============================================================================
# ANIMATIONS
# =============================================================================

ANIMATIONS = {
    "timing_smooth": "cubic-bezier(0.4, 0, 0.2, 1)",
    "timing_bounce": "cubic-bezier(0.68, -0.55, 0.265, 1.55)",
    "timing_ease": "cubic-bezier(0.25, 0.1, 0.25, 1)",
    "duration_fast": "150ms",
    "duration_normal": "200ms",
    "duration_slow": "300ms",
    "duration_slower": "500ms",
}

# =============================================================================
# URGENCY TIERS (Complete configuration)
# =============================================================================

URGENCY_TIERS = {
    "critical": {
        "color": COLORS["critical"],
        "bg": COLORS["critical_bg"],
        "border": COLORS["critical_border"],
        "label": "CRITICAL",
        "icon": "●",
        "description": "Act NOW - ≤3 days",
    },
    "urgent": {
        "color": COLORS["urgent"],
        "bg": COLORS["urgent_bg"],
        "border": COLORS["urgent_border"],
        "label": "URGENT",
        "icon": "●",
        "description": "This week - 4-7 days",
    },
    "moderate": {
        "color": COLORS["moderate"],
        "bg": COLORS["moderate_bg"],
        "border": COLORS["moderate_border"],
        "label": "MODERATE",
        "icon": "●",
        "description": "This month - 8-30 days",
    },
    "comfortable": {
        "color": COLORS["comfortable"],
        "bg": COLORS["comfortable_bg"],
        "border": COLORS["comfortable_border"],
        "label": "COMFORTABLE",
        "icon": "●",
        "description": "Plenty of time - 31-60 days",
    },
    "rolling": {
        "color": COLORS["rolling"],
        "bg": COLORS["rolling_bg"],
        "border": COLORS["rolling_border"],
        "label": "ROLLING",
        "icon": "●",
        "description": "Apply ASAP - Rolling basis",
    },
    "unknown": {
        "color": COLORS["unknown"],
        "bg": COLORS["unknown_bg"],
        "border": COLORS["unknown_border"],
        "label": "UNKNOWN",
        "icon": "○",
        "description": "Verify deadline date",
    },
}

# =============================================================================
# OPPORTUNITY TYPE ICONS
# =============================================================================

TYPE_ICONS = {
    "scholarship": {"icon": "$", "label": "Scholarship", "color": COLORS["brand"]},
    "internship": {"icon": "B", "label": "Internship", "color": COLORS["comfortable"]},
    "fellowship": {"icon": "F", "label": "Fellowship", "color": COLORS["urgent"]},
    "competition": {"icon": "C", "label": "Competition", "color": COLORS["critical"]},
    "research": {"icon": "R", "label": "Research", "color": COLORS["moderate"]},
    "exchange": {"icon": "E", "label": "Exchange", "color": COLORS["rolling"]},
    "job": {"icon": "J", "label": "Job", "color": COLORS["text_primary"]},
    "other": {"icon": "?", "label": "Other", "color": COLORS["text_secondary"]},
}


def get_urgency_tier(urgency: str) -> dict:
    """Get urgency tier configuration by name."""
    return URGENCY_TIERS.get(urgency, URGENCY_TIERS["unknown"])


def get_type_icon(type_name: str) -> dict:
    """Get type icon configuration by name."""
    return TYPE_ICONS.get(type_name, TYPE_ICONS["other"])


def get_match_color(score: int) -> str:
    """Get color for match score."""
    if score >= 80:
        return COLORS["match_high"]
    elif score >= 60:
        return COLORS["match_medium"]
    else:
        return COLORS["match_low"]
