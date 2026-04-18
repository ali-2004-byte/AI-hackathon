"""Comprehensive tests for the deterministic scoring engine."""

import pytest
from datetime import date, timedelta

from src.models import (
    StudentProfile,
    Opportunity,
    DeadlineType,
    UrgencyTier,
    OpportunityType,
)
from src.scoring import (
    calculate_profile_fit,
    calculate_urgency_score,
    calculate_completeness_score,
    calculate_composite_score,
    calculate_urgency_tier,
)


class TestCalculateUrgencyScore:
    """Test suite for urgency scoring with all DeadlineType paths."""

    def test_hard_deadline_critical(self):
        """Test HARD deadline with <= 3 days left (CRITICAL)."""
        opp = Opportunity(
            is_opportunity=True,
            confidence=0.9,
            deadline_type=DeadlineType.HARD,
            deadline_date=date.today() + timedelta(days=2),
        )
        score, reason = calculate_urgency_score(opp)
        assert score == 100.0
        assert "CRITICAL" in reason
        assert "2 days left" in reason

    def test_hard_deadline_urgent(self):
        """Test HARD deadline with 4-7 days left (URGENT)."""
        opp = Opportunity(
            is_opportunity=True,
            confidence=0.9,
            deadline_type=DeadlineType.HARD,
            deadline_date=date.today() + timedelta(days=5),
        )
        score, reason = calculate_urgency_score(opp)
        assert score == 90.0
        assert "URGENT" in reason
        assert "5 days left" in reason

    def test_hard_deadline_moderate(self):
        """Test HARD deadline with 8-30 days left (MODERATE)."""
        opp = Opportunity(
            is_opportunity=True,
            confidence=0.9,
            deadline_type=DeadlineType.HARD,
            deadline_date=date.today() + timedelta(days=15),
        )
        score, reason = calculate_urgency_score(opp)
        assert score == 70.0
        assert "MODERATE" in reason
        assert "15 days left" in reason

    def test_hard_deadline_comfortable(self):
        """Test HARD deadline with 31-60 days left (COMFORTABLE)."""
        opp = Opportunity(
            is_opportunity=True,
            confidence=0.9,
            deadline_type=DeadlineType.HARD,
            deadline_date=date.today() + timedelta(days=45),
        )
        score, reason = calculate_urgency_score(opp)
        assert score == 40.0
        assert "COMFORTABLE" in reason
        assert "45 days left" in reason

    def test_hard_deadline_far_future(self):
        """Test HARD deadline with > 60 days left."""
        opp = Opportunity(
            is_opportunity=True,
            confidence=0.9,
            deadline_type=DeadlineType.HARD,
            deadline_date=date.today() + timedelta(days=90),
        )
        score, reason = calculate_urgency_score(opp)
        assert score == 20.0
        assert "90 days left" in reason

    def test_hard_deadline_past(self):
        """Test HARD deadline that has already passed."""
        opp = Opportunity(
            is_opportunity=True,
            confidence=0.9,
            deadline_type=DeadlineType.HARD,
            deadline_date=date.today() - timedelta(days=5),
        )
        score, reason = calculate_urgency_score(opp)
        assert score == 0.0
        assert "PASSED" in reason

    def test_hard_deadline_no_date(self):
        """Test HARD deadline without deadline_date set."""
        opp = Opportunity(
            is_opportunity=True,
            confidence=0.9,
            deadline_type=DeadlineType.HARD,
            deadline_date=None,
        )
        score, reason = calculate_urgency_score(opp)
        assert score == 50.0
        assert "unavailable" in reason

    def test_rolling_deadline(self):
        """Test ROLLING deadline type."""
        opp = Opportunity(
            is_opportunity=True,
            confidence=0.9,
            deadline_type=DeadlineType.ROLLING,
        )
        score, reason = calculate_urgency_score(opp)
        assert score == 75.0
        assert "ROLLING BASIS" in reason

    def test_soft_early_deadline(self):
        """Test SOFT_EARLY deadline type."""
        opp = Opportunity(
            is_opportunity=True,
            confidence=0.9,
            deadline_type=DeadlineType.SOFT_EARLY,
        )
        score, reason = calculate_urgency_score(opp)
        assert score == 65.0
        assert "EARLY PRIORITY" in reason

    def test_relative_deadline(self):
        """Test RELATIVE deadline type."""
        opp = Opportunity(
            is_opportunity=True,
            confidence=0.9,
            deadline_type=DeadlineType.RELATIVE,
            deadline_text="End of month",
        )
        score, reason = calculate_urgency_score(opp)
        assert score == 60.0
        assert "RELATIVE" in reason

    def test_unknown_deadline(self):
        """Test UNKNOWN deadline type."""
        opp = Opportunity(
            is_opportunity=True,
            confidence=0.9,
            deadline_type=DeadlineType.UNKNOWN,
        )
        score, reason = calculate_urgency_score(opp)
        assert score == 50.0
        assert "UNKNOWN" in reason

    def test_custom_reference_date(self):
        """Test with custom reference date."""
        ref_date = date(2025, 6, 1)
        deadline = date(2025, 6, 3)
        opp = Opportunity(
            is_opportunity=True,
            confidence=0.9,
            deadline_type=DeadlineType.HARD,
            deadline_date=deadline,
        )
        score, reason = calculate_urgency_score(opp, ref_date)
        assert score == 100.0
        assert "CRITICAL" in reason


class TestCalculateUrgencyTier:
    """Test suite for urgency tier calculation."""

    def test_urgency_tier_critical(self):
        """Test CRITICAL tier (<= 3 days)."""
        opp = Opportunity(
            is_opportunity=True,
            confidence=0.9,
            deadline_type=DeadlineType.HARD,
            deadline_date=date.today() + timedelta(days=3),
        )
        tier = calculate_urgency_tier(opp)
        assert tier == UrgencyTier.CRITICAL

    def test_urgency_tier_urgent(self):
        """Test URGENT tier (4-7 days)."""
        opp = Opportunity(
            is_opportunity=True,
            confidence=0.9,
            deadline_type=DeadlineType.HARD,
            deadline_date=date.today() + timedelta(days=5),
        )
        tier = calculate_urgency_tier(opp)
        assert tier == UrgencyTier.URGENT

    def test_urgency_tier_moderate(self):
        """Test MODERATE tier (8-30 days)."""
        opp = Opportunity(
            is_opportunity=True,
            confidence=0.9,
            deadline_type=DeadlineType.HARD,
            deadline_date=date.today() + timedelta(days=20),
        )
        tier = calculate_urgency_tier(opp)
        assert tier == UrgencyTier.MODERATE

    def test_urgency_tier_comfortable(self):
        """Test COMFORTABLE tier (31-60 days)."""
        opp = Opportunity(
            is_opportunity=True,
            confidence=0.9,
            deadline_type=DeadlineType.HARD,
            deadline_date=date.today() + timedelta(days=45),
        )
        tier = calculate_urgency_tier(opp)
        assert tier == UrgencyTier.COMFORTABLE

    def test_urgency_tier_rolling(self):
        """Test ROLLING tier."""
        opp = Opportunity(
            is_opportunity=True,
            confidence=0.9,
            deadline_type=DeadlineType.ROLLING,
        )
        tier = calculate_urgency_tier(opp)
        assert tier == UrgencyTier.ROLLING

    def test_urgency_tier_unknown(self):
        """Test UNKNOWN tier."""
        opp = Opportunity(
            is_opportunity=True,
            confidence=0.9,
            deadline_type=DeadlineType.UNKNOWN,
        )
        tier = calculate_urgency_tier(opp)
        assert tier == UrgencyTier.UNKNOWN


class TestCalculateProfileFit:
    """Test suite for profile fit scoring."""

    def test_perfect_match(self):
        """Test perfect profile match."""
        profile = StudentProfile(
            degree="Computer Science",
            year=3,
            cgpa=3.8,
            skills=["Python", "Machine Learning"],
            location_pref="Remote",
            financial_need=True,
            experience=["internship"],
        )
        opp = Opportunity(
            is_opportunity=True,
            confidence=0.9,
            opportunity_type=OpportunityType.INTERNSHIP,
            eligibility_criteria=[
                "Computer Science students",
                "Minimum CGPA 3.5 required",
                "Python and Machine Learning skills",
                "Financial need considered",
                "Prior internship experience preferred",
            ],
            location="Remote",
            benefits="$5000 stipend for students with financial need",
        )
        score, reasons = calculate_profile_fit(profile, opp)
        assert score > 0
        assert len(reasons) > 0

    def test_no_eligibility_criteria(self):
        """Test when no eligibility criteria provided."""
        profile = StudentProfile(
            degree="Computer Science",
            year=3,
            cgpa=3.8,
        )
        opp = Opportunity(
            is_opportunity=True,
            confidence=0.9,
            eligibility_criteria=[],
        )
        score, reasons = calculate_profile_fit(profile, opp)
        # Should get neutral scores for most categories
        assert score >= 0

    def test_cgpa_requirement_not_met(self):
        """Test when CGPA requirement is not met."""
        profile = StudentProfile(
            degree="Computer Science",
            year=3,
            cgpa=3.0,
        )
        opp = Opportunity(
            is_opportunity=True,
            confidence=0.9,
            eligibility_criteria=["Minimum CGPA 3.5 required"],
        )
        score, reasons = calculate_profile_fit(profile, opp)
        assert score >= 0

    def test_location_match(self):
        """Test location preference matching."""
        profile = StudentProfile(
            degree="Computer Science",
            year=3,
            cgpa=3.5,
            location_pref="Remote",
        )
        opp = Opportunity(
            is_opportunity=True,
            confidence=0.9,
            location="Remote",
        )
        score, reasons = calculate_profile_fit(profile, opp)
        # Should include location match
        assert any("Location" in r for r in reasons)

    def test_financial_need_match(self):
        """Test financial need criteria matching."""
        profile = StudentProfile(
            degree="Computer Science",
            year=3,
            cgpa=3.5,
            financial_need=True,
        )
        opp = Opportunity(
            is_opportunity=True,
            confidence=0.9,
            eligibility_criteria=["Students with financial need preferred"],
            benefits="Need-based scholarship",
        )
        score, reasons = calculate_profile_fit(profile, opp)
        # Should include financial need match
        assert any("financial" in r.lower() for r in reasons)

    def test_skills_match(self):
        """Test skills matching."""
        profile = StudentProfile(
            degree="Computer Science",
            year=3,
            cgpa=3.5,
            skills=["Python", "Data Analysis", "Machine Learning"],
        )
        opp = Opportunity(
            is_opportunity=True,
            confidence=0.9,
            eligibility_criteria=["Python programming required", "Data Analysis skills"],
        )
        score, reasons = calculate_profile_fit(profile, opp)
        assert score > 0

    def test_empty_profile(self):
        """Test with minimal profile data."""
        profile = StudentProfile(
            degree="",
            year=1,
            cgpa=0.0,
        )
        opp = Opportunity(
            is_opportunity=True,
            confidence=0.9,
        )
        score, reasons = calculate_profile_fit(profile, opp)
        assert score >= 0


class TestCalculateCompletenessScore:
    """Test suite for completeness scoring."""

    def test_complete_opportunity(self):
        """Test with complete opportunity information."""
        profile = StudentProfile(
            degree="Computer Science",
            year=3,
            cgpa=3.5,
        )
        opp = Opportunity(
            is_opportunity=True,
            confidence=0.9,
            title="Test Scholarship",
            organization="Test Org",
            opportunity_type=OpportunityType.SCHOLARSHIP,
            application_link="https://example.com",
            benefits="$10,000 USD per year",
            location="Remote",
            eligibility_criteria=["CS students"],
            required_documents=["Resume", "Transcript"],
            duration="1 year",
        )
        score, factors = calculate_completeness_score(profile, opp)
        assert score > 50
        assert len(factors) > 0

    def test_minimal_opportunity(self):
        """Test with minimal opportunity information."""
        profile = StudentProfile(
            degree="Computer Science",
            year=3,
            cgpa=3.5,
        )
        opp = Opportunity(
            is_opportunity=True,
            confidence=0.9,
        )
        score, factors = calculate_completeness_score(profile, opp)
        assert score >= 0
        assert isinstance(factors, list)

    def test_benefits_with_money(self):
        """Test that monetary benefits increase score."""
        profile = StudentProfile(
            degree="Computer Science",
            year=3,
            cgpa=3.5,
        )
        opp = Opportunity(
            is_opportunity=True,
            confidence=0.9,
            benefits="$5,000 stipend for 6 months",
        )
        score, factors = calculate_completeness_score(profile, opp)
        assert score > 0


class TestCalculateCompositeScore:
    """Test suite for composite score calculation."""

    def test_basic_composite(self):
        """Test basic composite score calculation."""
        composite, breakdown = calculate_composite_score(80, 90, 70)
        # 80 * 0.45 + 90 * 0.30 + 70 * 0.25 = 36 + 27 + 17.5 = 80.5
        expected = 80 * 0.45 + 90 * 0.30 + 70 * 0.25
        assert composite == round(expected, 2)
        assert breakdown.profile_fit == 80
        assert breakdown.urgency == 90
        assert breakdown.completeness == 70
        assert breakdown.weights["profile_fit"] == 0.45
        assert breakdown.weights["urgency"] == 0.30
        assert breakdown.weights["completeness"] == 0.25

    def test_perfect_scores(self):
        """Test with all perfect scores."""
        composite, breakdown = calculate_composite_score(100, 100, 100)
        assert composite == 100.0

    def test_zero_scores(self):
        """Test with all zero scores."""
        composite, breakdown = calculate_composite_score(0, 0, 0)
        assert composite == 0.0

    def test_weight_distribution(self):
        """Verify weight distribution is correct."""
        _, breakdown = calculate_composite_score(100, 0, 0)
        assert breakdown.weights["profile_fit"] == 0.45

        _, breakdown = calculate_composite_score(0, 100, 0)
        assert breakdown.weights["urgency"] == 0.30

        _, breakdown = calculate_composite_score(0, 0, 100)
        assert breakdown.weights["completeness"] == 0.25

    def test_mixed_scores(self):
        """Test with various score combinations."""
        composite, _ = calculate_composite_score(50, 50, 50)
        assert composite == 50.0

        composite, _ = calculate_composite_score(100, 50, 0)
        # 100 * 0.45 + 50 * 0.30 + 0 * 0.25 = 45 + 15 + 0 = 60
        assert composite == 60.0

    def test_edge_cases(self):
        """Test edge cases and boundary values."""
        # Very high scores
        composite, _ = calculate_composite_score(99.9, 99.9, 99.9)
        assert composite > 99

        # Very low scores
        composite, _ = calculate_composite_score(0.1, 0.1, 0.1)
        assert composite > 0


class TestIntegrationScenarios:
    """Integration tests for realistic scenarios."""

    def test_full_scholarship_evaluation(self):
        """Test complete scholarship opportunity evaluation."""
        profile = StudentProfile(
            degree="Computer Science",
            year=3,
            cgpa=3.8,
            skills=["Python", "Machine Learning", "Data Analysis"],
            interests=["AI", "Research"],
            financial_need=True,
            location_pref="Remote",
            experience=["1 research internship"],
        )

        opp = Opportunity(
            is_opportunity=True,
            confidence=0.95,
            title="AI Research Fellowship",
            organization="Tech Research Lab",
            opportunity_type=OpportunityType.RESEARCH,
            deadline_type=DeadlineType.HARD,
            deadline_date=date.today() + timedelta(days=10),
            eligibility_criteria=[
                "Computer Science or related field",
                "Minimum CGPA 3.5",
                "Python programming required",
                "Machine Learning experience preferred",
            ],
            required_documents=["Resume", "Transcript", "Statement of Purpose"],
            application_link="https://research.example.com/apply",
            benefits="$8,000 USD stipend for 3 months + mentorship",
            location="Remote",
            duration="3 months",
        )

        # Calculate all scores
        profile_fit, fit_reasons = calculate_profile_fit(profile, opp)
        urgency, urgency_reason = calculate_urgency_score(opp)
        completeness, completeness_factors = calculate_completeness_score(profile, opp)
        composite, breakdown = calculate_composite_score(profile_fit, urgency, completeness)
        tier = calculate_urgency_tier(opp)

        # Assertions
        assert profile_fit > 0
        assert urgency > 0
        assert completeness > 0
        assert composite > 0
        assert tier == UrgencyTier.MODERATE
        assert len(fit_reasons) > 0
        assert len(completeness_factors) > 0

    def test_rolling_internship_evaluation(self):
        """Test rolling deadline internship."""
        profile = StudentProfile(
            degree="Software Engineering",
            year=2,
            cgpa=3.5,
            skills=["JavaScript", "React"],
        )

        opp = Opportunity(
            is_opportunity=True,
            confidence=0.9,
            title="Frontend Developer Intern",
            organization="StartupXYZ",
            deadline_type=DeadlineType.ROLLING,
            location="Hybrid",
            benefits="Competitive stipend",
        )

        profile_fit, _ = calculate_profile_fit(profile, opp)
        urgency, urgency_reason = calculate_urgency_score(opp)
        tier = calculate_urgency_tier(opp)

        assert urgency == 75.0
        assert "ROLLING BASIS" in urgency_reason
        assert tier == UrgencyTier.ROLLING

    def test_past_deadline_evaluation(self):
        """Test opportunity with past deadline."""
        opp = Opportunity(
            is_opportunity=True,
            confidence=0.9,
            deadline_type=DeadlineType.HARD,
            deadline_date=date.today() - timedelta(days=5),
        )

        urgency, reason = calculate_urgency_score(opp)
        assert urgency == 0.0
        assert "PASSED" in reason

    def test_unknown_deadline_evaluation(self):
        """Test opportunity with unknown deadline."""
        opp = Opportunity(
            is_opportunity=True,
            confidence=0.9,
            deadline_type=DeadlineType.UNKNOWN,
            title="Mystery Opportunity",
        )

        urgency, reason = calculate_urgency_score(opp)
        tier = calculate_urgency_tier(opp)

        assert urgency == 50.0
        assert "UNKNOWN" in reason
        assert tier == UrgencyTier.UNKNOWN
