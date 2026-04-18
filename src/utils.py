"""Utility functions for Opportunity Inbox Copilot.

This module provides date parsing, text cleaning, validation, and helper
functions for processing opportunities and emails.
"""

import re
from datetime import date, datetime
from typing import Optional
from urllib.parse import urlparse

import dateparser

from src.models import DeadlineType


# =============================================================================
# Date Parsing Functions
# =============================================================================


def parse_date_fuzzy(date_text: str) -> Optional[date]:
    """Parse a fuzzy date string into a date object.

    Uses dateparser library to handle various date formats including:
    - "March 15, 2025"
    - "15 March 2025"
    - "03/15/25"
    - "2025-03-15"
    - "next Friday"
    - "two weeks from now"

    Args:
        date_text: The date string to parse

    Returns:
        A date object if parsing succeeds, None otherwise
    """
    if not date_text or not isinstance(date_text, str):
        return None

    # Clean the input
    cleaned = date_text.strip()
    if not cleaned:
        return None

    try:
        # Use dateparser with settings for better accuracy
        parsed = dateparser.parse(
            cleaned,
            settings={
                'PREFER_DATES_FROM': 'future',
                'STRICT_PARSING': False,
                'RETURN_AS_TIMEZONE_AWARE': False,
            }
        )

        if parsed:
            return parsed.date()

        return None
    except Exception:
        return None


def is_relative_deadline(date_text: str) -> bool:
    """Detect if the date text contains relative time indicators.

    Identifies phrases like:
    - "end of month"
    - "next Friday"
    - "two weeks from now"
    - "coming Friday"
    - "this week"
    - "next week"

    Args:
        date_text: The date text to analyze

    Returns:
        True if the text contains relative time indicators
    """
    if not date_text or not isinstance(date_text, str):
        return False

    text_lower = date_text.lower()

    # Relative time patterns
    relative_patterns = [
        r'\bend of\b',
        r'\bnext\s+(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday|week|month|year)\b',
        r'\bthis\s+(?:week|month|year)\b',
        r'\bcoming\s+(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday|week|month)\b',
        r'\b(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten)\s+(?:days?|weeks?|months?)\s+(?:from\s+now|ago)\b',
        r'\b(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten)\s+(?:days?|weeks?|months?)\b',
        r'\btomorrow\b',
        r'\btoday\b',
        r'\bin\s+(?:a|\d+)\s+(?:days?|weeks?|months?)\b',
        r'\b(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b',
    ]

    for pattern in relative_patterns:
        if re.search(pattern, text_lower):
            return True

    return False


def extract_deadline_type(date_text: Optional[str]) -> DeadlineType:
    """Analyze deadline text and return appropriate DeadlineType.

    Classification logic:
    - "rolling", "continuous", "ongoing" -> ROLLING
    - "early", "priority", "encouraged" -> SOFT_EARLY
    - Relative indicators -> RELATIVE
    - Parseable hard date -> HARD
    - Otherwise -> UNKNOWN

    Args:
        date_text: The deadline text to analyze

    Returns:
        The appropriate DeadlineType enum value
    """
    if not date_text or not isinstance(date_text, str):
        return DeadlineType.UNKNOWN

    text_lower = date_text.lower()

    # Check for rolling basis keywords
    rolling_keywords = ['rolling', 'continuous', 'ongoing', 'open until filled']
    if any(keyword in text_lower for keyword in rolling_keywords):
        return DeadlineType.ROLLING

    # Check for soft/early deadline keywords
    soft_keywords = ['early', 'priority', 'encouraged', 'preferred', 'soft']
    if any(keyword in text_lower for keyword in soft_keywords):
        return DeadlineType.SOFT_EARLY

    # Check for relative time indicators
    if is_relative_deadline(date_text):
        return DeadlineType.RELATIVE

    # Try to parse as a hard date
    parsed_date = parse_date_fuzzy(date_text)
    if parsed_date:
        return DeadlineType.HARD

    return DeadlineType.UNKNOWN


# =============================================================================
# Text Cleaning Functions
# =============================================================================


def clean_email_text(email_text: str) -> str:
    """Clean and normalize email text.

    Performs the following operations:
    - Remove email headers if present
    - Normalize whitespace (multiple spaces, tabs, newlines)
    - Handle common email formatting issues
    - Remove forwarded/reply indicators

    Args:
        email_text: The raw email text to clean

    Returns:
        Cleaned and normalized email text
    """
    if not email_text:
        return ""

    text = email_text

    # Remove common email headers (From:, To:, Subject:, Date:, etc.)
    header_patterns = [
        r'^From:\s*.*?\n',
        r'^To:\s*.*?\n',
        r'^Cc:\s*.*?\n',
        r'^Bcc:\s*.*?\n',
        r'^Subject:\s*.*?\n',
        r'^Date:\s*.*?\n',
        r'^Reply-To:\s*.*?\n',
        r'^Message-ID:\s*.*?\n',
        r'^MIME-Version:\s*.*?\n',
        r'^Content-Type:\s*.*?\n',
        r'^Content-Transfer-Encoding:\s*.*?\n',
    ]

    for pattern in header_patterns:
        text = re.sub(pattern, '', text, flags=re.MULTILINE | re.IGNORECASE)

    # Remove forwarded message indicators
    forwarded_patterns = [
        r'-----Original Message-----.*?\n',
        r'----- Forwarded.*?-----.*?\n',
        r'Begin forwarded message:.*?\n',
        r'________________________.*?\n',
    ]

    for pattern in forwarded_patterns:
        text = re.sub(pattern, '\n', text, flags=re.MULTILINE | re.IGNORECASE | re.DOTALL)

    # Remove reply indicators
    text = re.sub(r'^(?:>|\s*>)+\s*', '', text, flags=re.MULTILINE)

    # Normalize whitespace: replace multiple spaces/tabs with single space
    text = re.sub(r'[ \t]+', ' ', text)

    # Normalize newlines: replace 3+ newlines with 2 newlines
    text = re.sub(r'\n{3,}', '\n\n', text)

    # Strip leading/trailing whitespace
    text = text.strip()

    return text


def extract_email_body(full_email: str) -> str:
    """Extract just the body from a full email string.

    Removes headers, signatures, and common email boilerplate.

    Args:
        full_email: The complete email string

    Returns:
        The extracted email body
    """
    if not full_email:
        return ""

    text = full_email

    # Find where headers end and body begins (first blank line)
    header_end = re.search(r'\n\r?\n', text)
    if header_end:
        text = text[header_end.end():]

    # Remove signatures (common patterns)
    signature_patterns = [
        r'--\s*\n.*',  # Standard signature delimiter
        r'(?:Best|Regards|Sincerely|Cheers|Thanks|Thank you),?\s*\n[^\n]+$',  # Closing + name
        r'(?:Sent from my|Sent via) .*$',  # Mobile signature
    ]

    for pattern in signature_patterns:
        text = re.sub(pattern, '', text, flags=re.MULTILINE | re.IGNORECASE | re.DOTALL)

    # Clean the resulting text
    text = clean_email_text(text)

    return text.strip()


# =============================================================================
# Validation Functions
# =============================================================================


def is_valid_application_link(url: str) -> bool:
    """Validate an application link URL.

    Performs basic URL validation:
    - Must have a scheme (http/https)
    - Must have a netloc (domain)
    - Must be a valid URL structure

    Args:
        url: The URL to validate

    Returns:
        True if the URL is valid, False otherwise
    """
    if not url or not isinstance(url, str):
        return False

    url = url.strip()
    if not url:
        return False

    try:
        parsed = urlparse(url)

        # Check for scheme and netloc
        if not parsed.scheme or not parsed.netloc:
            return False

        # Valid schemes
        if parsed.scheme not in ('http', 'https'):
            return False

        # Basic domain validation
        if '.' not in parsed.netloc:
            return False

        return True
    except Exception:
        return False


def sanitize_excerpt(excerpt: str, max_length: int = 200) -> str:
    """Clean up evidence excerpts for display.

    Performs the following:
    - Truncates to max_length
    - Adds ellipsis if truncated
    - Normalizes whitespace
    - Removes excessive newlines
    - Strips leading/trailing whitespace

    Args:
        excerpt: The raw excerpt text
        max_length: Maximum length for the excerpt (default: 200)

    Returns:
        Sanitized excerpt ready for display
    """
    if not excerpt:
        return ""

    text = excerpt.strip()

    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)

    # Truncate if necessary
    if len(text) > max_length:
        # Try to break at a word boundary
        truncated = text[:max_length]
        last_space = truncated.rfind(' ')

        if last_space > max_length * 0.8:  # If there's a space in the last 20%
            text = truncated[:last_space]
        else:
            text = truncated

        text = text + '...'

    return text


# =============================================================================
# Helper Functions
# =============================================================================


def calculate_days_left(deadline_date: date) -> int:
    """Calculate days from today until the deadline.

    Args:
        deadline_date: The deadline date

    Returns:
        Number of days until deadline (negative if past)
    """
    if not deadline_date:
        return 0

    today = date.today()

    # Handle both date and datetime objects
    if isinstance(deadline_date, datetime):
        deadline_date = deadline_date.date()

    delta = deadline_date - today
    return delta.days


def format_deadline_display(
    deadline_type: DeadlineType,
    deadline_date: Optional[date] = None,
    deadline_text: Optional[str] = None
) -> str:
    """Format deadline for UI display based on type.

    Args:
        deadline_type: The type of deadline
        deadline_date: The parsed deadline date (for HARD deadlines)
        deadline_text: The raw deadline text (for other types)

    Returns:
        Formatted deadline string for display
    """
    if deadline_type == DeadlineType.HARD:
        if deadline_date:
            days = calculate_days_left(deadline_date)
            if days == 0:
                return f"Today ({deadline_date.strftime('%B %d, %Y')})"
            elif days == 1:
                return f"Tomorrow ({deadline_date.strftime('%B %d, %Y')})"
            elif days < 0:
                return f"Expired ({deadline_date.strftime('%B %d, %Y')})"
            else:
                return f"{deadline_date.strftime('%B %d, %Y')} ({days} days left)"
        return "Unknown date"

    elif deadline_type == DeadlineType.ROLLING:
        return "Rolling basis"

    elif deadline_type == DeadlineType.SOFT_EARLY:
        if deadline_text:
            return f"Early deadline: {deadline_text}"
        return "Early deadline encouraged"

    elif deadline_type == DeadlineType.RELATIVE:
        if deadline_text:
            return deadline_text
        return "Relative deadline"

    else:  # UNKNOWN
        if deadline_text:
            return deadline_text
        return "No deadline specified"
