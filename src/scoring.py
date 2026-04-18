"""Deterministic scoring engine for Opportunity Inbox Copilot.

This module provides deterministic (non-LLM) scoring functions for ranking
opportunities based on profile fit, urgency, and completeness.
"""

from datetime import date
from typing import List, Tuple, Optional

from src.models import (
    StudentProfile,
    Opportunity,
    DeadlineType,
    UrgencyTier,
    ScoreBreakdown,
)


def calculate_profile_fit(
    profile: StudentProfile,
    opportunity: Opportunity,
) -> Tuple[float, List[str]]:
    """Calculate profile fit score (0-100) with detailed reasons.

    Scoring breakdown:
    - Degree match: 10 pts (exact = 10, related = 5, no match = 0)
    - CGPA threshold: 10 pts (if CGPA >= min_required)
    - Skills overlap: 10 pts (based on matching)
    - Location: 5 pts (match with preference)
    - Financial need: 5 pts (opportunity mentions need + profile has it)
    - Experience: 5 pts (profile matches requirements)

    Args:
        profile: Student's profile with academic and personal info
        opportunity: Opportunity to evaluate against profile

    Returns:
        Tuple of (score 0-100, list of reason strings)
    """
    score = 0.0
    reasons = []

    # Degree match: 10 points
    degree_score = _calculate_degree_match(profile, opportunity)
    score += degree_score
    if degree_score >= 10:
        reasons.append(f"Degree match: {profile.degree} aligns with opportunity requirements")
    elif degree_score >= 5:
        reasons.append(f"Related degree: {profile.degree} may be relevant")

    # CGPA threshold: 10 points
    cgpa_score = _calculate_cgpa_match(profile, opportunity)
    score += cgpa_score
    if cgpa_score >= 10:
        reasons.append(f"CGPA {profile.cgpa} meets eligibility requirements")
    elif cgpa_score >= 5:
        reasons.append("CGPA partially meets requirements")

    # Skills overlap: 10 points
    skills_score = _calculate_skills_match(profile, opportunity)
    score += skills_score
    if skills_score >= 8:
        reasons.append(f"Strong skills match ({int(skills_score)}/10 points)")
    elif skills_score >= 4:
        reasons.append(f"Moderate skills overlap ({int(skills_score)}/10 points)")

    # Location: 5 points
    location_score = _calculate_location_match(profile, opportunity)
    score += location_score
    if location_score >= 5:
        reasons.append(f"Location preference match: {profile.location_pref}")

    # Financial need: 5 points
    financial_score = _calculate_financial_match(profile, opportunity)
    score += financial_score
    if financial_score >= 5:
        reasons.append("Financial need criteria met")

    # Experience: 5 points
    experience_score = _calculate_experience_match(profile, opportunity)
    score += experience_score
    if experience_score >= 5:
        reasons.append("Experience matches opportunity requirements")
    elif experience_score >= 2:
        reasons.append("Some relevant experience")

    return min(score, 100.0), reasons


def _calculate_degree_match(profile: StudentProfile, opportunity: Opportunity) -> float:
    """Calculate degree match score (0-10)."""
    if not opportunity.eligibility_criteria:
        return 5.0  # Neutral if no criteria specified

    criteria_text = " ".join(opportunity.eligibility_criteria).lower()
    degree_lower = profile.degree.lower()

    # Direct match
    if degree_lower in criteria_text:
        return 10.0

    # Related field matching
    related_fields = {
        "computer": ["software", "programming", "cs", "it", "technology"],
        "engineering": ["technical", "stem", "technology"],
        "business": ["management", "administration", "commerce"],
        "science": ["stem", "research", "technical"],
    }

    for field, related in related_fields.items():
        if field in degree_lower:
            for rel in related:
                if rel in criteria_text:
                    return 5.0

    return 0.0


def _calculate_cgpa_match(profile: StudentProfile, opportunity: Opportunity) -> float:
    """Calculate CGPA match score (0-10)."""
    if not opportunity.eligibility_criteria:
        return 5.0  # Neutral if no criteria

    criteria_text = " ".join(opportunity.eligibility_criteria).lower()

    # Look for CGPA requirements
    import re
    cgpa_patterns = [
        r"(?:cgpa|gpa).*?([0-3]\.[0-9])",
        r"minimum.*?gpa.*?([0-3]\.[0-9])",
        r"gpa.*?([0-3]\.[0-9]).*?required",
    ]

    min_cgpa = None
    for pattern in cgpa_patterns:
        match = re.search(pattern, criteria_text)
        if match:
            try:
                min_cgpa = float(match.group(1))
                break
            except ValueError:
                continue

    if min_cgpa is None:
        return 5.0  # Neutral if can't parse

    if profile.cgpa >= min_cgpa:
        return 10.0
    elif profile.cgpa >= min_cgpa - 0.5:
        return 5.0
    else:
        return 0.0


def _calculate_skills_match(profile: StudentProfile, opportunity: Opportunity) -> float:
    """Calculate skills match score (0-10) using Jaccard-like similarity."""
    if not opportunity.eligibility_criteria:
        return 5.0  # Neutral if no criteria

    criteria_text = " ".join(opportunity.eligibility_criteria).lower()
    profile_skills = [s.lower() for s in profile.skills]

    if not profile_skills:
        return 0.0

    matches = 0
    for skill in profile_skills:
        if skill in criteria_text:
            matches += 1

    # Score based on proportion of skills that match
    match_ratio = matches / len(profile_skills)
    return min(match_ratio * 10, 10.0)


def _calculate_location_match(profile: StudentProfile, opportunity: Opportunity) -> float:
    """Calculate location match score (0-5)."""
    if not profile.location_pref or not opportunity.location:
        return 2.5  # Neutral

    profile_loc = profile.location_pref.lower()
    opp_loc = opportunity.location.lower()

    # Direct match
    if profile_loc in opp_loc or opp_loc in profile_loc:
        return 5.0

    # Remote preference matches any remote opportunity
    if "remote" in profile_loc and "remote" in opp_loc:
        return 5.0

    return 0.0


def _calculate_financial_match(profile: StudentProfile, opportunity: Opportunity) -> float:
    """Calculate financial need match score (0-5)."""
    if not profile.financial_need:
        return 0.0

    # Check if opportunity mentions financial need
    all_text = " ".join(opportunity.eligibility_criteria).lower()
    if opportunity.benefits:
        all_text += " " + opportunity.benefits.lower()

    financial_keywords = ["financial need", "need-based", "merit-cum-means", "economic need"]
    for keyword in financial_keywords:
        if keyword in all_text:
            return 5.0

    return 0.0


def _calculate_experience_match(profile: StudentProfile, opportunity: Opportunity) -> float:
    """Calculate experience match score (0-5)."""
    if not opportunity.eligibility_criteria:
        return 2.5  # Neutral

    if not profile.experience:
        return 0.0

    criteria_text = " ".join(opportunity.eligibility_criteria).lower()
    exp_score = 0.0

    for exp in profile.experience:
        exp_lower = exp.lower()
        # Check if experience keywords appear in criteria
        if any(word in criteria_text for word in exp_lower.split()):
            exp_score += 2.5

    return min(exp_score, 5.0)


def calculate_urgency_score(
    opportunity: Opportunity,
    reference_date: Optional[date] = None,
) -> Tuple[float, str]:
    """Calculate urgency score (0-100) with explanation.

    DeadlineType handling:
    - HARD: Calculate days_left from deadline_date
      * days_left < 0: 0 pts ("Deadline passed")
      * days_left <= 3: 100 pts ("CRITICAL: X days left")
      * days_left <= 7: 90 pts ("URGENT: X days left")
      * days_left <= 30: 70 pts ("MODERATE: X days left")
      * days_left <= 60: 40 pts ("COMFORTABLE: X days left")
      * else: 20 pts ("X days left")
    - ROLLING: 75 pts baseline ("ROLLING BASIS: Apply ASAP")
    - SOFT_EARLY: 65 pts baseline ("EARLY PRIORITY: Earlier = better")
    - RELATIVE: 60 pts baseline ("RELATIVE: verify actual date")
    - UNKNOWN: 50 pts baseline ("DEADLINE UNKNOWN: check portal")

    Args:
        opportunity: Opportunity to evaluate
        reference_date: Date to calculate from (defaults to today)

    Returns:
        Tuple of (score 0-100, explanation string)
    """
    if reference_date is None:
        reference_date = date.today()

    deadline_type = opportunity.deadline_type

    if deadline_type == DeadlineType.HARD:
        return _calculate_hard_deadline_score(opportunity, reference_date)
    elif deadline_type == DeadlineType.ROLLING:
        return 75.0, "ROLLING BASIS: Apply ASAP"
    elif deadline_type == DeadlineType.SOFT_EARLY:
        return 65.0, "EARLY PRIORITY: Earlier applications have better chances"
    elif deadline_type == DeadlineType.RELATIVE:
        return 60.0, "RELATIVE DEADLINE: Verify actual date on portal"
    else:  # UNKNOWN
        return 50.0, "DEADLINE UNKNOWN: Check portal for details"


def _calculate_hard_deadline_score(
    opportunity: Opportunity,
    reference_date: date,
) -> Tuple[float, str]:
    """Calculate urgency score for HARD deadlines."""
    if opportunity.deadline_date is None:
        return 50.0, "DEADLINE PARSED: Date unavailable"

    days_left = (opportunity.deadline_date - reference_date).days

    if days_left < 0:
        return 0.0, f"DEADLINE PASSED: {abs(days_left)} days ago"
    elif days_left <= 3:
        return 100.0, f"CRITICAL: {days_left} days left"
    elif days_left <= 7:
        return 90.0, f"URGENT: {days_left} days left"
    elif days_left <= 30:
        return 70.0, f"MODERATE: {days_left} days left"
    elif days_left <= 60:
        return 40.0, f"COMFORTABLE: {days_left} days left"
    else:
        return 20.0, f"{days_left} days left - Plenty of time"


def calculate_urgency_tier(
    opportunity: Opportunity,
    reference_date: Optional[date] = None,
) -> UrgencyTier:
    """Calculate urgency tier based on deadline.

    - CRITICAL: <= 3 days
    - URGENT: 4-7 days
    - MODERATE: 8-30 days
    - COMFORTABLE: 31-60 days
    - ROLLING: if deadline_type is ROLLING
    - UNKNOWN: if deadline_type is UNKNOWN

    Args:
        opportunity: Opportunity to evaluate
        reference_date: Date to calculate from (defaults to today)

    Returns:
        UrgencyTier enum value
    """
    if reference_date is None:
        reference_date = date.today()

    deadline_type = opportunity.deadline_type

    if deadline_type == DeadlineType.ROLLING:
        return UrgencyTier.ROLLING
    elif deadline_type == DeadlineType.UNKNOWN:
        return UrgencyTier.UNKNOWN
    elif deadline_type == DeadlineType.HARD and opportunity.deadline_date:
        days_left = (opportunity.deadline_date - reference_date).days

        if days_left <= 3:
            return UrgencyTier.CRITICAL
        elif days_left <= 7:
            return UrgencyTier.URGENT
        elif days_left <= 30:
            return UrgencyTier.MODERATE
        else:
            return UrgencyTier.COMFORTABLE
    else:
        # For SOFT_EARLY and RELATIVE, use moderate urgency
        return UrgencyTier.MODERATE


def calculate_completeness_score(
    profile: StudentProfile,
    opportunity: Opportunity,
) -> Tuple[float, List[str]]:
    """Calculate completeness score (0-100) with factors.

    Scoring breakdown:
    - Info completeness: 10 pts (% of key fields populated)
    - Docs match: 10 pts (how many required docs student likely has)
    - Value clarity: 5 pts (benefits/stipend mentioned)

    Args:
        profile: Student's profile
        opportunity: Opportunity to evaluate

    Returns:
        Tuple of (score 0-100, list of factor strings)
    """
    score = 0.0
    factors = []

    # Info completeness: 35 points (adjusted from 10 to give more weight)
    info_score = _calculate_info_completeness(opportunity)
    score += info_score
    if info_score >= 30:
        factors.append(f"Complete opportunity info ({int(info_score)}/35)")
    elif info_score >= 15:
        factors.append(f"Partial opportunity info ({int(info_score)}/35)")

    # Documents match: 35 points (adjusted from 10)
    docs_score = _calculate_documents_match(profile, opportunity)
    score += docs_score
    if docs_score >= 30:
        factors.append(f"All required documents likely available ({int(docs_score)}/35)")
    elif docs_score >= 15:
        factors.append(f"Some documents may be ready ({int(docs_score)}/35)")

    # Value clarity: 30 points (adjusted from 5)
    value_score = _calculate_value_clarity(opportunity)
    score += value_score
    if value_score >= 25:
        factors.append(f"Clear benefits/value stated ({int(value_score)}/30)")

    return min(score, 100.0), factors


def _calculate_info_completeness(opportunity: Opportunity) -> float:
    """Calculate information completeness score (0-35)."""
    key_fields = [
        opportunity.title,
        opportunity.organization,
        opportunity.opportunity_type,
        opportunity.application_link,
        opportunity.benefits,
        opportunity.location,
    ]

    eligibility_fields = [
        opportunity.eligibility_criteria,
        opportunity.required_documents,
    ]

    # Count populated fields
    populated = sum(1 for f in key_fields if f is not None)
    populated += sum(1 for f in eligibility_fields if len(f) > 0)

    total_fields = len(key_fields) + len(eligibility_fields)
    ratio = populated / total_fields if total_fields > 0 else 0

    return ratio * 35


def _calculate_documents_match(
    profile: StudentProfile,
    opportunity: Opportunity,
) -> float:
    """Calculate documents match score (0-35)."""
    if not opportunity.required_documents:
        return 17.5  # Neutral if no docs required

    # Common documents students typically have
    common_docs = [
        "resume", "cv", "transcript", "portfolio", "id", "identification",
        "recommendation", "reference", "letter", "essay", "statement",
        "cover letter", "application form",
    ]

    # Check how many required docs are common
    required = [d.lower() for d in opportunity.required_documents]
    matches = sum(1 for req in required if any(cd in req for cd in common_docs))

    ratio = matches / len(required) if required else 1.0
    return ratio * 35


def _calculate_value_clarity(opportunity: Opportunity) -> float:
    """Calculate value clarity score (0-30)."""
    score = 0.0

    if opportunity.benefits:
        score += 15.0
        benefits_lower = opportunity.benefits.lower()
        # Bonus for specific monetary values
        import re
        if re.search(r"\$[\d,]+", benefits_lower) or re.search(r"\d+\s*(?:usd|gbp|eur)", benefits_lower):
            score += 10.0
        if re.search(r"\d+\s*(?:month|year|week)", benefits_lower):
            score += 5.0

    if opportunity.duration:
        score += 5.0

    return min(score, 30.0)


def calculate_composite_score(
    profile_fit: float,
    urgency: float,
    completeness: float,
) -> Tuple[float, ScoreBreakdown]:
    """Calculate composite score with weighted components.

    Weights:
    - profile_fit: 0.45 (45%)
    - urgency: 0.30 (30%)
    - completeness: 0.25 (25%)

    Args:
        profile_fit: Profile fit score (0-100)
        urgency: Urgency score (0-100)
        completeness: Completeness score (0-100)

    Returns:
        Tuple of (composite_score, ScoreBreakdown)
    """
    weights = {
        "profile_fit": 0.45,
        "urgency": 0.30,
        "completeness": 0.25,
    }

    composite = (
        profile_fit * weights["profile_fit"] +
        urgency * weights["urgency"] +
        completeness * weights["completeness"]
    )

    breakdown = ScoreBreakdown(
        profile_fit=profile_fit,
        urgency=urgency,
        completeness=completeness,
        weights=weights,
    )

    return round(composite, 2), breakdown
