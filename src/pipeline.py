"""Pipeline orchestrator for Opportunity Inbox Copilot.

This module provides the main pipeline functions for processing emails
through the full extraction, scoring, and action generation workflow.
"""

import logging
from datetime import date
from typing import List, Optional, Dict, Any

from groq import Groq

from src.models import (
    StudentProfile,
    Opportunity,
    RankedOpportunity,
    ScoreBreakdown,
    UrgencyTier,
    OpportunityType,
)
from src.extraction import extract_from_email
from src.scoring import (
    calculate_profile_fit,
    calculate_urgency_score,
    calculate_completeness_score,
    calculate_composite_score,
    calculate_urgency_tier,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =============================================================================
# Action Checklist Stub (until actions.py is created by another agent)
# =============================================================================

def generate_action_checklist(opportunity: Opportunity) -> List[Dict[str, Any]]:
    """Generate actionable checklist for an opportunity.

    This is a stub implementation. The full implementation will be provided
    by another agent in actions.py.

    Args:
        opportunity: The opportunity to generate actions for

    Returns:
        List of action items with status and priority
    """
    checklist = []

    # Always add a review action
    checklist.append({
        "action": "Review opportunity details",
        "completed": False,
        "priority": "high",
        "category": "review"
    })

    # Add deadline reminder if applicable
    if opportunity.deadline_type.value != "unknown":
        checklist.append({
            "action": f"Note deadline: {opportunity.deadline_text or opportunity.deadline_type.value}",
            "completed": False,
            "priority": "high",
            "category": "deadline"
        })

    # Add document preparation actions
    for doc in opportunity.required_documents:
        checklist.append({
            "action": f"Prepare {doc}",
            "completed": False,
            "priority": "medium",
            "category": "document"
        })

    # Add application link action
    if opportunity.application_link:
        checklist.append({
            "action": f"Apply via: {opportunity.application_link}",
            "completed": False,
            "priority": "high",
            "category": "application"
        })

    return checklist


# =============================================================================
# Pipeline Functions
# =============================================================================

def process_email(
    email_text: str,
    profile: StudentProfile,
    groq_client: Optional[Groq] = None,
) -> Optional[RankedOpportunity]:
    """Process a single email through the full pipeline.

    Steps:
    1. Extract opportunity from email using Groq LLM
    2. Filter out non-opportunities or low-confidence results
    3. Calculate profile fit score
    4. Calculate urgency score
    5. Calculate completeness score
    6. Calculate composite score with weights
    7. Determine urgency tier
    8. Generate action checklist
    9. Return RankedOpportunity with all data

    Args:
        email_text: The raw email text to process
        profile: Student profile for scoring
        groq_client: Optional initialized Groq client

    Returns:
        RankedOpportunity if valid opportunity, None otherwise
    """
    try:
        logger.info("Starting email processing pipeline")

        # Step 1: Extract opportunity from email
        logger.info("Step 1: Extracting opportunity from email")
        opportunity = extract_from_email(email_text, groq_client)

        # Step 2: Filter out non-opportunities or low-confidence results
        if not opportunity.is_opportunity:
            logger.info(f"Skipping: Not an opportunity (reason: {opportunity.classification_reason})")
            return None

        if opportunity.confidence < 0.5:
            logger.info(f"Skipping: Low confidence ({opportunity.confidence:.2f} < 0.5)")
            return None

        logger.info(f"Opportunity extracted: {opportunity.title or 'Untitled'} "
                    f"({opportunity.opportunity_type.value if opportunity.opportunity_type else 'unknown'})")

        # Step 3: Calculate profile fit score
        logger.info("Step 3: Calculating profile fit score")
        profile_fit, fit_reasons = calculate_profile_fit(profile, opportunity)

        # Step 4: Calculate urgency score
        logger.info("Step 4: Calculating urgency score")
        urgency_score, urgency_explanation = calculate_urgency_score(opportunity)

        # Step 5: Calculate completeness score
        logger.info("Step 5: Calculating completeness score")
        completeness, completeness_factors = calculate_completeness_score(profile, opportunity)

        # Step 6: Calculate composite score
        logger.info("Step 6: Calculating composite score")
        composite_score, score_breakdown = calculate_composite_score(
            profile_fit=profile_fit,
            urgency=urgency_score,
            completeness=completeness,
        )

        # Step 7: Calculate urgency tier
        logger.info("Step 7: Calculating urgency tier")
        urgency_tier = calculate_urgency_tier(opportunity)

        # Step 8: Generate action checklist
        logger.info("Step 8: Generating action checklist")
        action_checklist = generate_action_checklist(opportunity)

        # Build ranking reasons
        ranking_reasons = []
        ranking_reasons.extend(fit_reasons)
        ranking_reasons.append(urgency_explanation)
        ranking_reasons.extend(completeness_factors)

        # Calculate days left for display
        days_left = None
        if opportunity.deadline_date:
            days_left = (opportunity.deadline_date - date.today()).days

        # Step 9: Return RankedOpportunity
        ranked = RankedOpportunity(
            opportunity=opportunity,
            composite_score=composite_score,
            scores=score_breakdown,
            ranking_reasons=ranking_reasons,
            action_checklist=action_checklist,
            urgency_tier=urgency_tier,
            days_left=days_left,
        )

        logger.info(f"Pipeline complete: {opportunity.title or 'Untitled'} "
                    f"with composite score {composite_score:.2f}")

        return ranked

    except Exception as e:
        logger.error(f"Error processing email: {e}")
        return None


def process_inbox(
    emails: List[str],
    profile: StudentProfile,
    groq_client: Optional[Groq] = None,
) -> List[RankedOpportunity]:
    """Process multiple emails and return ranked list.

    Steps:
    1. Iterate through emails
    2. Process each with process_email()
    3. Filter out None results
    4. Sort by composite_score descending
    5. Return List[RankedOpportunity]

    Args:
        emails: List of raw email texts to process
        profile: Student profile for scoring
        groq_client: Optional initialized Groq client

    Returns:
        List of RankedOpportunity objects sorted by composite score
    """
    logger.info(f"Starting inbox processing: {len(emails)} emails")

    ranked_opportunities = []

    for i, email_text in enumerate(emails, 1):
        logger.info(f"Processing email {i}/{len(emails)}")

        try:
            ranked = process_email(email_text, profile, groq_client)
            if ranked is not None:
                ranked_opportunities.append(ranked)
                logger.info(f"Email {i}: Added opportunity '{ranked.opportunity.title or 'Untitled'}'")
            else:
                logger.info(f"Email {i}: No valid opportunity found")
        except Exception as e:
            logger.error(f"Email {i}: Error during processing: {e}")
            continue

    # Sort by composite score descending
    ranked_opportunities.sort(key=lambda x: x.composite_score, reverse=True)

    logger.info(f"Inbox processing complete: {len(ranked_opportunities)} opportunities found")

    return ranked_opportunities


def filter_non_opportunities(
    opportunities: List[RankedOpportunity],
    min_confidence: float = 0.5,
) -> List[RankedOpportunity]:
    """Filter out low-confidence or non-opportunity results.

    Args:
        opportunities: List of RankedOpportunity objects
        min_confidence: Minimum confidence threshold (default: 0.5)

    Returns:
        Filtered list of opportunities meeting confidence threshold
    """
    filtered = [
        opp for opp in opportunities
        if opp.opportunity.is_opportunity and opp.opportunity.confidence >= min_confidence
    ]

    logger.info(f"Filtered {len(opportunities)} opportunities to {len(filtered)} "
                f"meeting confidence threshold {min_confidence}")

    return filtered


def calculate_summary_stats(
    ranked_opportunities: List[RankedOpportunity],
) -> Dict[str, Any]:
    """Calculate summary statistics for a list of ranked opportunities.

    Statistics returned:
    - total_opportunities: Total count
    - count_by_urgency_tier: Count by urgency tier
    - count_by_opportunity_type: Count by opportunity type
    - average_match_score: Average composite score
    - score_range: Min and max composite scores

    Args:
        ranked_opportunities: List of RankedOpportunity objects

    Returns:
        Dictionary containing summary statistics
    """
    if not ranked_opportunities:
        return {
            "total_opportunities": 0,
            "count_by_urgency_tier": {},
            "count_by_opportunity_type": {},
            "average_match_score": 0.0,
            "score_range": {"min": 0.0, "max": 0.0},
        }

    # Total opportunities
    total_opportunities = len(ranked_opportunities)

    # Count by urgency tier
    count_by_urgency_tier: Dict[str, int] = {}
    for opp in ranked_opportunities:
        tier = opp.urgency_tier.value if opp.urgency_tier else "unknown"
        count_by_urgency_tier[tier] = count_by_urgency_tier.get(tier, 0) + 1

    # Count by opportunity type
    count_by_opportunity_type: Dict[str, int] = {}
    for opp in ranked_opportunities:
        opp_type = (opp.opportunity.opportunity_type.value
                    if opp.opportunity.opportunity_type else "unknown")
        count_by_opportunity_type[opp_type] = count_by_opportunity_type.get(opp_type, 0) + 1

    # Average match score
    scores = [opp.composite_score for opp in ranked_opportunities]
    average_match_score = sum(scores) / len(scores) if scores else 0.0

    # Score range
    score_range = {
        "min": min(scores) if scores else 0.0,
        "max": max(scores) if scores else 0.0,
    }

    stats = {
        "total_opportunities": total_opportunities,
        "count_by_urgency_tier": count_by_urgency_tier,
        "count_by_opportunity_type": count_by_opportunity_type,
        "average_match_score": round(average_match_score, 2),
        "score_range": score_range,
    }

    logger.info(f"Summary stats calculated: {total_opportunities} opportunities, "
                f"avg score {average_match_score:.2f}")

    return stats


def get_top_opportunities(
    ranked_opportunities: List[RankedOpportunity],
    n: int = 5,
) -> List[RankedOpportunity]:
    """Return top N opportunities by composite score.

    Args:
        ranked_opportunities: List of RankedOpportunity objects
        n: Number of top opportunities to return (default: 5)

    Returns:
        List of top N RankedOpportunity objects
    """
    # Ensure list is sorted by composite score descending
    sorted_opps = sorted(ranked_opportunities, key=lambda x: x.composite_score, reverse=True)

    top_n = sorted_opps[:n]

    logger.info(f"Retrieved top {len(top_n)} opportunities from {len(ranked_opportunities)} total")

    return top_n


# =============================================================================
# Async Support (Optional)
# =============================================================================

async def process_email_async(
    email_text: str,
    profile: StudentProfile,
    groq_client: Optional[Groq] = None,
) -> Optional[RankedOpportunity]:
    """Async wrapper for process_email.

    This is a placeholder for future async implementation.
    Currently just calls the synchronous version.

    Args:
        email_text: The raw email text to process
        profile: Student profile for scoring
        groq_client: Optional initialized Groq client

    Returns:
        RankedOpportunity if valid opportunity, None otherwise
    """
    # Currently just calls the sync version
    # Future implementation could use asyncio.to_thread or async groq client
    return process_email(email_text, profile, groq_client)


async def process_inbox_async(
    emails: List[str],
    profile: StudentProfile,
    groq_client: Optional[Groq] = None,
) -> List[RankedOpportunity]:
    """Process multiple emails asynchronously.

    This is a placeholder for future async implementation.
    Currently processes emails sequentially.

    Args:
        emails: List of raw email texts to process
        profile: Student profile for scoring
        groq_client: Optional initialized Groq client

    Returns:
        List of RankedOpportunity objects sorted by composite score
    """
    logger.info(f"Starting async inbox processing: {len(emails)} emails")

    # For now, just use the synchronous version
    # Future implementation could use asyncio.gather for parallel processing
    return process_inbox(emails, profile, groq_client)


if __name__ == "__main__":
    # Test imports
    print("Testing pipeline module imports...")

    # Test that we can import all functions
    from src.pipeline import (
        process_email,
        process_inbox,
        filter_non_opportunities,
        calculate_summary_stats,
        get_top_opportunities,
        generate_action_checklist,
    )

    print("All functions imported successfully")
    print("Pipeline module ready!")
