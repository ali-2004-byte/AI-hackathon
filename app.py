"""Streamlit entry point for Opportunity Inbox Copilot.

Follows design_system.md specifications:
- Light mode primary
- Indigo brand color (#4F46E5)
- Specific urgency colors for different deadline types
- No emojis in code - use text labels only

Micro-interactions added:
- Premium loading states with animations
- Hover effects on cards and buttons
- Smooth transitions between screens
- Toast notifications for actions
- Progress indicators with animations
- Enhanced micro-copy with tooltips
"""

import streamlit as st
from datetime import date, datetime, timedelta
from typing import List, Optional, Dict, Any
import time
import random
import logging

from src.micro_interactions import (
    get_all_css,
    render_toast_container,
    get_loading_message as get_micro_loading_message,
    get_encouragement,
    get_tooltip,
    MICRO_COPY,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =============================================================================
# DESIGN SYSTEM - Color Constants
# =============================================================================

COLORS = {
    # Primary palette
    "background": "#F8F9FB",
    "surface": "#FFFFFF",
    "brand": "#4F46E5",  # Indigo - primary brand color
    "text_primary": "#1A1D23",
    "text_secondary": "#6B7280",
    "border": "#E5E7EB",

    # Urgency colors (per design_system.md)
    "critical": "#EF4444",       # <= 3 days, bg: #FEF2F2
    "critical_bg": "#FEF2F2",
    "urgent": "#F59E0B",         # 4-7 days, bg: #FFFBEB
    "urgent_bg": "#FFFBEB",
    "moderate": "#84CC16",       # 8-30 days, bg: #F7FEE7
    "moderate_bg": "#F7FEE7",
    "comfortable": "#10B981",    # 31-60 days, bg: #ECFDF5
    "comfortable_bg": "#ECFDF5",
    "rolling": "#6366F1",        # Rolling basis, bg: #EEF2FF
    "rolling_bg": "#EEF2FF",
    "unknown": "#94A3B8",        # Unknown, bg: #F8FAFC
    "unknown_bg": "#F8FAFC",

    # Match score colors
    "match_high": "#10B981",     # 80-100%
    "match_medium": "#F59E0B",   # 60-79%
    "match_low": "#6B7280",      # <60%
}

# Urgency tier mapping - using text labels instead of emojis
URGENCY_TIERS = {
    "critical": {"color": COLORS["critical"], "bg": COLORS["critical_bg"], "label": "CRITICAL", "icon": "●"},
    "urgent": {"color": COLORS["urgent"], "bg": COLORS["urgent_bg"], "label": "URGENT", "icon": "●"},
    "moderate": {"color": COLORS["moderate"], "bg": COLORS["moderate_bg"], "label": "MODERATE", "icon": "●"},
    "comfortable": {"color": COLORS["comfortable"], "bg": COLORS["comfortable_bg"], "label": "COMFORTABLE", "icon": "●"},
    "rolling": {"color": COLORS["rolling"], "bg": COLORS["rolling_bg"], "label": "ROLLING", "icon": "●"},
    "unknown": {"color": COLORS["unknown"], "bg": COLORS["unknown_bg"], "label": "UNKNOWN", "icon": "○"},
}

# Opportunity type icons (text-based)
TYPE_ICONS = {
    "scholarship": "$",
    "internship": "B",
    "fellowship": "F",
    "competition": "C",
    "research": "R",
    "exchange": "E",
    "job": "J",
    "other": "?",
}


# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

def setup_page_config():
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title="Opportunity Inbox Copilot",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    # Premium CSS with animations, micro-interactions, and polish
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

    :root {{
        --brand-primary: {COLORS["brand"]};
        --brand-hover: #4338CA;
        --brand-light: #EEF2FF;
        --animation-smooth: cubic-bezier(0.4, 0, 0.2, 1);
        --animation-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);
        --animation-spring: cubic-bezier(0.175, 0.885, 0.32, 1.275);
        --animation-out-expo: cubic-bezier(0.19, 1, 0.22, 1);
    }}

    /* Base Styles */
    .stApp {{
        background-color: {COLORS["background"]};
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }}
    .main {{
        background-color: {COLORS["background"]};
    }}

    /* Typography Hierarchy - 8px grid system */
    h1 {{
        color: {COLORS["text_primary"]};
        font-family: 'Inter', system-ui, sans-serif;
        font-size: 32px;
        font-weight: 700;
        line-height: 1.2;
        letter-spacing: -0.02em;
        margin-bottom: 8px;
    }}
    h2 {{
        color: {COLORS["text_primary"]};
        font-family: 'Inter', system-ui, sans-serif;
        font-size: 24px;
        font-weight: 600;
        line-height: 1.3;
        margin-bottom: 8px;
    }}
    h3 {{
        color: {COLORS["text_primary"]};
        font-family: 'Inter', system-ui, sans-serif;
        font-size: 18px;
        font-weight: 600;
        line-height: 1.4;
        margin-bottom: 8px;
    }}
    p, span {{
        line-height: 1.6;
    }}

    /* Smooth scroll behavior */
    html {{
        scroll-behavior: smooth;
    }}

    /* Button Styles with Premium Interactions */
    .stButton>button {{
        background-color: {COLORS["brand"]};
        color: white;
        border-radius: 12px;
        border: none;
        padding: 14px 28px;
        font-weight: 600;
        font-size: 15px;
        transition: all 0.25s var(--animation-smooth);
        box-shadow: 0 2px 4px rgba(79, 70, 229, 0.15);
        min-height: 48px;
    }}
    .stButton>button:hover {{
        background-color: #4338CA;
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(79, 70, 229, 0.25);
    }}
    .stButton>button:active {{
        transform: scale(0.98) translateY(0);
        box-shadow: 0 2px 4px rgba(79, 70, 229, 0.15);
        transition: all 0.1s ease;
    }}
    .stButton>button:disabled {{
        background-color: #CBD5E1;
        color: #64748B;
        transform: none;
        box-shadow: none;
        cursor: not-allowed;
    }}
    .stButton>button:focus {{
        outline: none;
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.3);
    }}

    /* Primary button variant */
    .stButton>button[kind="primary"] {{
        background: linear-gradient(135deg, {COLORS["brand"]} 0%, #6366F1 100%);
    }}
    .stButton>button[kind="primary"]:hover {{
        background: linear-gradient(135deg, #4338CA 0%, #4F46E5 100%);
    }}

    /* Input Styles with Focus States */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {{
        border-radius: 10px;
        border: 1.5px solid {COLORS["border"]};
        background-color: {COLORS["surface"]};
        padding: 12px 16px;
        font-size: 15px;
        transition: all 0.2s var(--animation-smooth);
    }}
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {{
        border-color: {COLORS["brand"]};
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
        outline: none;
    }}
    .stTextInput>div>div>input:hover, .stTextArea>div>div>textarea:hover {{
        border-color: #D1D5DB;
    }}

    /* Selectbox Styling */
    .stSelectbox>div>div>div {{
        border-radius: 10px;
        border: 1.5px solid {COLORS["border"]};
        transition: all 0.2s var(--animation-smooth);
    }}
    .stSelectbox>div>div>div:hover {{
        border-color: #D1D5DB;
    }}
    .stSelectbox>div>div>div:focus-within {{
        border-color: {COLORS["brand"]};
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
    }}

    /* Number Input */
    .stNumberInput>div>div>input {{
        border-radius: 10px;
        border: 1.5px solid {COLORS["border"]};
        transition: all 0.2s var(--animation-smooth);
    }}
    .stNumberInput>div>div>input:focus {{
        border-color: {COLORS["brand"]};
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
    }}

    /* Slider Styling */
    .stSlider>div>div {{
        border-radius: 10px;
    }}
    .stSlider [data-testid="stThumbValue"] {{
        font-weight: 600;
        color: {COLORS["brand"]};
    }}

    /* Checkbox and Radio */
    .stCheckbox>label {{
        font-size: 14px;
        font-weight: 500;
        transition: color 0.2s ease;
    }}
    .stCheckbox>label:hover {{
        color: {COLORS["brand"]};
    }}
    .stRadio>div {{
        gap: 16px;
    }}

    /* File Uploader */
    .stFileUploader>div {{
        border-radius: 12px;
        border: 2px dashed {COLORS["border"]};
        transition: all 0.2s var(--animation-smooth);
        background: {COLORS["surface"]};
    }}
    .stFileUploader>div:hover {{
        border-color: {COLORS["brand"]};
        background: var(--brand-light);
    }}
    .stFileUploader>div:focus-within {{
        border-color: {COLORS["brand"]};
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
    }}

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
    }}
    .stTabs [data-baseweb="tab"] {{
        border-radius: 10px 10px 0 0;
        padding: 12px 20px;
        font-weight: 500;
        transition: all 0.2s var(--animation-smooth);
    }}
    .stTabs [data-baseweb="tab"]:hover {{
        background-color: rgba(79, 70, 229, 0.05);
    }}
    .stTabs [aria-selected="true"] {{
        background-color: {COLORS["brand"]} !important;
        color: white !important;
        font-weight: 600;
    }}

    /* Progress Bar Animation */
    .stProgress>div>div>div {{
        background: linear-gradient(90deg, {COLORS["brand"]} 0%, #6366F1 50%, {COLORS["brand"]} 100%);
        background-size: 200% 100%;
        animation: shimmer 2s infinite;
        border-radius: 4px;
    }}
    @keyframes shimmer {{
        0% {{ background-position: -200% 0; }}
        100% {{ background-position: 200% 0; }}
    }}

    /* Custom Card Styling with Hover Effects */
    .opportunity-card {{
        background-color: {COLORS["surface"]};
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.04);
        margin: 16px 0;
        overflow: hidden;
        transition: all 0.3s var(--animation-smooth);
        border: 1px solid transparent;
    }}
    .opportunity-card:hover {{
        transform: translateY(-3px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.12), 0 4px 8px rgba(0,0,0,0.08);
        border-color: rgba(79, 70, 229, 0.15);
    }}
    .opportunity-card:active {{
        transform: scale(0.99) translateY(-1px);
    }}

    /* Left Accent Bar with Pulse Animation */
    .left-accent {{
        width: 4px;
        min-height: 100%;
        border-radius: 2px;
    }}
    .left-accent.critical {{
        animation: pulse-critical 2s infinite;
    }}
    .left-accent.urgent {{
        animation: pulse-urgent 2s infinite;
    }}
    @keyframes pulse-critical {{
        0%, 100% {{ opacity: 1; box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }}
        50% {{ opacity: 0.9; box-shadow: 0 0 0 6px rgba(239, 68, 68, 0); }}
    }}
    @keyframes pulse-urgent {{
        0%, 100% {{ opacity: 1; box-shadow: 0 0 0 0 rgba(245, 158, 11, 0.4); }}
        50% {{ opacity: 0.9; box-shadow: 0 0 0 4px rgba(245, 158, 11, 0); }}
    }}

    /* Deadline Monospace Styling */
    .deadline-mono {{
        font-family: 'JetBrains Mono', 'Courier New', monospace;
        font-size: 14px;
        font-weight: 600;
        letter-spacing: -0.01em;
    }}

    /* Evidence Quote Styling */
    .evidence-quote {{
        border-left: 3px solid {COLORS["border"]};
        padding-left: 16px;
        margin: 12px 0;
        color: {COLORS["text_secondary"]};
        font-style: italic;
        font-size: 14px;
        line-height: 1.6;
    }}

    /* Summary Bar Styling */
    .summary-box {{
        background-color: {COLORS["surface"]};
        padding: 20px 16px;
        border-radius: 12px;
        text-align: center;
        border-left: 4px solid;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        transition: all 0.25s var(--animation-smooth);
    }}
    .summary-box:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    }}
    .summary-count {{
        font-size: 28px;
        font-weight: 700;
        letter-spacing: -0.02em;
    }}
    .summary-label {{
        font-size: 11px;
        color: {COLORS["text_secondary"]};
        text-transform: uppercase;
        letter-spacing: 0.8px;
        font-weight: 600;
        margin-top: 4px;
    }}

    /* Loading Spinner Animation */
    @keyframes spin {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}
    .spinner {{
        width: 40px;
        height: 40px;
        border: 3px solid rgba(79, 70, 229, 0.1);
        border-top: 3px solid {COLORS["brand"]};
        border-radius: 50%;
        animation: spin 0.8s linear infinite;
    }}

    /* Skeleton Loading Animation */
    @keyframes shimmer-skeleton {{
        0% {{ background-position: -200% 0; }}
        100% {{ background-position: 200% 0; }}
    }}
    .skeleton {{
        background: linear-gradient(90deg, #E5E7EB 0%, #F3F4F6 50%, #E5E7EB 100%);
        background-size: 200% 100%;
        animation: shimmer-skeleton 1.5s infinite;
        border-radius: 8px;
    }}

    /* Animated Dots for Loading Text */
    @keyframes dots {{
        0%, 20% {{ content: '.'; }}
        40% {{ content: '..'; }}
        60%, 100% {{ content: '...'; }}
    }}
    .loading-dots::after {{
        content: '.';
        animation: dots 1.5s infinite;
    }}

    /* Tag/Chips Styling */
    .skill-chip {{
        display: inline-flex;
        align-items: center;
        padding: 6px 14px;
        background: var(--brand-light);
        color: {COLORS["brand"]};
        border-radius: 20px;
        font-size: 13px;
        font-weight: 500;
        margin: 4px;
        transition: all 0.2s var(--animation-smooth);
        cursor: pointer;
    }}
    .skill-chip:hover {{
        background: {COLORS["brand"]};
        color: white;
        transform: scale(1.05);
    }}
    .skill-chip.selected {{
        background: {COLORS["brand"]};
        color: white;
    }}

    /* Match Score Ring */
    .match-ring {{
        position: relative;
        display: inline-flex;
        align-items: center;
        justify-content: center;
    }}
    .match-ring svg {{
        transform: rotate(-90deg);
    }}
    .match-ring-circle {{
        fill: none;
        stroke-width: 4;
        stroke-linecap: round;
        transition: stroke-dashoffset 1s var(--animation-smooth);
    }}
    .match-ring-bg {{
        stroke: #E5E7EB;
    }}
    .match-ring-fill {{
        stroke: {COLORS["match_high"]};
        stroke-dasharray: 100;
        animation: fillRing 1s var(--animation-smooth) forwards;
    }}
    @keyframes fillRing {{
        from {{ stroke-dashoffset: 100; }}
        to {{ stroke-dashoffset: var(--offset); }}
    }}

    /* Expander Styling */
    .streamlit-expanderHeader {{
        font-weight: 500;
        color: {COLORS["text_secondary"]};
        transition: color 0.2s ease;
    }}
    .streamlit-expanderHeader:hover {{
        color: {COLORS["brand"]};
    }}

    /* Success/Info/Warning Messages */
    .stSuccess, .stInfo, .stWarning, .stError {{
        border-radius: 12px;
        padding: 16px;
        font-weight: 500;
        animation: slideIn 0.3s var(--animation-smooth);
    }}
    @keyframes slideIn {{
        from {{
            opacity: 0;
            transform: translateY(-10px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}

    /* Responsive Adjustments */
    @media (max-width: 768px) {{
        h1 {{ font-size: 24px; }}
        h2 {{ font-size: 20px; }}
        h3 {{ font-size: 16px; }}
        .stButton>button {{
            width: 100%;
            min-height: 52px;
            font-size: 16px;
        }}
        .summary-box {{
            padding: 16px 12px;
        }}
        .summary-count {{
            font-size: 22px;
        }}
    }}

    /* Confetti Animation */
    @keyframes confetti-fall {{
        0% {{ transform: translateY(-100%) rotate(0deg); opacity: 1; }}
        100% {{ transform: translateY(100vh) rotate(720deg); opacity: 0; }}
    }}
    .confetti {{
        position: fixed;
        width: 10px;
        height: 10px;
        top: -10px;
        animation: confetti-fall 3s linear forwards;
        z-index: 9999;
        pointer-events: none;
    }}

    /* Checkmark Animation */
    @keyframes checkmark {{
        0% {{ transform: scale(0); opacity: 0; }}
        50% {{ transform: scale(1.2); }}
        100% {{ transform: scale(1); opacity: 1; }}
    }}
    .checkmark-animate {{
        animation: checkmark 0.4s var(--animation-bounce) forwards;
    }}

    /* Fade In Animation */
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    .fade-in {{
        animation: fadeIn 0.5s var(--animation-smooth) forwards;
    }}

    /* Staggered fade in for lists */
    .fade-in-delay-1 {{ animation-delay: 0.1s; opacity: 0; }}
    .fade-in-delay-2 {{ animation-delay: 0.2s; opacity: 0; }}
    .fade-in-delay-3 {{ animation-delay: 0.3s; opacity: 0; }}
    .fade-in-delay-4 {{ animation-delay: 0.4s; opacity: 0; }}
    .fade-in-delay-5 {{ animation-delay: 0.5s; opacity: 0; }}
    .fade-in-delay-6 {{ animation-delay: 0.6s; opacity: 0; }}

    /* Enhanced Button Press Animation */
    @keyframes buttonPress {{
        0% {{ transform: scale(1); }}
        50% {{ transform: scale(0.97); }}
        100% {{ transform: scale(1); }}
    }}
    .button-press {{
        animation: buttonPress 0.15s var(--animation-smooth) forwards;
    }}

    /* Tooltip Styles */
    .tooltip-container {{
        position: relative;
        display: inline-block;
    }}
    .tooltip-container:hover .tooltip-text {{
        opacity: 1;
        visibility: visible;
        transform: translateY(0);
    }}
    .tooltip-text {{
        position: absolute;
        bottom: 100%;
        left: 50%;
        transform: translateX(-50%) translateY(-8px);
        padding: 8px 12px;
        background: #1A1D23;
        color: white;
        font-size: 13px;
        font-weight: 500;
        border-radius: 8px;
        white-space: nowrap;
        opacity: 0;
        visibility: hidden;
        transition: all 0.2s var(--animation-smooth);
        z-index: 1000;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }}
    .tooltip-text::after {{
        content: '';
        position: absolute;
        top: 100%;
        left: 50%;
        transform: translateX(-50%);
        border: 6px solid transparent;
        border-top-color: #1A1D23;
    }}

    /* Enhanced Card Hover with Glow */
    .opportunity-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 100%;
        background: linear-gradient(135deg, rgba(79, 70, 229, 0.03) 0%, transparent 50%);
        opacity: 0;
        transition: opacity 0.3s ease;
        pointer-events: none;
    }}
    .opportunity-card:hover::before {{
        opacity: 1;
    }}

    /* Counter Animation */
    @keyframes counterUp {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    .counter-animate {{
        animation: counterUp 0.6s var(--animation-out-expo) forwards;
    }}

    /* Toast Container */
    .toast-container {{
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 10000;
        display: flex;
        flex-direction: column;
        gap: 12px;
        pointer-events: none;
    }}
    .toast {{
        min-width: 300px;
        max-width: 450px;
        padding: 16px 20px;
        border-radius: 12px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 14px;
        font-weight: 500;
        animation: slideInRight 0.3s var(--animation-out-expo) forwards;
        backdrop-filter: blur(8px);
        pointer-events: auto;
    }}
    .toast-exit {{
        animation: fadeOut 0.3s var(--animation-smooth) forwards;
    }}
    .toast-success {{
        background: rgba(255, 255, 255, 0.95);
        border-left: 4px solid #10B981;
        color: #065F46;
    }}
    .toast-error {{
        background: rgba(255, 255, 255, 0.95);
        border-left: 4px solid #EF4444;
        color: #991B1B;
    }}
    .toast-warning {{
        background: rgba(255, 255, 255, 0.95);
        border-left: 4px solid #F59E0B;
        color: #92400E;
    }}
    .toast-info {{
        background: rgba(255, 255, 255, 0.95);
        border-left: 4px solid #4F46E5;
        color: #312E81;
    }}
    .toast-icon {{
        flex-shrink: 0;
        width: 24px;
        height: 24px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
    }}
    .toast-success .toast-icon {{ background: #D1FAE5; color: #059669; }}
    .toast-error .toast-icon {{ background: #FEE2E2; color: #DC2626; }}
    .toast-warning .toast-icon {{ background: #FEF3C7; color: #D97706; }}
    .toast-info .toast-icon {{ background: #EEF2FF; color: #4F46E5; }}
    .toast-message {{ flex: 1; line-height: 1.5; }}

    @keyframes slideInRight {{
        from {{ opacity: 0; transform: translateX(30px); }}
        to {{ opacity: 1; transform: translateX(0); }}
    }}

    /* Skill Chip Enhanced */
    .skill-chip {{
        display: inline-flex;
        align-items: center;
        padding: 6px 14px;
        background: var(--brand-light);
        color: {COLORS["brand"]};
        border-radius: 20px;
        font-size: 13px;
        font-weight: 500;
        margin: 4px;
        transition: all 0.2s var(--animation-smooth);
        cursor: pointer;
        user-select: none;
    }}
    .skill-chip:hover {{
        background: {COLORS["brand"]};
        color: white;
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.2);
    }}
    .skill-chip.selected {{
        background: {COLORS["brand"]};
        color: white;
    }}

    /* Email Counter Badge */
    .email-counter {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-width: 24px;
        height: 24px;
        padding: 0 8px;
        background: {COLORS["brand"]};
        color: white;
        border-radius: 12px;
        font-size: 13px;
        font-weight: 600;
        transition: all 0.3s var(--animation-spring);
    }}
    .email-counter:hover {{
        transform: scale(1.1);
    }}
    </style>

    <!-- Toast Container -->
    <div class="toast-container" id="toast-container"></div>

    <!-- JavaScript for Toast Notifications and Animations -->
    <script>
    function showToast(message, type = 'info', duration = 3000) {{
        const container = document.getElementById('toast-container');
        const toast = document.createElement('div');
        toast.className = `toast toast-${{type}}`;

        const icons = {{
            success: '✓',
            error: '✕',
            warning: '!',
            info: 'i'
        }};

        toast.innerHTML = `
            <div class="toast-icon">${{icons[type] || icons.info}}</div>
            <div class="toast-message">${{message}}</div>
        `;

        container.appendChild(toast);

        setTimeout(() => {{
            toast.classList.add('toast-exit');
            setTimeout(() => toast.remove(), 300);
        }}, duration);
    }}

    function celebrate() {{
        const colors = ['#4F46E5', '#10B981', '#F59E0B', '#EF4444', '#6366F1'];
        for (let i = 0; i < 50; i++) {{
            const confetti = document.createElement('div');
            confetti.className = 'confetti';
            confetti.style.left = Math.random() * 100 + 'vw';
            confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
            confetti.style.animationDelay = Math.random() * 2 + 's';
            confetti.style.borderRadius = Math.random() > 0.5 ? '50%' : '0';
            document.body.appendChild(confetti);
            setTimeout(() => confetti.remove(), 3000);
        }}
    }}

    function animateValue(element, start, end, duration) {{
        const startTime = performance.now();
        function update(currentTime) {{
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const easeProgress = 1 - Math.pow(1 - progress, 3);
            element.textContent = Math.floor(start + (end - start) * easeProgress);
            if (progress < 1) requestAnimationFrame(update);
        }}
        requestAnimationFrame(update);
    }}

    // Animate counter on page load
    document.querySelectorAll('[data-animate-counter]').forEach(el => {{
        const end = parseInt(el.getAttribute('data-animate-counter'));
        animateValue(el, 0, end, 1000);
    }});
    </script>
    """, unsafe_allow_html=True)

    <!-- JavaScript for Confetti and Interactions -->
    <script>
    function celebrate() {{
        const colors = ['#4F46E5', '#10B981', '#F59E0B', '#EF4444', '#6366F1'];
        for (let i = 0; i < 50; i++) {{
            const confetti = document.createElement('div');
            confetti.className = 'confetti';
            confetti.style.left = Math.random() * 100 + 'vw';
            confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
            confetti.style.animationDelay = Math.random() * 2 + 's';
            confetti.style.borderRadius = Math.random() > 0.5 ? '50%' : '0';
            document.body.appendChild(confetti);
            setTimeout(() => confetti.remove(), 3000);
        }}
    }}

    function animateValue(element, start, end, duration) {{
        const startTime = performance.now();
        function update(currentTime) {{
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const easeProgress = 1 - Math.pow(1 - progress, 3);
            element.textContent = Math.floor(start + (end - start) * easeProgress);
            if (progress < 1) requestAnimationFrame(update);
        }}
        requestAnimationFrame(update);
    }}
    </script>
    """, unsafe_allow_html=True)


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def parse_emails_from_text(text: str) -> List[str]:
    """Parse emails from text using --- delimiter."""
    if not text:
        return []
    emails = [e.strip() for e in text.split("---") if e.strip()]
    return emails


def get_match_color(score: int) -> str:
    """Get color based on match score."""
    if score >= 80:
        return COLORS["match_high"]
    elif score >= 60:
        return COLORS["match_medium"]
    else:
        return COLORS["match_low"]


def format_deadline(deadline_text: str, urgency: str) -> str:
    """Format deadline text with monospace styling."""
    return f'<span class="deadline-mono" style="color: {URGENCY_TIERS[urgency]["color"]};">{deadline_text}</span>'


def show_toast(message: str, toast_type: str = "info"):
    """Display a toast notification using JavaScript."""
    st.markdown(f"""
    <script>
    showToast("{message}", "{toast_type}", 3000);
    </script>
    """, unsafe_allow_html=True)


# =============================================================================
# SCREEN 1: ONBOARDING / INPUT
# =============================================================================

def render_input_screen():
    """Render the profile and email input screen (STEP 1 of 2)."""
    # Header with enhanced styling
    col_header1, col_header2, col_header3 = st.columns([1, 2, 1])
    with col_header2:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 24px;" class="fade-in">
            <h1 style="margin-bottom: 8px;">Opportunity Inbox Copilot</h1>
            <p style="color: #6B7280; font-size: 16px;">
                Turn email chaos into your personal opportunity edge
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Progress indicator with enhanced styling
    st.markdown("""
    <div style="margin-bottom: 8px;">
        <span style="font-size: 12px; font-weight: 600; color: #4F46E5; text-transform: uppercase; letter-spacing: 0.5px;">
            Step 1 of 2
        </span>
    </div>
    """, unsafe_allow_html=True)
    st.progress(50)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("""
        <div style="margin-bottom: 16px;">
            <h2 style="font-size: 20px; margin-bottom: 4px;">Your Profile</h2>
            <p style="color: #6B7280; font-size: 14px;">Tell us about yourself to personalize your rankings</p>
        </div>
        """, unsafe_allow_html=True)

        with st.container():
            # Degree select
            degree = st.selectbox(
                "Degree/Program",
                ["Computer Science", "Electrical Engineering", "Mechanical Engineering",
                 "Data Science", "Business", "Biology", "Physics", "Mathematics", "Other"],
                key="degree"
            )

            # Year slider
            year = st.slider("Year/Semester", 1, 6, 3, key="year")

            # CGPA input
            cgpa = st.number_input(
                "CGPA",
                min_value=0.0,
                max_value=4.0,
                value=3.5,
                step=0.1,
                format="%.2f",
                key="cgpa"
            )

            # Skills multiselect with tag-style
            skill_options = [
                "Python", "JavaScript", "Java", "C++", "Machine Learning",
                "Data Analysis", "Web Development", "Mobile Development",
                "Cloud Computing", "AI/Deep Learning", "Research",
                "Leadership", "Communication", "Design", "Project Management"
            ]
            skills = st.multiselect(
                "Skills & Interests (select multiple)",
                options=skill_options,
                default=["Python", "Machine Learning"],
                key="skills"
            )

            st.markdown("")
            st.markdown("**I'm looking for:**")

            # Opportunity types - 3 columns of checkboxes
            col_types1, col_types2, col_types3 = st.columns(3)
            with col_types1:
                type_scholarship = st.checkbox("Scholarship", value=True, key="type_scholarship")
                type_internship = st.checkbox("Internship", value=True, key="type_internship")
            with col_types2:
                type_fellowship = st.checkbox("Fellowship", key="type_fellowship")
                type_competition = st.checkbox("Competition", key="type_competition")
            with col_types3:
                type_research = st.checkbox("Research", key="type_research")
                type_exchange = st.checkbox("Exchange", key="type_exchange")

            # Collect selected types
            selected_types = []
            if type_scholarship:
                selected_types.append("Scholarship")
            if type_internship:
                selected_types.append("Internship")
            if type_fellowship:
                selected_types.append("Fellowship")
            if type_competition:
                selected_types.append("Competition")
            if type_research:
                selected_types.append("Research")
            if type_exchange:
                selected_types.append("Exchange")

            st.markdown("")
            financial_need = st.radio(
                "Financial Need",
                ["No", "Yes"],
                horizontal=True,
                key="financial_need"
            )

            location_pref = st.selectbox(
                "Location Preference",
                ["Open to Remote + Onsite", "Remote Only", "Onsite Only", "Hybrid"],
                key="location_pref"
            )

    with col2:
        st.markdown("""
        <div style="margin-bottom: 16px;">
            <h2 style="font-size: 20px; margin-bottom: 4px;">Paste Your Emails</h2>
            <p style="color: #6B7280; font-size: 14px;">Paste 5-15 emails separated by '---' or upload files</p>
        </div>
        """, unsafe_allow_html=True)

        email_input = st.text_area(
            "Email content",
            height=350,
            placeholder="""Paste your opportunity emails here...

---

Next email goes here...

---

And so on...""",
            key="email_input",
            help="Paste emails from scholarship portals, internship listings, or opportunity newsletters"
        )

        # Email count with animated counter
        emails = parse_emails_from_text(email_input)
        email_count = len(emails)

        # Enhanced email counter display
        counter_col1, counter_col2 = st.columns([1, 2])
        with counter_col1:
            if email_count > 0:
                st.markdown(f"""
                <div class="fade-in">
                    <span style="font-size: 14px; color: #6B7280;">Emails detected: </span>
                    <span class="email-counter counter-animate" data-animate-counter="{email_count}">{email_count}</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown('<span style="font-size: 14px; color: #9CA3AF;">Emails detected: 0</span>', unsafe_allow_html=True)

        with counter_col2:
            if email_count >= 5:
                st.markdown("""
                <div class="fade-in">
                    <span style="color: #10B981; font-size: 13px; font-weight: 500;">✓ Ready to analyze</span>
                </div>
                """, unsafe_allow_html=True)
            elif email_count > 0:
                st.markdown(f"""
                <div class="fade-in">
                    <span style="color: #F59E0B; font-size: 13px;">⚠ {5 - email_count} more needed</span>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("")
        st.markdown('<span style="font-size: 14px; font-weight: 600; color: #6B7280; margin-bottom: 8px;">Or upload files:</span>', unsafe_allow_html=True)
        uploaded_files = st.file_uploader(
            "Upload .txt or .eml files",
            type=["txt", "eml"],
            accept_multiple_files=True,
            key="file_upload",
            help="Upload exported email files or text documents containing opportunity information"
        )

        # Process uploaded files
        if uploaded_files:
            file_emails = []
            for file in uploaded_files:
                content = file.read().decode("utf-8", errors="ignore")
                file_emails.extend(parse_emails_from_text(content))
            if file_emails:
                st.info(f"Loaded {len(file_emails)} additional emails from files")
                emails.extend(file_emails)
                email_count = len(emails)

    # Analyze button with enhanced styling
    st.markdown("")
    st.markdown("---")

    analyze_disabled = email_count < 5

    # Button container with tooltip
    btn_col1, btn_col2 = st.columns([3, 1])
    with btn_col1:
        analyze_clicked = st.button(
            "Analyze My Opportunities" if analyze_disabled else "Analyze My Opportunities →",
            disabled=analyze_disabled,
            use_container_width=True,
            key="analyze_btn",
            help="AI will scan your emails and find the best opportunities for your profile" if not analyze_disabled else "Please enter at least 5 emails to continue"
        )

    with btn_col2:
        st.markdown("")
        st.markdown("")
        st.markdown(f"""
        <div style="text-align: right; font-size: 12px; color: #9CA3AF; margin-top: 14px;">
            {MICRO_COPY["status"]["min_required"] if email_count < 5 else MICRO_COPY["status"]["ready"]}
        </div>
        """, unsafe_allow_html=True)

    if analyze_clicked:
        # Show toast notification
        show_toast("Starting analysis...", "info")

        # Store data in session state
        st.session_state["emails"] = emails
        st.session_state["profile"] = {
            "degree": degree,
            "year": year,
            "cgpa": cgpa,
            "skills": skills,
            "preferred_types": selected_types,
            "financial_need": financial_need == "Yes",
            "location_pref": location_pref,
        }
        st.session_state["screen"] = "processing"
        st.rerun()


# =============================================================================
# SCREEN 2: PROCESSING STATE - Premium Loading Experience
# =============================================================================

def get_loading_message(step: int) -> str:
    """Get encouraging loading messages from micro_interactions module."""
    return get_micro_loading_message(step)

def render_skeleton_cards(count: int = 3):
    """Render skeleton loading cards with staggered animation."""
    for i in range(count):
        st.markdown(f"""
        <div class="premium-card fade-in-delay-{min(i + 1, 6)}" style="background: {COLORS['surface']}; border-radius: 12px; padding: 24px; margin: 16px 0;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.08);">
            <div class="skeleton" style="height: 24px; width: 60%; margin-bottom: 16px;"></div>
            <div class="skeleton" style="height: 16px; width: 40%; margin-bottom: 12px;"></div>
            <div class="skeleton" style="height: 16px; width: 80%; margin-bottom: 8px;"></div>
            <div style="display: flex; gap: 12px; margin-top: 16px;">
                <div class="skeleton" style="height: 32px; width: 120px; border-radius: 8px;"></div>
                <div class="skeleton" style="height: 32px; width: 100px; border-radius: 8px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_processing_screen():
    """Render the premium processing/loading screen."""
    # Center content
    col1, col2, col3 = st.columns([1, 3, 1])

    with col2:
        st.markdown("<div style='text-align: center; padding-top: 20px;' class='fade-in'>", unsafe_allow_html=True)

        # Animated spinner with glow effect
        st.markdown("""
        <div style="display: flex; justify-content: center; margin-bottom: 32px;">
            <div class="spinner glow"></div>
        </div>
        """, unsafe_allow_html=True)

        # Dynamic title with loading dots
        current_step = st.session_state.get("processing_step", 0)
        loading_text = get_loading_message(current_step)
        st.markdown(f"""
        <h2 style="text-align: center; margin-bottom: 8px; font-size: 22px;">{loading_text}<span class="loading-dots"></span></h2>
        <p style="text-align: center; color: {COLORS['text_secondary']}; font-size: 15px;">
            This usually takes 10-20 seconds
        </p>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # Initialize processing state
        if "processing_step" not in st.session_state:
            st.session_state["processing_step"] = 0
            st.session_state["processing_complete"] = False
            st.session_state["show_confetti"] = False

        # Get email count
        email_count = len(st.session_state.get("emails", []))
        opportunity_count = max(3, int(email_count * 0.6))  # Simulated

        # Progress bar with percentage
        progress = min((st.session_state["processing_step"] + 1) * 25, 100)
        progress_col1, progress_col2 = st.columns([6, 1])
        with progress_col1:
            st.progress(progress / 100)
        with progress_col2:
            st.markdown(f"<p style='font-weight: 600; color: {COLORS['brand']};'>{progress}%</p>", unsafe_allow_html=True)

        # Processing steps with animated status indicators
        st.markdown("<div style='margin-top: 24px;'>", unsafe_allow_html=True)

        steps = [
            (f"Detected {email_count} emails", 0),
            (f"Classified {opportunity_count} opportunities", 1),
            ("Extracted deadlines & requirements", 2),
            ("Scored against your profile", 3),
        ]

        for i, (step_text, step_idx) in enumerate(steps):
            current_step = st.session_state["processing_step"]

            if i < current_step:
                # Completed step with animated checkmark
                st.markdown(f"""
                <div style="display: flex; align-items: center; gap: 12px; padding: 12px;
                            background: {COLORS['comfortable_bg']}; border-radius: 8px; margin: 8px 0;
                            animation: slideIn 0.3s ease;">
                    <div style="color: {COLORS['comfortable']}; font-size: 18px;" class="checkmark-animate">✓</div>
                    <span style="color: {COLORS['comfortable']}; font-weight: 500;">{step_text}</span>
                </div>
                """, unsafe_allow_html=True)
            elif i == current_step:
                # Current step with pulsing indicator
                st.markdown(f"""
                <div style="display: flex; align-items: center; gap: 12px; padding: 12px;
                            background: {COLORS['rolling_bg']}; border-radius: 8px; margin: 8px 0;
                            border: 1px solid rgba(79, 70, 229, 0.2);">
                    <div style="width: 18px; height: 18px; border: 2px solid {COLORS['brand']};
                                border-top-color: transparent; border-radius: 50%;
                                animation: spin 0.8s linear infinite;"></div>
                    <span style="color: {COLORS['brand']}; font-weight: 600;">{step_text}</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Future step
                st.markdown(f"""
                <div style="display: flex; align-items: center; gap: 12px; padding: 12px;
                            border-radius: 8px; margin: 8px 0; opacity: 0.5;">
                    <div style="width: 18px; height: 18px; border: 2px solid {COLORS['text_secondary']};
                                border-radius: 50%;"></div>
                    <span style="color: {COLORS['text_secondary']};">{step_text}</span>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # Skeleton cards preview
        if current_step >= 2:
            st.markdown("<div style='margin-top: 32px; opacity: 0.6;'>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: {0}; font-size: 14px; margin-bottom: 16px;'>Preparing your results...</p>".format(COLORS['text_secondary']), unsafe_allow_html=True)
            render_skeleton_cards(2)
            st.markdown("</div>", unsafe_allow_html=True)

        # Tips card with encouraging message from micro_interactions module
        if current_step < 3:
            tip = get_encouragement()
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {COLORS['brand']} 0%, #6366F1 100%); color: white; padding: 16px 20px;
                        border-radius: 12px; margin-top: 32px; text-align: center;
                        animation: fadeIn 0.5s ease; box-shadow: 0 4px 16px rgba(79, 70, 229, 0.2);">
                <span style="font-size: 20px; margin-right: 8px;">&#128161;</span>
                <span style="font-weight: 500;">{tip}</span>
            </div>
            """, unsafe_allow_html=True)

    # Simulate processing with auto-advance
    if st.session_state["processing_step"] < 4:
        time.sleep(0.7)  # Slightly faster for better UX
        st.session_state["processing_step"] += 1
        st.rerun()
    else:
        # Processing complete - show confetti and redirect
        if not st.session_state.get("show_confetti", False):
            st.session_state["show_confetti"] = True
            st.balloons()  # Streamlit's built-in celebration
            st.toast("Analysis complete! Found 8 opportunities for you", icon="✅")

        time.sleep(1.0)
        st.session_state["processing_complete"] = True
        st.session_state["screen"] = "results"
        st.rerun()


# =============================================================================
# SCREEN 3: RESULTS DASHBOARD
# =============================================================================

# Sample data for demonstration
SAMPLE_OPPORTUNITIES = [
    {
        "rank": 1,
        "title": "Google Generation Scholarship",
        "type": "scholarship",
        "type_label": "Scholarship",
        "urgency": "critical",
        "match": 94,
        "deadline": "March 15, 2025 (2 days left)",
        "location": "Remote",
        "award": "$10,000 + Mentorship",
        "why": "Highest urgency + strong profile match. Your CGPA (3.8) meets threshold. CS degree matches requirement. Financial need flag aligns. Deadline in 2 days - act today.",
        "evidence": "Applications after midnight will not be reviewed regardless of timezone.",
        "application_link": "https://scholarships.google.com",
        "documents": ["Updated Resume/CV", "Unofficial Transcript", "1 Recommendation Letter", "500-word Personal Statement", "Proof of enrollment"],
        "next_steps": ["Visit application portal", "Create account or log in", "Complete Section A (Personal Info)", "Upload transcript and resume", "Write/paste personal statement", "Submit before 11:59 PM on March 15"],
    },
    {
        "rank": 2,
        "title": "Microsoft Summer Internship",
        "type": "internship",
        "type_label": "Internship",
        "urgency": "rolling",
        "match": 89,
        "deadline": "Rolling basis - Apply ASAP",
        "location": "Redmond, WA (Hybrid)",
        "award": "$8,000/month + Housing",
        "why": "Strong skills match (Python, ML). Rolling deadline means high competition. Your profile matches 89% of requirements.",
        "evidence": "We review applications on a rolling basis and positions fill quickly.",
        "application_link": "https://careers.microsoft.com",
        "documents": ["Resume/CV", "Unofficial Transcript", "Cover Letter"],
        "next_steps": ["Visit careers portal", "Search for 'Summer Intern 2025'", "Complete online application", "Upload required documents"],
    },
    {
        "rank": 3,
        "title": "MIT AI Research Fellowship",
        "type": "fellowship",
        "type_label": "Fellowship",
        "urgency": "urgent",
        "match": 87,
        "deadline": "January 15, 2025 (7 days left)",
        "location": "Cambridge, MA",
        "award": "$45,000/year + Tuition",
        "why": "Excellent research fit. Early application encouraged for priority consideration. Strong ML background alignment.",
        "evidence": "Priority consideration given to applications received by January 15.",
        "application_link": "https://mit.edu/ai-fellowship",
        "documents": ["CV/Resume", "Research Statement", "2 Recommendation Letters", "Writing Sample"],
        "next_steps": ["Review research areas", "Contact potential advisor", "Prepare research proposal", "Submit application"],
    },
    {
        "rank": 4,
        "title": "NSF REU Program",
        "type": "research",
        "type_label": "Research",
        "urgency": "moderate",
        "match": 82,
        "deadline": "February 1, 2025 (18 days left)",
        "location": "Various US Universities",
        "award": "$6,000 stipend + Housing",
        "why": "Good match for your research interests. Multiple locations available. Strong alignment with your CS background.",
        "evidence": "REU sites are distributed across the country with various research focuses.",
        "application_link": "https://nsf.gov/reu",
        "documents": ["Transcript", "Personal Statement", "2 Recommendations"],
        "next_steps": ["Browse REU sites", "Identify 3-5 programs of interest", "Contact program coordinators", "Submit applications"],
    },
    {
        "rank": 5,
        "title": "Stanford Summer Exchange",
        "type": "exchange",
        "type_label": "Exchange",
        "urgency": "comfortable",
        "match": 76,
        "deadline": "March 30, 2025 (47 days left)",
        "location": "Stanford, CA",
        "award": "Full tuition coverage",
        "why": "Comfortable deadline allows time for preparation. Exchange experience valuable for your profile. Good academic fit.",
        "evidence": "Summer exchange programs offer immersive academic and cultural experiences.",
        "application_link": "https://stanford.edu/summer-exchange",
        "documents": ["Academic Transcript", "Letter of Motivation", "Language Proficiency Test"],
        "next_steps": ["Research program options", "Prepare application materials", "Submit by deadline"],
    },
]


def render_summary_bar():
    """Render the summary bar with urgency counts."""
    st.markdown("### Summary")

    # Calculate counts from sample data
    urgency_counts = {
        "critical": 1,
        "urgent": 1,
        "moderate": 1,
        "comfortable": 1,
        "rolling": 1,
    }

    summary_cols = st.columns(5)
    summary_data = [
        ("Critical", "1", "critical", COLORS["critical"]),
        ("Urgent", "1", "urgent", COLORS["urgent"]),
        ("Moderate", "1", "moderate", COLORS["moderate"]),
        ("Comfortable", "1", "comfortable", COLORS["comfortable"]),
        ("Rolling", "1", "rolling", COLORS["rolling"]),
    ]

    for col, (label, count, urgency_key, color) in zip(summary_cols, summary_data):
        with col:
            st.markdown(f"""
            <div class="summary-box" style="border-left-color: {color};">
                <div class="summary-count" style="color: {color};">{count}</div>
                <div class="summary-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("")


def render_filter_bar():
    """Render the filter bar with tabs and sort dropdown."""
    filter_col1, filter_col2, filter_col3 = st.columns([2, 1, 1])

    with filter_col1:
        # Filter tabs using selectbox styled as tabs
        filter_type = st.selectbox(
            "Filter by type",
            ["All", "Scholarship", "Internship", "Fellowship", "Competition", "Research", "Exchange"],
            key="filter_type",
            label_visibility="collapsed"
        )

    with filter_col2:
        sort_by = st.selectbox(
            "Sort by",
            ["Rank", "Deadline", "Match Score"],
            key="sort_by"
        )

    st.markdown("---")

    return filter_type, sort_by


def render_opportunity_card(opp: Dict[str, Any], expanded: bool = False):
    """Render a single opportunity card."""
    urgency_info = URGENCY_TIERS.get(opp["urgency"], URGENCY_TIERS["unknown"])
    match_color = get_match_color(opp["match"])
    type_icon = TYPE_ICONS.get(opp["type"], "?")

    # Main card container
    with st.container():
        # Card with left accent bar using columns
        col_accent, col_content = st.columns([0.01, 0.99])

        with col_accent:
            st.markdown(f"""
            <div style="background-color: {urgency_info['color']}; width: 4px; height: 100%; min-height: 200px; border-radius: 2px;"></div>
            """, unsafe_allow_html=True)

        with col_content:
            # Card header: Rank, Urgency badge, Match score
            header_col1, header_col2, header_col3 = st.columns([0.15, 0.5, 0.35])

            with header_col1:
                st.markdown(f"**#{opp['rank']}**")

            with header_col2:
                st.markdown(f"""
                <span style="background-color: {urgency_info['bg']}; color: {urgency_info['color']}; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: 600;">
                    {urgency_info['icon']} {urgency_info['label']}
                </span>
                """, unsafe_allow_html=True)

            with header_col3:
                st.markdown(f"""
                <div style="text-align: right;">
                    <span style="background-color: {match_color}; color: white; padding: 4px 12px; border-radius: 20px; font-size: 14px; font-weight: 600;">
                        {opp['match']}% Match
                    </span>
                </div>
                """, unsafe_allow_html=True)

            # Title
            st.markdown(f"### {opp['title']}")

            # Metadata row
            st.markdown(f"""
            <div style="color: {COLORS['text_secondary']}; font-size: 14px; margin-bottom: 10px;">
                <strong>[{type_icon}] {opp['type_label']}</strong> |
                {opp['location']} |
                {opp['award']}
            </div>
            """, unsafe_allow_html=True)

            # Deadline with monospace font
            st.markdown(f"""
            <div class="deadline-mono" style="color: {urgency_info['color']}; margin-bottom: 10px;">
                Deadline: {opp['deadline']}
            </div>
            """, unsafe_allow_html=True)

            # Why this rank - expandable
            with st.expander("Why this rank?"):
                st.markdown(f"<span style='color: {COLORS['text_secondary']};'>{opp['why']}</span>", unsafe_allow_html=True)

                # Evidence quote
                if opp.get("evidence"):
                    st.markdown(f"""
                    <div class="evidence-quote">
                        "{opp['evidence']}"
                    </div>
                    """, unsafe_allow_html=True)

            # Action buttons
            btn_col1, btn_col2, btn_col3 = st.columns([0.3, 0.3, 0.4])

            with btn_col1:
                checklist_key = f"checklist_{opp['rank']}"
                if st.button("See Action Checklist", key=checklist_key):
                    st.session_state[f"expand_{opp['rank']}"] = True
                    st.rerun()

            with btn_col2:
                apply_key = f"apply_{opp['rank']}"
                if st.button("Apply Now", key=apply_key, type="primary"):
                    if opp.get("application_link"):
                        st.markdown(f"""
                        <script>window.open("{opp['application_link']}", "_blank");</script>
                        """, unsafe_allow_html=True)
                        st.info(f"Opening application portal: {opp['application_link']}")

        st.markdown("")


def render_action_checklist(opp: Dict[str, Any]):
    """Render the expanded action checklist panel."""
    st.markdown(f"#### Action Checklist - {opp['title']}")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown(f"**Deadline:** {opp['deadline']}")

    with col2:
        if st.button("Set Reminder", key=f"reminder_{opp['rank']}"):
            st.success("Reminder set!")

    st.markdown("")
    st.markdown("**Documents Required:**")

    # Document checkboxes
    for i, doc in enumerate(opp.get("documents", [])):
        st.checkbox(doc, key=f"doc_{opp['rank']}_{i}")

    st.markdown("")
    st.markdown("**Next Steps:**")

    # Next steps with checkboxes
    for i, step in enumerate(opp.get("next_steps", [])):
        st.checkbox(f"{i+1}. {step}", key=f"step_{opp['rank']}_{i}")

    # Evidence quote
    if opp.get("evidence"):
        st.markdown("")
        st.markdown(f"""
        <div class="evidence-quote">
            <strong>Note from email:</strong> "{opp['evidence']}"
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")
    btn_col1, btn_col2, btn_col3 = st.columns(3)

    with btn_col1:
        if st.button("Mark as Applied", key=f"applied_{opp['rank']}"):
            st.success("Marked as applied!")

    with btn_col2:
        if st.button("Dismiss", key=f"dismiss_{opp['rank']}"):
            st.info("Opportunity dismissed")

    with btn_col3:
        if opp.get("application_link"):
            st.markdown(f"[Open Portal]({opp['application_link']})")


def render_profile_insights_section(profile: Dict[str, Any], opportunities: List[Dict[str, Any]]):
    """Render the Profile Insights section with improvement suggestions."""
    from src.suggestions import (
        suggest_profile_improvements,
        generate_skill_gap_analysis,
        calculate_match_potential,
        format_impact_summary,
    )
    from src.models import StudentProfile, Opportunity, OpportunityType, DeadlineType
    from datetime import date

    # Convert profile dict to StudentProfile
    try:
        preferred_types = []
        for t in profile.get("preferred_types", []):
            try:
                preferred_types.append(OpportunityType(t.lower()))
            except ValueError:
                pass

        student_profile = StudentProfile(
            degree=profile.get("degree", "Computer Science"),
            year=profile.get("year", 3),
            cgpa=profile.get("cgpa", 3.5),
            skills=profile.get("skills", []),
            preferred_types=preferred_types,
            financial_need=profile.get("financial_need", False),
            location_pref=profile.get("location_pref"),
            experience=profile.get("experience", []),
        )
    except Exception as e:
        logger.warning(f"Could not create StudentProfile: {e}")
        return

    # Convert opportunities to Opportunity objects
    opp_objects = []
    for opp in opportunities:
        try:
            opp_obj = Opportunity(
                is_opportunity=True,
                confidence=opp.get("match", 80) / 100,
                title=opp.get("title", "Untitled"),
                organization="Organization",
                eligibility_criteria=[
                    f"Looking for candidates with {opp.get('type_label', 'skills')}",
                ],
                required_documents=opp.get("documents", []),
                benefits=opp.get("award"),
                location=opp.get("location"),
            )
            opp_objects.append(opp_obj)
        except Exception:
            pass

    if not opp_objects:
        return

    # Generate suggestions
    suggestions = suggest_profile_improvements(student_profile, opp_objects)
    skill_gaps = generate_skill_gap_analysis(student_profile, opp_objects)

    # Calculate match stats
    matched = sum(1 for o in opportunities if o.get("match", 0) >= 60)
    total = len(opportunities)
    unmatched = total - matched

    # Render Profile Insights Section
    st.markdown("---")
    st.markdown("## Profile Insights")
    st.markdown("*Actionable suggestions to unlock more opportunities*")
    st.markdown("")

    # Summary card
    summary_col1, summary_col2, summary_col3 = st.columns([2, 2, 1])

    with summary_col1:
        st.markdown(f"""
        <div style="background: {COLORS['surface']}; padding: 20px; border-radius: 12px;
                    border-left: 4px solid {COLORS['brand']}; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
            <div style="font-size: 28px; font-weight: 700; color: {COLORS['text_primary']};">{matched}/{total}</div>
            <div style="color: {COLORS['text_secondary']}; font-size: 14px;">Opportunities Matched</div>
        </div>
        """, unsafe_allow_html=True)

    with summary_col2:
        if unmatched > 0:
            st.markdown(f"""
            <div style="background: {COLORS['urgent_bg']}; padding: 20px; border-radius: 12px;
                        border-left: 4px solid {COLORS['urgent']}; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
                <div style="font-size: 28px; font-weight: 700; color: {COLORS['urgent']};">+{unlocked_potential(suggestions)}</div>
                <div style="color: {COLORS['text_secondary']}; font-size: 14px;">More Opportunities Possible</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background: {COLORS['comfortable_bg']}; padding: 20px; border-radius: 12px;
                        border-left: 4px solid {COLORS['comfortable']}; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
                <div style="font-size: 28px; font-weight: 700; color: {COLORS['comfortable']};">Excellent!</div>
                <div style="color: {COLORS['text_secondary']}; font-size: 14px;">Great Profile Match</div>
            </div>
            """, unsafe_allow_html=True)

    with summary_col3:
        st.markdown("")
        st.markdown("")
        if st.button("See Full Analysis", key="full_analysis_btn"):
            st.session_state["show_full_insights"] = not st.session_state.get("show_full_insights", False)
            st.rerun()

    st.markdown("")

    # Top suggestions
    if suggestions:
        st.markdown("### Quick Wins")
        st.markdown(f"*You match {matched}/{total} opportunities. Here's how to match the other {unmatched}:*")
        st.markdown("")

        # Display top 3 suggestions as cards
        suggestion_cols = st.columns(min(3, len(suggestions)))
        for i, (suggestion, impact, priority) in enumerate(suggestions[:3]):
            with suggestion_cols[i % 3]:
                priority_color = COLORS["critical"] if priority == "high" else COLORS["urgent"]
                priority_label = "HIGH IMPACT" if priority == "high" else "MEDIUM IMPACT"

                st.markdown(f"""
                <div style="background: {COLORS['surface']}; padding: 16px; border-radius: 12px;
                            border-top: 3px solid {priority_color}; box-shadow: 0 2px 8px rgba(0,0,0,0.08);
                            margin-bottom: 12px;">
                    <div style="font-size: 11px; color: {priority_color}; font-weight: 700;
                                text-transform: uppercase; letter-spacing: 0.5px;">{priority_label}</div>
                    <div style="margin: 8px 0; color: {COLORS['text_primary']}; font-size: 14px; line-height: 1.5;">
                        {suggestion}
                    </div>
                    <div style="font-size: 12px; color: {COLORS['text_secondary']};">
                        Impact: +{impact} opportunities
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # Interactive skill explorer
        if skill_gaps:
            st.markdown("")
            st.markdown("### Skills That Unlock More Opportunities")
            st.markdown("")

            # Create interactive skill chips
            skill_cols = st.columns(min(5, len(skill_gaps)))
            selected_skill = None

            for i, gap in enumerate(skill_gaps[:5]):
                with skill_cols[i]:
                    skill_name = gap["skill"].title()
                    frequency = gap["frequency"]

                    if st.button(
                        f"{skill_name}\n+{frequency} opps",
                        key=f"skill_{i}",
                        use_container_width=True,
                    ):
                        selected_skill = gap

            # Show details for selected skill
            if selected_skill:
                st.markdown("")
                impact_col1, impact_col2 = st.columns([2, 1])

                with impact_col1:
                    st.markdown(f"""
                    <div style="background: {COLORS['brand']}; color: white; padding: 16px 20px;
                                border-radius: 12px; margin-bottom: 16px;">
                        <div style="font-size: 14px; opacity: 0.9;">Adding {selected_skill['skill'].title()}</div>
                        <div style="font-size: 32px; font-weight: 700; margin: 8px 0;">
                            +{selected_skill['frequency']} more opportunities
                        </div>
                        <div style="font-size: 13px; opacity: 0.8;">
                            Appears in {selected_skill['percentage_of_opps']}% of your opportunities
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                with impact_col2:
                    # Calculate match potential for this skill
                    from src.models import StudentProfile
                    modified_profile = StudentProfile(
                        degree=student_profile.degree,
                        year=student_profile.year,
                        cgpa=student_profile.cgpa,
                        skills=student_profile.skills + [selected_skill["skill"]],
                        preferred_types=student_profile.preferred_types,
                        financial_need=student_profile.financial_need,
                        location_pref=student_profile.location_pref,
                        experience=student_profile.experience,
                    )

                    potential = calculate_match_potential(modified_profile, opp_objects, {
                        "type": "add_skill",
                        "value": selected_skill["skill"],
                    })

                    st.markdown(f"""
                    <div style="background: {COLORS['surface']}; padding: 16px; border-radius: 12px;
                                border: 1px solid {COLORS['border']};">
                        <div style="font-size: 12px; color: {COLORS['text_secondary']};">Newly Unlocked</div>
                        <div style="font-size: 18px; font-weight: 600; color: {COLORS['brand']};">
                            {len(potential['newly_unlocked'])} opportunities
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # Learning resources
                if selected_skill.get("learning_resources"):
                    st.markdown("")
                    st.markdown("**How to learn this:**")
                    for resource in selected_skill["learning_resources"][:3]:
                        st.markdown(f"- {resource}")

    st.markdown("")


def unlocked_potential(suggestions: List[tuple]) -> int:
    """Calculate total potential opportunities from suggestions."""
    if not suggestions:
        return 0
    return sum(s[1] for s in suggestions[:3])


def render_results_screen():
    """Render the results dashboard with ranked opportunities."""
    st.title("Your Opportunity Dashboard")
    st.markdown("*Ranked opportunities with personalized insights*")
    st.markdown("---")

    # Export buttons row
    st.markdown("")
    export_col1, export_col2, export_col3, export_col4 = st.columns(4)

    with export_col1:
        if st.button("Export PDF", key="export_pdf_btn", use_container_width=True):
            # Export top opportunity as PDF
            from src.export import export_to_pdf
            from src.models import RankedOpportunity, Opportunity, OpportunityType, UrgencyTier, ScoreBreakdown, DeadlineType
            from datetime import date, timedelta

            # Convert sample data to RankedOpportunity for export
            top_opp = SAMPLE_OPPORTUNITIES[0] if SAMPLE_OPPORTUNITIES else None
            if top_opp:
                pdf_buffer = export_sample_opportunity_to_pdf(top_opp)
                st.download_button(
                    label="Download PDF",
                    data=pdf_buffer.getvalue(),
                    file_name=f"{top_opp['title'][:30].replace(' ', '_')}.pdf",
                    mime="application/pdf",
                    key="download_pdf"
                )

    with export_col2:
        if st.button("Export All (CSV)", key="export_csv_btn", use_container_width=True):
            from src.export import export_to_csv
            csv_data = export_opportunities_to_csv(SAMPLE_OPPORTUNITIES)
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name="opportunities.csv",
                mime="text/csv",
                key="download_csv"
            )

    with export_col3:
        if st.button("Copy to Clipboard", key="copy_clipboard_btn", use_container_width=True):
            from src.export import copy_to_clipboard
            markdown_text = copy_opportunities_to_clipboard(SAMPLE_OPPORTUNITIES)
            st.code(markdown_text, language="markdown")
            st.info("Select the text above (Ctrl+A) and copy (Ctrl+C) to clipboard")

    with export_col4:
        if st.button("Add to Calendar", key="add_calendar_btn", use_container_width=True):
            from src.export import generate_calendar_ics
            ics_data = generate_calendar_ics_for_opportunities(SAMPLE_OPPORTUNITIES)
            st.download_button(
                label="Download Calendar (.ics)",
                data=ics_data,
                file_name="opportunity_deadlines.ics",
                mime="text/calendar",
                key="download_ics"
            )

    st.markdown("")

    # Profile Insights section (NEW!)
    profile = st.session_state.get("profile", {})
    if profile:
        render_profile_insights_section(profile, SAMPLE_OPPORTUNITIES)

    st.markdown("---")

    # Summary bar
    render_summary_bar()

    # Filter bar
    filter_type, sort_by = render_filter_bar()

    # Filter opportunities based on selection
    filtered_opps = SAMPLE_OPPORTUNITIES
    if filter_type != "All":
        filtered_opps = [o for o in filtered_opps if o["type_label"] == filter_type]

    # Sort opportunities
    if sort_by == "Deadline":
        # Sort by urgency tier (critical first)
        urgency_order = {"critical": 0, "urgent": 1, "moderate": 2, "comfortable": 3, "rolling": 4, "unknown": 5}
        filtered_opps = sorted(filtered_opps, key=lambda x: urgency_order.get(x["urgency"], 5))
    elif sort_by == "Match Score":
        filtered_opps = sorted(filtered_opps, key=lambda x: x["match"], reverse=True)

    # Render opportunity cards
    if not filtered_opps:
        st.info("No opportunities match your filter criteria.")
    else:
        for opp in filtered_opps:
            # Check if this card should show expanded checklist
            checklist_key = f"expand_{opp['rank']}"
            show_checklist = st.session_state.get(checklist_key, False)

            # Render the main card
            render_opportunity_card(opp, expanded=show_checklist)

            # Render expanded checklist if triggered
            if show_checklist:
                with st.container():
                    st.markdown(f"""
                    <div style="background-color: {COLORS['surface']}; border: 1px solid {COLORS['border']}; border-radius: 8px; padding: 20px; margin: -10px 0 20px 20px;">
                    """, unsafe_allow_html=True)

                    render_action_checklist(opp)

                    # Close button
                    if st.button("Close Checklist", key=f"close_{opp['rank']}"):
                        st.session_state[checklist_key] = False
                        st.rerun()

                    st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("")

    # Back button
    st.markdown("---")
    if st.button("Back to Input", key="back_btn"):
        st.session_state["screen"] = "input"
        # Clear processing state
        for key in ["processing_step", "processing_complete"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()


# =============================================================================
# MAIN APP
# =============================================================================

def main():
    """Main application entry point."""
    setup_page_config()

    # Initialize session state
    if "screen" not in st.session_state:
        st.session_state["screen"] = "input"
    if "emails" not in st.session_state:
        st.session_state["emails"] = []
    if "profile" not in st.session_state:
        st.session_state["profile"] = {}

    # Route to appropriate screen
    current_screen = st.session_state["screen"]

    if current_screen == "input":
        render_input_screen()
    elif current_screen == "processing":
        render_processing_screen()
    elif current_screen == "results":
        render_results_screen()


if __name__ == "__main__":
    main()
