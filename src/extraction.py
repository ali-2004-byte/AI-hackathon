"""Groq LLM extraction layer for Opportunity Inbox Copilot.

This module provides functions to extract structured opportunity data from
unstructured email text using Groq's LLM API with Pydantic-based structured output.
"""

import os
import logging
import time
from typing import Optional, Tuple, List
from datetime import date

from groq import Groq
from groq.types.chat.chat_completion import ChatCompletion

from src.models import Opportunity, DeadlineType, OpportunityType

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =============================================================================
# Groq Client Initialization
# =============================================================================

def get_groq_client() -> Groq:
    """Initialize and return a Groq client.

    Reads the API key from the GROQ_API_KEY environment variable.
    Raises a ValueError if the API key is not found.

    Returns:
        Groq: Initialized Groq client instance.

    Raises:
        ValueError: If GROQ_API_KEY environment variable is not set.
    """
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY environment variable is not set. "
            "Please set it before running the extraction."
        )
    return Groq(api_key=api_key)


def get_groq_client_safe() -> Optional[Groq]:
    """Initialize Groq client, returning None if API key is missing.

    This is a safe wrapper that doesn't raise exceptions for missing keys.

    Returns:
        Groq | None: Initialized Groq client or None if API key is missing.
    """
    try:
        return get_groq_client()
    except ValueError:
        logger.warning("GROQ_API_KEY not found. Extraction functions will not work.")
        return None


# =============================================================================
# Extraction Prompt
# =============================================================================

EXTRACTION_SYSTEM_PROMPT = """You are an expert information extraction system for an "Opportunity Inbox Copilot" - a tool that helps students find and track academic and career opportunities from their emails.

Your task is to analyze the provided email text and extract structured information about any opportunities mentioned (scholarships, internships, fellowships, competitions, research positions, jobs, etc.).

DEADLINE TYPE CLASSIFICATION RULES:
- "hard": A specific, concrete date is given (e.g., "March 15, 2025", "December 1, 2024")
- "rolling": Phrases like "rolling basis", "continuous review", "ongoing", "we review as received"
- "soft_early": Phrases like "early applications encouraged", "priority deadline", "early deadline", "encouraged to apply early"
- "relative": Relative time references like "end of month", "next Friday", "two weeks from now", "by month's end"
- "unknown": No deadline information is provided

CRITICAL RULES:
1. Only set deadline_date if deadline_type is "hard" (i.e., there's a specific calendar date)
2. For rolling, soft_early, relative, or unknown deadlines, set deadline_text with the raw text instead
3. Set is_opportunity to false for spam, newsletters, advertisements, or generic announcements without specific actionable opportunities
4. Extract 2-3 raw_excerpts as direct quotes from the email that support key claims (eligibility, deadlines, benefits)
5. Be precise - only extract information that is explicitly stated in the email

Extract the following fields:
- is_opportunity: Whether this email contains a genuine actionable opportunity
- confidence: Your confidence in this classification (0.0 to 1.0)
- classification_reason: Brief explanation of why this is/isn't an opportunity
- title: The opportunity title/name
- organization: Organization offering the opportunity
- opportunity_type: One of: scholarship, internship, fellowship, competition, research, job, exchange, other
- deadline_type: One of: hard, rolling, soft_early, relative, unknown
- deadline_date: ISO date string (YYYY-MM-DD) only if deadline_type is "hard"
- deadline_text: Raw deadline text for non-hard deadlines
- eligibility_criteria: List of eligibility requirements
- required_documents: List of required application documents
- application_link: URL for applying
- contact_email: Contact email for questions
- benefits: Benefits/award amount (e.g., "$10,000 scholarship")
- location: Location (e.g., "Remote", "Mountain View, CA")
- duration: Duration if applicable (e.g., "3 months", "1 year")
- raw_excerpts: 2-3 direct quotes from the email as evidence
"""

# Alias for backward compatibility
EXTRACTION_PROMPT = EXTRACTION_SYSTEM_PROMPT

CLASSIFICATION_SYSTEM_PROMPT = """You are an expert at classifying emails to determine if they contain genuine actionable opportunities for students.

An "opportunity" is a specific, actionable program that a student can apply for, such as:
- Scholarships or financial aid
- Internships or co-op programs
- Fellowships or grants
- Research positions
- Competitions or hackathons
- Job openings
- Exchange programs

NOT opportunities (should be classified as false):
- Newsletters or general updates
- Spam or advertisements
- Generic motivational content
- Scams or "get rich quick" schemes
- Information-only announcements without an application process
- Product promotions or sales pitches

Analyze the email and return:
1. is_opportunity: true if this is a genuine actionable opportunity, false otherwise
2. confidence: Your confidence score from 0.0 to 1.0
3. reason: A brief explanation of your classification decision

Be conservative - when in doubt, classify as not an opportunity.
"""


# =============================================================================
# Retry Logic
# =============================================================================

def retry_with_backoff(
    func,
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 10.0,
    exceptions: Tuple[type, ...] = (Exception,)
) -> any:
    """Execute a function with exponential backoff retry logic.

    Args:
        func: The function to execute.
        max_retries: Maximum number of retry attempts.
        base_delay: Initial delay in seconds between retries.
        max_delay: Maximum delay in seconds between retries.
        exceptions: Tuple of exception types to catch and retry on.

    Returns:
        The result of the function call.

    Raises:
        The last exception encountered after all retries are exhausted.
    """
    last_exception = None

    for attempt in range(max_retries):
        try:
            return func()
        except exceptions as e:
            last_exception = e
            if attempt < max_retries - 1:
                # Calculate exponential backoff with jitter
                delay = min(base_delay * (2 ** attempt), max_delay)
                logger.warning(
                    f"Attempt {attempt + 1}/{max_retries} failed: {e}. "
                    f"Retrying in {delay:.1f}s..."
                )
                time.sleep(delay)
            else:
                logger.error(f"All {max_retries} attempts failed. Last error: {e}")

    raise last_exception


# =============================================================================
# Extraction Function
# =============================================================================

def _call_groq_extraction(email_text: str, groq_client: Groq) -> Opportunity:
    """Internal function to call Groq API for extraction.

    Args:
        email_text: The raw email text to analyze.
        groq_client: Initialized Groq client.

    Returns:
        Opportunity: Parsed opportunity data.
    """
    response = groq_client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": EXTRACTION_SYSTEM_PROMPT},
            {"role": "user", "content": f"Extract opportunity information from this email:\n\n{email_text}"}
        ],
        temperature=0,
        response_format={"type": "json_object"},
    )

    # Parse the JSON response
    import json
    content = response.choices[0].message.content
    data = json.loads(content)

    # Handle deadline_date parsing
    deadline_date = None
    if data.get("deadline_date") and data.get("deadline_type") == "hard":
        try:
            # Parse ISO date string
            date_str = data["deadline_date"]
            if isinstance(date_str, str):
                deadline_date = date.fromisoformat(date_str.replace("Z", ""))
        except (ValueError, TypeError):
            logger.warning(f"Could not parse deadline_date: {data.get('deadline_date')}")
            deadline_date = None

    # Handle deadline_type enum
    deadline_type_str = data.get("deadline_type", "unknown")
    try:
        deadline_type = DeadlineType(deadline_type_str.lower())
    except ValueError:
        deadline_type = DeadlineType.UNKNOWN

    # Handle opportunity_type enum
    opportunity_type = None
    if data.get("opportunity_type"):
        try:
            opportunity_type = OpportunityType(data["opportunity_type"].lower())
        except ValueError:
            opportunity_type = None

    # Build the Opportunity object
    opportunity = Opportunity(
        is_opportunity=data.get("is_opportunity", False),
        confidence=float(data.get("confidence", 0.0)),
        classification_reason=data.get("classification_reason"),
        title=data.get("title"),
        organization=data.get("organization"),
        opportunity_type=opportunity_type,
        deadline_type=deadline_type,
        deadline_date=deadline_date,
        deadline_text=data.get("deadline_text"),
        eligibility_criteria=data.get("eligibility_criteria", []),
        required_documents=data.get("required_documents", []),
        application_link=data.get("application_link"),
        contact_email=data.get("contact_email"),
        benefits=data.get("benefits"),
        location=data.get("location"),
        duration=data.get("duration"),
        raw_excerpts=data.get("raw_excerpts", []),
    )

    return opportunity


def extract_from_email(email_text: str, groq_client: Optional[Groq] = None) -> Opportunity:
    """Extract structured opportunity data from an email using Groq LLM.

    Uses structured output with retry logic and exponential backoff.

    Args:
        email_text: The raw email text to analyze.
        groq_client: Optional initialized Groq client. If not provided, will
                    attempt to create one using get_groq_client().

    Returns:
        Opportunity: Validated Opportunity Pydantic model with extracted data.

    Raises:
        ValueError: If groq_client is not provided and GROQ_API_KEY is not set.
        Exception: If all API retry attempts fail.
    """
    if groq_client is None:
        groq_client = get_groq_client()

    logger.info("Extracting opportunity from email using Groq API...")

    def _extract():
        return _call_groq_extraction(email_text, groq_client)

    opportunity = retry_with_backoff(
        _extract,
        max_retries=3,
        base_delay=1.0,
        exceptions=(Exception,)
    )

    logger.info(f"Extraction complete. is_opportunity={opportunity.is_opportunity}, "
                f"confidence={opportunity.confidence:.2f}")

    return opportunity


# =============================================================================
# Classification Function
# =============================================================================

def _call_groq_classification(email_text: str, groq_client: Groq) -> Tuple[bool, float, str]:
    """Internal function to call Groq API for classification.

    Args:
        email_text: The raw email text to analyze.
        groq_client: Initialized Groq client.

    Returns:
        Tuple of (is_opportunity, confidence, reason).
    """
    response = groq_client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": CLASSIFICATION_SYSTEM_PROMPT},
            {"role": "user", "content": f"Classify this email:\n\n{email_text}"}
        ],
        temperature=0,
        response_format={"type": "json_object"},
    )

    import json
    content = response.choices[0].message.content
    data = json.loads(content)

    is_opportunity = bool(data.get("is_opportunity", False))
    confidence = float(data.get("confidence", 0.0))
    reason = str(data.get("reason", ""))

    return is_opportunity, confidence, reason


def classify_opportunity(email_text: str, groq_client: Optional[Groq] = None) -> Tuple[bool, float, str]:
    """Classify whether an email contains a genuine opportunity.

    This is a lightweight classification that only determines if the email
    is an opportunity and provides a confidence score, without doing full
    information extraction.

    Args:
        email_text: The raw email text to analyze.
        groq_client: Optional initialized Groq client. If not provided, will
                    attempt to create one using get_groq_client().

    Returns:
        Tuple of (is_opportunity: bool, confidence: float, reason: str).

    Raises:
        ValueError: If groq_client is not provided and GROQ_API_KEY is not set.
        Exception: If all API retry attempts fail.
    """
    if groq_client is None:
        groq_client = get_groq_client()

    logger.info("Classifying email using Groq API...")

    def _classify():
        return _call_groq_classification(email_text, groq_client)

    result = retry_with_backoff(
        _classify,
        max_retries=3,
        base_delay=1.0,
        exceptions=(Exception,)
    )

    logger.info(f"Classification complete. is_opportunity={result[0]}, "
                f"confidence={result[1]:.2f}")

    return result


# =============================================================================
# Convenience Functions
# =============================================================================

def extract_opportunities_batch(
    emails: List[str],
    groq_client: Optional[Groq] = None
) -> List[Opportunity]:
    """Extract opportunities from multiple emails in batch.

    Args:
        emails: List of email texts to process.
        groq_client: Optional initialized Groq client.

    Returns:
        List of extracted Opportunity objects.
    """
    if groq_client is None:
        groq_client = get_groq_client()

    opportunities = []
    for i, email in enumerate(emails):
        logger.info(f"Processing email {i + 1}/{len(emails)}...")
        try:
            opp = extract_from_email(email, groq_client)
            opportunities.append(opp)
        except Exception as e:
            logger.error(f"Failed to process email {i + 1}: {e}")
            # Return a placeholder with error info
            opportunities.append(Opportunity(
                is_opportunity=False,
                confidence=0.0,
                classification_reason=f"Extraction failed: {str(e)}"
            ))

    return opportunities


if __name__ == "__main__":
    # Test import and basic functionality
    print("Testing extraction module...")

    # Test that we can import the models
    from src.models import Opportunity, DeadlineType, OpportunityType
    print("✓ Models imported successfully")

    # Test creating a client (will fail without API key, but tests the code path)
    try:
        client = get_groq_client()
        print("✓ Groq client initialized successfully")
    except ValueError as e:
        print(f"⚠ Groq client initialization failed (expected without API key): {e}")

    print("\nExtraction module ready!")
