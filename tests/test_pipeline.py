"""Tests for the pipeline orchestrator module.

This module contains integration tests for the pipeline functions including:
- process_email
- process_inbox
- filter_non_opportunities
- calculate_summary_stats
- get_top_opportunities
"""

import pytest
from datetime import date
from typing import List, Optional

from src.models import (
    StudentProfile,
    Opportunity,
    RankedOpportunity,
    ScoreBreakdown,
    UrgencyTier,
    OpportunityType,
    DeadlineType,
)
from src.pipeline import (
    process_email,
    process_inbox,
    filter_non_opportunities,
    calculate_summary_stats,
    get_top_opportunities,
    generate_action_checklist,
)


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture
def sample_profile() -> StudentProfile:
    """Create a sample student profile for testing."""
    return StudentProfile(
        degree="Computer Science",
        year=3,
        cgpa=3.7,
        skills=["Python", "Machine Learning", "Data Analysis"],
        interests=["AI", "Web Development"],
        preferred_types=[OpportunityType.INTERNSHIP, OpportunityType.SCHOLARSHIP],
        financial_need=False,
        location_pref="Remote",
        experience=["2 internships"],
    )


@pytest.fixture
def mock_opportunity() -> Opportunity:
    """Create a mock opportunity for testing."""
    return Opportunity(
        is_opportunity=True,
        confidence=0.9,
        title="Test Internship",
        organization="Test Corp",
        opportunity_type=OpportunityType.INTERNSHIP,
        deadline_type=DeadlineType.HARD,
        deadline_date=date(2025, 6, 15),
        deadline_text=None,
        eligibility_criteria=["Computer Science students", "Python experience"],
        required_documents=["Resume", "Cover Letter"],
        application_link="https://example.com/apply",
        contact_email="hr@testcorp.com",
        benefits="$5000/month stipend",
        location="Remote",
        duration="3 months",
        raw_excerpts=["Join our team", "Remote position available"],
        classification_reason="Contains clear internship opportunity with application link",
    )


@pytest.fixture
def mock_ranked_opportunity(mock_opportunity: Opportunity) -> RankedOpportunity:
    """Create a mock ranked opportunity for testing."""
    return RankedOpportunity(
        opportunity=mock_opportunity,
        composite_score=85.5,
        scores=ScoreBreakdown(
            profile_fit=90.0,
            urgency=80.0,
            completeness=85.0,
            weights={"profile_fit": 0.45, "urgency": 0.30, "completeness": 0.25},
        ),
        ranking_reasons=["Good profile fit", "Upcoming deadline"],
        action_checklist=[
            {"action": "Review opportunity", "completed": False, "priority": "high"},
        ],
        urgency_tier=UrgencyTier.MODERATE,
        days_left=30,
    )


@pytest.fixture
def mock_email_scholarship() -> str:
    """Sample scholarship email text."""
    return """
    Subject: Google Generation Scholarship Application Open

    Dear Students,

    We are excited to announce the Google Generation Scholarship program
    for 2025. This scholarship offers $10,000 for students pursuing
    Computer Science degrees.

    Eligibility:
    - Computer Science or related technical field
    - Minimum 3.0 GPA
    - Demonstrated passion for technology

    Required Documents:
    - Resume
    - Transcript
    - Two recommendation letters
    - Personal statement

    Deadline: March 15, 2025

    Apply at: https://scholarships.google.com/generation

    Contact: scholarships@google.com

    Best regards,
    Google Scholarship Team
    """


@pytest.fixture
def mock_email_internship() -> str:
    """Sample internship email text."""
    return """
    Subject: Summer 2025 Software Engineering Internship at TechCorp

    Hi there,

    TechCorp is hiring Software Engineering Interns for Summer 2025!

    Position: Software Engineering Intern
    Duration: 12 weeks
    Location: Mountain View, CA (Hybrid)
    Stipend: $8,000/month

    Requirements:
    - Currently pursuing BS/MS in Computer Science
    - Experience with Python, Java, or Go
    - Strong problem-solving skills

    Deadline: Applications accepted on a rolling basis

    Apply: https://techcorp.com/careers/interns

    Questions? Email: internships@techcorp.com
    """


@pytest.fixture
def mock_email_not_opportunity() -> str:
    """Sample non-opportunity email text (newsletter)."""
    return """
    Subject: Weekly Tech Newsletter - Issue #42

    Hello Subscriber,

    Here's what's happening in tech this week:

    1. New AI model released
    2. Startup funding rounds
    3. Industry trends

    Thanks for reading!
    """


# =============================================================================
# Tests for generate_action_checklist
# =============================================================================

def test_generate_action_checklist_basic(mock_opportunity: Opportunity):
    """Test basic action checklist generation."""
    checklist = generate_action_checklist(mock_opportunity)

    assert isinstance(checklist, list)
    assert len(checklist) > 0

    # Check structure of action items
    for item in checklist:
        assert "action" in item
        assert "completed" in item
        assert "priority" in item
        assert isinstance(item["completed"], bool)


def test_generate_action_checklist_has_review_action(mock_opportunity: Opportunity):
    """Test that checklist always includes a review action."""
    checklist = generate_action_checklist(mock_opportunity)

    review_actions = [item for item in checklist if "review" in item.get("category", "")]
    assert len(review_actions) >= 1


def test_generate_action_checklist_with_documents(mock_opportunity: Opportunity):
    """Test checklist includes actions for required documents."""
    checklist = generate_action_checklist(mock_opportunity)

    doc_actions = [item for item in checklist if item.get("category") == "document"]
    assert len(doc_actions) == len(mock_opportunity.required_documents)


def test_generate_action_checklist_with_deadline(mock_opportunity: Opportunity):
    """Test checklist includes deadline action."""
    checklist = generate_action_checklist(mock_opportunity)

    deadline_actions = [item for item in checklist if item.get("category") == "deadline"]
    assert len(deadline_actions) >= 1


def test_generate_action_checklist_no_application_link():
    """Test checklist without application link."""
    opp = Opportunity(
        is_opportunity=True,
        confidence=0.8,
        title="Test Opportunity",
        application_link=None,
        deadline_type=DeadlineType.UNKNOWN,
    )

    checklist = generate_action_checklist(opp)
    app_actions = [item for item in checklist if item.get("category") == "application"]
    assert len(app_actions) == 0


# =============================================================================
# Tests for filter_non_opportunities
# =============================================================================

def test_filter_non_opportunities_basic(mock_ranked_opportunity: RankedOpportunity):
    """Test basic filtering of opportunities."""
    opportunities = [mock_ranked_opportunity]
    filtered = filter_non_opportunities(opportunities)

    assert len(filtered) == 1
    assert filtered[0] == mock_ranked_opportunity


def test_filter_non_opportunities_low_confidence(mock_opportunity: Opportunity):
    """Test filtering out low confidence opportunities."""
    low_confidence = Opportunity(
        is_opportunity=True,
        confidence=0.3,  # Below threshold
        title="Low confidence opp",
        deadline_type=DeadlineType.UNKNOWN,
    )

    ranked_low = RankedOpportunity(
        opportunity=low_confidence,
        composite_score=50.0,
        scores=ScoreBreakdown(
            profile_fit=50.0,
            urgency=50.0,
            completeness=50.0,
            weights={},
        ),
        ranking_reasons=[],
        action_checklist=[],
    )

    opportunities = [mock_opportunity, ranked_low]
    # Need to wrap in RankedOpportunity
    ranked_high = RankedOpportunity(
        opportunity=mock_opportunity,
        composite_score=80.0,
        scores=ScoreBreakdown(
            profile_fit=80.0,
            urgency=80.0,
            completeness=80.0,
            weights={},
        ),
        ranking_reasons=[],
        action_checklist=[],
    )

    opportunities = [ranked_high, ranked_low]
    filtered = filter_non_opportunities(opportunities, min_confidence=0.5)

    assert len(filtered) == 1
    assert filtered[0].opportunity.confidence >= 0.5


def test_filter_non_opportunities_not_opportunity(mock_opportunity: Opportunity):
    """Test filtering out non-opportunities."""
    not_opp = Opportunity(
        is_opportunity=False,
        confidence=0.9,
        title="Not an opportunity",
        deadline_type=DeadlineType.UNKNOWN,
    )

    ranked_not = RankedOpportunity(
        opportunity=not_opp,
        composite_score=0.0,
        scores=ScoreBreakdown(
            profile_fit=0.0,
            urgency=0.0,
            completeness=0.0,
            weights={},
        ),
        ranking_reasons=[],
        action_checklist=[],
    )

    ranked_yes = RankedOpportunity(
        opportunity=mock_opportunity,
        composite_score=80.0,
        scores=ScoreBreakdown(
            profile_fit=80.0,
            urgency=80.0,
            completeness=80.0,
            weights={},
        ),
        ranking_reasons=[],
        action_checklist=[],
    )

    opportunities = [ranked_not, ranked_yes]
    filtered = filter_non_opportunities(opportunities)

    assert len(filtered) == 1
    assert filtered[0].opportunity.is_opportunity is True


def test_filter_non_opportunities_empty_list():
    """Test filtering empty list."""
    filtered = filter_non_opportunities([])
    assert filtered == []


def test_filter_non_opportunities_custom_threshold():
    """Test filtering with custom confidence threshold."""
    med_confidence = Opportunity(
        is_opportunity=True,
        confidence=0.7,
        title="Medium confidence",
        deadline_type=DeadlineType.UNKNOWN,
    )

    ranked_med = RankedOpportunity(
        opportunity=med_confidence,
        composite_score=70.0,
        scores=ScoreBreakdown(
            profile_fit=70.0,
            urgency=70.0,
            completeness=70.0,
            weights={},
        ),
        ranking_reasons=[],
        action_checklist=[],
    )

    opportunities = [ranked_med]
    filtered = filter_non_opportunities(opportunities, min_confidence=0.8)

    assert len(filtered) == 0


# =============================================================================
# Tests for calculate_summary_stats
# =============================================================================

def test_calculate_summary_stats_empty():
    """Test summary stats with empty list."""
    stats = calculate_summary_stats([])

    assert stats["total_opportunities"] == 0
    assert stats["count_by_urgency_tier"] == {}
    assert stats["count_by_opportunity_type"] == {}
    assert stats["average_match_score"] == 0.0
    assert stats["score_range"] == {"min": 0.0, "max": 0.0}


def test_calculate_summary_stats_single(mock_ranked_opportunity: RankedOpportunity):
    """Test summary stats with single opportunity."""
    stats = calculate_summary_stats([mock_ranked_opportunity])

    assert stats["total_opportunities"] == 1
    assert stats["average_match_score"] == 85.5
    assert stats["score_range"]["min"] == 85.5
    assert stats["score_range"]["max"] == 85.5


def test_calculate_summary_stats_multiple():
    """Test summary stats with multiple opportunities."""
    opp1 = Opportunity(
        is_opportunity=True,
        confidence=0.9,
        title="Opp 1",
        opportunity_type=OpportunityType.INTERNSHIP,
        deadline_type=DeadlineType.HARD,
        deadline_date=date(2025, 6, 1),
    )

    opp2 = Opportunity(
        is_opportunity=True,
        confidence=0.8,
        title="Opp 2",
        opportunity_type=OpportunityType.SCHOLARSHIP,
        deadline_type=DeadlineType.ROLLING,
    )

    opp3 = Opportunity(
        is_opportunity=True,
        confidence=0.85,
        title="Opp 3",
        opportunity_type=OpportunityType.INTERNSHIP,
        deadline_type=DeadlineType.HARD,
        deadline_date=date(2025, 7, 1),
    )

    ranked_opps = [
        RankedOpportunity(
            opportunity=opp1,
            composite_score=90.0,
            scores=ScoreBreakdown(profile_fit=90.0, urgency=90.0, completeness=90.0, weights={}),
            ranking_reasons=[],
            action_checklist=[],
            urgency_tier=UrgencyTier.URGENT,
        ),
        RankedOpportunity(
            opportunity=opp2,
            composite_score=70.0,
            scores=ScoreBreakdown(profile_fit=70.0, urgency=70.0, completeness=70.0, weights={}),
            ranking_reasons=[],
            action_checklist=[],
            urgency_tier=UrgencyTier.ROLLING,
        ),
        RankedOpportunity(
            opportunity=opp3,
            composite_score=80.0,
            scores=ScoreBreakdown(profile_fit=80.0, urgency=80.0, completeness=80.0, weights={}),
            ranking_reasons=[],
            action_checklist=[],
            urgency_tier=UrgencyTier.MODERATE,
        ),
    ]

    stats = calculate_summary_stats(ranked_opps)

    assert stats["total_opportunities"] == 3
    assert stats["average_match_score"] == 80.0
    assert stats["score_range"]["min"] == 70.0
    assert stats["score_range"]["max"] == 90.0
    assert stats["count_by_urgency_tier"]["urgent"] == 1
    assert stats["count_by_urgency_tier"]["rolling"] == 1
    assert stats["count_by_urgency_tier"]["moderate"] == 1
    assert stats["count_by_opportunity_type"]["internship"] == 2
    assert stats["count_by_opportunity_type"]["scholarship"] == 1


# =============================================================================
# Tests for get_top_opportunities
# =============================================================================

def test_get_top_opportunities_basic():
    """Test getting top N opportunities."""
    opps = [
        RankedOpportunity(
            opportunity=Opportunity(is_opportunity=True, confidence=0.9, title=f"Opp {i}", deadline_type=DeadlineType.UNKNOWN),
            composite_score=float(80 - i * 10),  # 80, 70, 60, 50, 40, 30
            scores=ScoreBreakdown(profile_fit=0.0, urgency=0.0, completeness=0.0, weights={}),
            ranking_reasons=[],
            action_checklist=[],
        )
        for i in range(6)
    ]

    top = get_top_opportunities(opps, n=3)

    assert len(top) == 3
    assert top[0].composite_score == 80.0
    assert top[1].composite_score == 70.0
    assert top[2].composite_score == 60.0


def test_get_top_opportunities_default_n():
    """Test getting top opportunities with default n=5."""
    opps = [
        RankedOpportunity(
            opportunity=Opportunity(is_opportunity=True, confidence=0.9, title=f"Opp {i}", deadline_type=DeadlineType.UNKNOWN),
            composite_score=float(100 - i * 5),
            scores=ScoreBreakdown(profile_fit=0.0, urgency=0.0, completeness=0.0, weights={}),
            ranking_reasons=[],
            action_checklist=[],
        )
        for i in range(10)
    ]

    top = get_top_opportunities(opps)  # Default n=5

    assert len(top) == 5


def test_get_top_opportunities_less_than_n():
    """Test getting top opportunities when list has fewer than n items."""
    opps = [
        RankedOpportunity(
            opportunity=Opportunity(is_opportunity=True, confidence=0.9, title="Opp 1", deadline_type=DeadlineType.UNKNOWN),
            composite_score=80.0,
            scores=ScoreBreakdown(profile_fit=0.0, urgency=0.0, completeness=0.0, weights={}),
            ranking_reasons=[],
            action_checklist=[],
        ),
    ]

    top = get_top_opportunities(opps, n=5)

    assert len(top) == 1


def test_get_top_opportunities_empty_list():
    """Test getting top opportunities from empty list."""
    top = get_top_opportunities([], n=5)
    assert top == []


def test_get_top_opportunities_sorts_correctly():
    """Test that opportunities are sorted by composite score."""
    opps = [
        RankedOpportunity(
            opportunity=Opportunity(is_opportunity=True, confidence=0.9, title="Low", deadline_type=DeadlineType.UNKNOWN),
            composite_score=50.0,
            scores=ScoreBreakdown(profile_fit=0.0, urgency=0.0, completeness=0.0, weights={}),
            ranking_reasons=[],
            action_checklist=[],
        ),
        RankedOpportunity(
            opportunity=Opportunity(is_opportunity=True, confidence=0.9, title="High", deadline_type=DeadlineType.UNKNOWN),
            composite_score=90.0,
            scores=ScoreBreakdown(profile_fit=0.0, urgency=0.0, completeness=0.0, weights={}),
            ranking_reasons=[],
            action_checklist=[],
        ),
        RankedOpportunity(
            opportunity=Opportunity(is_opportunity=True, confidence=0.9, title="Medium", deadline_type=DeadlineType.UNKNOWN),
            composite_score=70.0,
            scores=ScoreBreakdown(profile_fit=0.0, urgency=0.0, completeness=0.0, weights={}),
            ranking_reasons=[],
            action_checklist=[],
        ),
    ]

    top = get_top_opportunities(opps, n=2)

    assert top[0].composite_score == 90.0
    assert top[1].composite_score == 70.0


# =============================================================================
# Tests for process_email (with mocked extraction)
# =============================================================================

def test_process_email_no_groq_client(sample_profile: StudentProfile):
    """Test process_email without Groq client (should fail gracefully)."""
    email_text = "Some email about an internship opportunity"

    # Should return None when no client available and extraction fails
    result = process_email(email_text, sample_profile, groq_client=None)
    # This will fail because extract_from_email requires a client or env var
    # The function should handle the error gracefully and return None
    assert result is None


def test_process_email_error_handling(sample_profile: StudentProfile):
    """Test that process_email handles errors gracefully."""
    # Empty email should not crash
    result = process_email("", sample_profile)
    assert result is None

    # Malformed email should not crash
    result = process_email("garbage data 123", sample_profile)
    assert result is None


# =============================================================================
# Tests for process_inbox (with mocked extraction)
# =============================================================================

def test_process_inbox_empty_list(sample_profile: StudentProfile):
    """Test processing empty inbox."""
    result = process_inbox([], sample_profile)
    assert result == []


def test_process_inbox_all_invalid(sample_profile: StudentProfile, mock_email_not_opportunity: str):
    """Test processing inbox where all emails are not opportunities."""
    emails = [mock_email_not_opportunity] * 3

    # Should return empty list since emails are not opportunities
    # (Note: Without mocked extraction, this requires real API call)
    # result = process_inbox(emails, sample_profile)
    # assert result == []
    pass  # Skip - requires mocking


# =============================================================================
# Integration Test Example
# =============================================================================

def test_pipeline_integration(sample_profile: StudentProfile, mock_opportunity: Opportunity):
    """Integration test demonstrating full pipeline flow."""
    # Create a ranked opportunity manually to test downstream functions
    ranked = RankedOpportunity(
        opportunity=mock_opportunity,
        composite_score=85.0,
        scores=ScoreBreakdown(
            profile_fit=90.0,
            urgency=80.0,
            completeness=85.0,
            weights={"profile_fit": 0.45, "urgency": 0.30, "completeness": 0.25},
        ),
        ranking_reasons=[
            "Strong degree match",
            "CGPA meets requirements",
            "Moderate urgency",
        ],
        action_checklist=generate_action_checklist(mock_opportunity),
        urgency_tier=UrgencyTier.MODERATE,
        days_left=30,
    )

    # Test filtering
    filtered = filter_non_opportunities([ranked])
    assert len(filtered) == 1

    # Test summary stats
    stats = calculate_summary_stats([ranked])
    assert stats["total_opportunities"] == 1
    assert stats["average_match_score"] == 85.0

    # Test top opportunities
    top = get_top_opportunities([ranked], n=1)
    assert len(top) == 1
    assert top[0].opportunity.title == "Test Internship"


if __name__ == "__main__":
    # Run basic import test
    print("Testing pipeline imports...")

    from src.pipeline import (
        process_email,
        process_inbox,
        filter_non_opportunities,
        calculate_summary_stats,
        get_top_opportunities,
        generate_action_checklist,
    )

    print("All pipeline functions imported successfully!")
    print("\nRun with pytest for full test suite:")
    print("  pytest tests/test_pipeline.py -v")
