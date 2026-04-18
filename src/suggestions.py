"""Profile improvement suggestions for Opportunity Inbox Copilot.

This module provides AI-powered suggestions to help students improve their
profiles and qualify for more/better opportunities. It analyzes missed
opportunities, identifies skill gaps, and generates actionable recommendations.
"""

import logging
from typing import List, Dict, Any, Optional, Tuple
from collections import Counter

from src.models import StudentProfile, Opportunity, RankedOpportunity, DeadlineType
from src.scoring import calculate_profile_fit

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =============================================================================
# SKILL/REQUIREMENT EXTRACTION PATTERNS
# =============================================================================

# Common skills/technologies to look for in eligibility criteria
SKILL_PATTERNS = {
    "Programming Languages": [
        "python", "java", "javascript", "typescript", "c++", "c#", "golang", "rust",
        "ruby", "php", "swift", "kotlin", "matlab", "sql", "shell", "bash",
        "r programming", "r language",  # More specific R references
    ],
    "Web Technologies": [
        "react", "reactjs", "react.js", "angular", "vue", "vuejs", "node", "nodejs",
        "express", "django", "flask", "fastapi",
        "html", "css", "sass", "webpack", "next.js", "nuxt", "svelte"
    ],
    "Data & ML": [
        "machine learning", "deep learning", "data analysis", "data science",
        "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy", "keras",
        "nlp", "natural language", "computer vision", "artificial intelligence", "statistics"
    ],
    "Cloud & DevOps": [
        "aws", "azure", "gcp", "docker", "kubernetes", "ci/cd", "jenkins",
        "terraform", "ansible", "devops", "cloud computing", "serverless"
    ],
    "Databases": [
        "mysql", "postgresql", "mongodb", "redis", "elasticsearch", "sqlite",
        "oracle", "nosql", "database design", "database administration"
    ],
    "Tools & Practices": [
        "git", "agile", "scrum", "linux", "unix", "rest api", "graphql",
        "microservices", "testing", "tdd", "oop", "design patterns"
    ],
    "Soft Skills": [
        "leadership", "communication", "teamwork", "collaboration", "problem solving",
        "critical thinking", "creativity", "adaptability", "time management"
    ],
    "Domain Knowledge": [
        "cybersecurity", "blockchain", "iot", "robotics", "fintech", "healthtech",
        "edtech", "game development", "mobile development", "embedded systems"
    ],
}

# Common requirements that might disqualify users
REQUIREMENT_PATTERNS = {
    "cgpa": ["cgpa", "gpa", "minimum.*[0-3]\\.[0-9]", "grade.*average"],
    "year": ["year", "semester", "junior", "senior", "sophomore", "freshman", "graduate"],
    "experience": ["experience", "internship", "work", "years", "prior"],
    "degree": ["degree", "major", "field", "computer science", "engineering", "stem"],
    "documents": ["transcript", "recommendation", "resume", "cv", "portfolio", "essay"],
}


# =============================================================================
# GAP ANALYSIS
# =============================================================================

def analyze_missed_opportunities(
    missed_opportunities: List[Opportunity],
    user_profile: StudentProfile,
) -> List[Dict[str, Any]]:
    """Analyze opportunities the user didn't match well with.

    Identifies common patterns in eligibility criteria that the user lacks.

    Args:
        missed_opportunities: List of opportunities with low match scores
        user_profile: The user's current profile

    Returns:
        List of gap analysis items with:
        - gap_type: Category of gap (skill, cgpa, experience, etc.)
        - description: Human-readable description
        - frequency: How many opportunities have this requirement
        - impact: Estimated impact of addressing this gap
        - suggestions: Actionable suggestions to address the gap
    """
    if not missed_opportunities:
        return []

    gaps = []
    skill_counts = Counter()
    requirement_counts = Counter()

    # Analyze each missed opportunity
    for opp in missed_opportunities:
        criteria_text = " ".join(opp.eligibility_criteria).lower()

        # Extract skills mentioned
        for category, skills in SKILL_PATTERNS.items():
            for skill in skills:
                if skill in criteria_text:
                    skill_counts[skill] += 1

        # Extract requirements
        for req_type, patterns in REQUIREMENT_PATTERNS.items():
            for pattern in patterns:
                import re
                if re.search(pattern, criteria_text):
                    requirement_counts[req_type] += 1

    # Find skills user lacks
    user_skills_lower = [s.lower() for s in user_profile.skills]
    missing_skills = []
    for skill, count in skill_counts.most_common(10):
        if skill not in user_skills_lower and count >= 2:
            missing_skills.append({
                "skill": skill,
                "count": count,
                "category": _get_skill_category(skill),
            })

    # Build gap analysis
    if missing_skills:
        gaps.append({
            "gap_type": "skills",
            "description": f"Missing {len(missing_skills)} skills that appear in multiple opportunities",
            "frequency": sum(s["count"] for s in missing_skills),
            "impact": len(missing_skills) * 2,  # Estimated opportunities unlocked
            "details": missing_skills[:5],  # Top 5 missing skills
            "suggestions": _generate_skill_suggestions(missing_skills[:5]),
        })

    # Check CGPA gaps
    cgpa_gap = _analyze_cgpa_gap(missed_opportunities, user_profile)
    if cgpa_gap:
        gaps.append(cgpa_gap)

    # Check experience gaps
    exp_gap = _analyze_experience_gap(missed_opportunities, user_profile)
    if exp_gap:
        gaps.append(exp_gap)

    # Check document readiness
    doc_gap = _analyze_document_gap(missed_opportunities)
    if doc_gap:
        gaps.append(doc_gap)

    # Sort by impact
    gaps.sort(key=lambda x: x["impact"], reverse=True)

    return gaps


def _get_skill_category(skill: str) -> str:
    """Get the category for a skill."""
    skill_lower = skill.lower()
    for category, skills in SKILL_PATTERNS.items():
        if skill_lower in skills:
            return category
    return "Other"


def _analyze_cgpa_gap(
    missed_opportunities: List[Opportunity],
    user_profile: StudentProfile,
) -> Optional[Dict[str, Any]]:
    """Analyze if CGPA is a limiting factor."""
    import re

    cgpa_thresholds = []
    for opp in missed_opportunities:
        criteria_text = " ".join(opp.eligibility_criteria).lower()
        matches = re.findall(r"(?:cgpa|gpa).*?([0-3]\.[0-9])", criteria_text)
        for match in matches:
            try:
                threshold = float(match)
                if user_profile.cgpa < threshold:
                    cgpa_thresholds.append(threshold)
            except ValueError:
                pass

    if cgpa_thresholds:
        avg_threshold = sum(cgpa_thresholds) / len(cgpa_thresholds)
        return {
            "gap_type": "cgpa",
            "description": f"Your CGPA ({user_profile.cgpa}) is below average threshold ({avg_threshold:.2f})",
            "frequency": len(cgpa_thresholds),
            "impact": len(cgpa_thresholds),
            "details": {
                "your_cgpa": user_profile.cgpa,
                "avg_threshold": avg_threshold,
                "opportunities_affected": len(cgpa_thresholds),
            },
            "suggestions": [
                "Highlight relevant projects and achievements to offset CGPA",
                "Focus on opportunities without strict CGPA requirements",
                "Consider retaking key courses if feasible",
                "Emphasize upward grade trend in applications",
            ],
        }

    return None


def _analyze_experience_gap(
    missed_opportunities: List[Opportunity],
    user_profile: StudentProfile,
) -> Optional[Dict[str, Any]]:
    """Analyze if experience is a limiting factor."""
    exp_keywords = ["internship", "work experience", "years", "prior", "professional"]
    exp_mentioned = 0

    for opp in missed_opportunities:
        criteria_text = " ".join(opp.eligibility_criteria).lower()
        if any(kw in criteria_text for kw in exp_keywords):
            exp_mentioned += 1

    if exp_mentioned >= 2 and len(user_profile.experience) < 2:
        return {
            "gap_type": "experience",
            "description": "Limited experience may be affecting your match rate",
            "frequency": exp_mentioned,
            "impact": exp_mentioned,
            "details": {
                "your_experience_count": len(user_profile.experience),
                "opportunities_requiring_experience": exp_mentioned,
            },
            "suggestions": [
                "Start with internships or research positions to build experience",
                "Contribute to open-source projects",
                "Participate in hackathons and competitions",
                "Highlight academic projects as relevant experience",
            ],
        }

    return None


def _analyze_document_gap(
    missed_opportunities: List[Opportunity],
) -> Optional[Dict[str, Any]]:
    """Analyze document requirements across missed opportunities."""
    doc_counts = Counter()

    for opp in missed_opportunities:
        for doc in opp.required_documents:
            doc_lower = doc.lower()
            if "recommendation" in doc_lower:
                doc_counts["recommendation_letters"] += 1
            elif "transcript" in doc_lower:
                doc_counts["transcripts"] += 1
            elif "portfolio" in doc_lower:
                doc_counts["portfolio"] += 1
            elif "essay" in doc_lower or "statement" in doc_lower:
                doc_counts["essays"] += 1

    if doc_counts:
        most_common = doc_counts.most_common(3)
        return {
            "gap_type": "documents",
            "description": "Document preparation needed for applications",
            "frequency": sum(c for _, c in most_common),
            "impact": sum(c for _, c in most_common),
            "details": dict(most_common),
            "suggestions": _generate_document_suggestions(most_common),
        }

    return None


def _generate_skill_suggestions(missing_skills: List[Dict]) -> List[str]:
    """Generate actionable skill-building suggestions."""
    suggestions = []
    for skill_info in missing_skills:
        skill = skill_info["skill"]
        category = skill_info["category"]
        suggestions.append(f"Complete online course in {skill} (Coursera, edX, Udemy)")
        suggestions.append(f"Build a portfolio project demonstrating {skill}")

    return suggestions[:5]  # Limit to top 5


def _generate_document_suggestions(doc_counts: List[Tuple[str, int]]) -> List[str]:
    """Generate document preparation suggestions."""
    suggestions = []
    for doc_type, count in doc_counts:
        if doc_type == "recommendation_letters":
            suggestions.append("Identify 2-3 professors/references and request letters early")
        elif doc_type == "transcripts":
            suggestions.append("Request unofficial transcripts from registrar")
        elif doc_type == "portfolio":
            suggestions.append("Create GitHub portfolio showcasing your best projects")
        elif doc_type == "essays":
            suggestions.append("Draft template personal statement (500-750 words)")

    return suggestions


# =============================================================================
# PROFILE IMPROVEMENT SUGGESTIONS
# =============================================================================

def suggest_profile_improvements(
    user_profile: StudentProfile,
    all_opportunities: List[Opportunity],
) -> List[Tuple[str, int, str]]:
    """Generate specific, actionable profile improvement suggestions.

    Compares user profile against high-scoring opportunities to identify
    what changes would unlock more matches.

    Args:
        user_profile: The user's current profile
        all_opportunities: All available opportunities

    Returns:
        List of (suggestion, impact_count, priority) tuples where:
        - suggestion: Human-readable actionable suggestion
        - impact_count: Number of additional opportunities this would unlock
        - priority: "high", "medium", or "low"
    """
    suggestions = []

    # Separate high-scoring and low-scoring opportunities
    high_scoring = []
    low_scoring = []

    for opp in all_opportunities:
        score, _ = calculate_profile_fit(user_profile, opp)
        if score >= 70:
            high_scoring.append((opp, score))
        elif score >= 40:
            low_scoring.append((opp, score))

    # Analyze what skills appear in high-scoring but user lacks
    skill_impact = _calculate_skill_impact(user_profile, all_opportunities)
    for skill, impact in skill_impact.items():
        if impact >= 2:
            priority = "high" if impact >= 4 else "medium"
            suggestions.append((
                f"Add {skill.title()} to skills → unlocks {impact} more opportunities",
                impact,
                priority,
            ))

    # Check for experience-related suggestions
    exp_suggestions = _generate_experience_suggestions(user_profile, low_scoring)
    suggestions.extend(exp_suggestions)

    # Check for document-related suggestions
    doc_suggestions = _generate_document_priority_suggestions(user_profile, all_opportunities)
    suggestions.extend(doc_suggestions)

    # Check for CGPA-related framing suggestions
    cgpa_suggestions = _generate_cgpa_framing_suggestions(user_profile, all_opportunities)
    suggestions.extend(cgpa_suggestions)

    # Sort by impact
    suggestions.sort(key=lambda x: x[1], reverse=True)

    return suggestions


def _calculate_skill_impact(
    user_profile: StudentProfile,
    opportunities: List[Opportunity],
) -> Dict[str, int]:
    """Calculate how many more opportunities each skill would unlock."""
    user_skills_lower = set(s.lower() for s in user_profile.skills)
    skill_impact = Counter()

    for opp in opportunities:
        criteria_text = " ".join(opp.eligibility_criteria).lower()

        # Check if user currently matches
        current_match = any(skill in criteria_text for skill in user_skills_lower)

        if not current_match:
            # Check what single skill addition would create a match
            for category, skills in SKILL_PATTERNS.items():
                for skill in skills:
                    if skill not in user_skills_lower and skill in criteria_text:
                        skill_impact[skill] += 1

    return dict(skill_impact.most_common(10))


def _generate_experience_suggestions(
    user_profile: StudentProfile,
    low_scoring: List[Tuple[Opportunity, float]],
) -> List[Tuple[str, int, str]]:
    """Generate experience-related suggestions."""
    suggestions = []

    if len(user_profile.experience) < 2:
        # Count opportunities mentioning experience
        exp_opps = 0
        for opp, _ in low_scoring:
            criteria_text = " ".join(opp.eligibility_criteria).lower()
            if "experience" in criteria_text or "internship" in criteria_text:
                exp_opps += 1

        if exp_opps >= 2:
            suggestions.append((
                "Add internship or project experience → matches more experienced candidate profiles",
                exp_opps,
                "high",
            ))

    return suggestions


def _generate_document_priority_suggestions(
    user_profile: StudentProfile,
    opportunities: List[Opportunity],
) -> List[Tuple[str, int, str]]:
    """Generate document preparation suggestions."""
    doc_counts = Counter()

    for opp in opportunities:
        for doc in opp.required_documents:
            doc_lower = doc.lower()
            if "recommendation" in doc_lower:
                doc_counts["Recommendation letters ready"] += 1
            elif "portfolio" in doc_lower:
                doc_counts["Portfolio prepared"] += 1
            elif "transcript" in doc_lower:
                doc_counts["Transcripts available"] += 1

    suggestions = []
    for doc, count in doc_counts.most_common(3):
        if count >= 3:
            suggestions.append((
                f"Keep {doc.lower()} → required by {count} opportunities",
                count,
                "medium",
            ))

    return suggestions


def _generate_cgpa_framing_suggestions(
    user_profile: StudentProfile,
    opportunities: List[Opportunity],
) -> List[Tuple[str, int, str]]:
    """Generate suggestions for handling CGPA limitations."""
    if user_profile.cgpa < 3.0:
        # Count opportunities with CGPA requirements
        cgpa_opps = 0
        for opp in opportunities:
            criteria_text = " ".join(opp.eligibility_criteria).lower()
            if "cgpa" in criteria_text or "gpa" in criteria_text:
                cgpa_opps += 1

        if cgpa_opps > 0:
            return [(
                "CGPA below threshold for some opportunities → highlight projects and skills instead",
                cgpa_opps,
                "medium",
            )]

    return []


# =============================================================================
# MATCH POTENTIAL CALCULATION
# =============================================================================

def calculate_match_potential(
    user_profile: StudentProfile,
    opportunities: List[Opportunity],
    proposed_change: Dict[str, Any],
) -> Dict[str, Any]:
    """Calculate how many more opportunities would match with a proposed change.

    Args:
        user_profile: Current user profile
        opportunities: All available opportunities
        proposed_change: Dictionary with change details, e.g.:
            - {"type": "add_skill", "value": "Python"}
            - {"type": "add_experience", "value": "ML Internship"}
            - {"type": "improve_cgpa", "value": 3.5}

    Returns:
        Dictionary with:
        - current_matches: Number of opportunities currently matched
        - new_matches: Number of opportunities with proposed change
        - improvement: Difference
        - percentage_gain: Percentage improvement
        - specific_opportunities: Names of newly unlocked opportunities
    """
    # Calculate current matches
    current_matches = 0
    current_scores = []

    for opp in opportunities:
        score, _ = calculate_profile_fit(user_profile, opp)
        current_scores.append((opp, score))
        if score >= 50:  # Threshold for "match"
            current_matches += 1

    # Apply proposed change to create modified profile
    modified_profile = _apply_profile_change(user_profile, proposed_change)

    # Calculate new matches
    new_matches = 0
    new_scores = []
    newly_unlocked = []

    for opp in opportunities:
        score, _ = calculate_profile_fit(modified_profile, opp)
        new_scores.append((opp, score))
        if score >= 50:
            new_matches += 1
            # Check if this is newly unlocked
            old_score, _ = calculate_profile_fit(user_profile, opp)
            if old_score < 50:
                newly_unlocked.append(opp.title or "Untitled Opportunity")

    improvement = new_matches - current_matches
    percentage_gain = (improvement / len(opportunities) * 100) if opportunities else 0

    return {
        "current_matches": current_matches,
        "new_matches": new_matches,
        "improvement": improvement,
        "percentage_gain": round(percentage_gain, 1),
        "newly_unlocked": newly_unlocked[:5],  # Top 5 newly unlocked
        "change_description": _format_change_description(proposed_change),
    }


def _apply_profile_change(
    profile: StudentProfile,
    change: Dict[str, Any],
) -> StudentProfile:
    """Apply a proposed change to a profile."""
    # Create a copy by dict-ing the model
    profile_dict = profile.model_dump()

    change_type = change.get("type")
    value = change.get("value")

    if change_type == "add_skill":
        if value not in profile_dict["skills"]:
            profile_dict["skills"].append(value)
    elif change_type == "add_experience":
        if value not in profile_dict["experience"]:
            profile_dict["experience"].append(value)
    elif change_type == "improve_cgpa":
        profile_dict["cgpa"] = max(profile_dict["cgpa"], value)

    return StudentProfile(**profile_dict)


def _format_change_description(change: Dict[str, Any]) -> str:
    """Format a human-readable description of the proposed change."""
    change_type = change.get("type")
    value = change.get("value")

    if change_type == "add_skill":
        return f"Adding '{value}' to skills"
    elif change_type == "add_experience":
        return f"Adding '{value}' to experience"
    elif change_type == "improve_cgpa":
        return f"Improving CGPA to {value}"
    else:
        return f"Applying {change_type}: {value}"


# =============================================================================
# SKILL GAP ANALYSIS
# =============================================================================

def generate_skill_gap_analysis(
    user_profile: StudentProfile,
    opportunities: List[Opportunity],
) -> List[Dict[str, Any]]:
    """Compare user skills vs skills mentioned in opportunities.

    Finds most common missing skills and prioritizes by frequency and value.

    Args:
        user_profile: Current user profile
        opportunities: All available opportunities

    Returns:
        Ranked list of skills to learn with:
        - skill: The skill name
        - category: Skill category
        - frequency: How many opportunities mention it
        - current_match_rate: % of opportunities user matches without it
        - potential_match_rate: % of opportunities user would match with it
        - priority_score: Combined priority score (0-100)
        - learning_resources: Suggested learning paths
    """
    user_skills_lower = set(s.lower() for s in user_profile.skills)
    skill_stats = Counter()
    skill_opportunities = {}  # skill -> list of opps mentioning it

    import re

    # Collect skill statistics
    for opp in opportunities:
        criteria_text = " ".join(opp.eligibility_criteria).lower()

        for category, skills in SKILL_PATTERNS.items():
            for skill in skills:
                # Use word boundary matching for short skills (1-2 chars)
                if len(skill) <= 2:
                    # For short skills like "r", "go", "ai", use word boundaries
                    pattern = r'\b' + re.escape(skill) + r'\b'
                    if re.search(pattern, criteria_text):
                        skill_stats[skill] += 1
                        if skill not in skill_opportunities:
                            skill_opportunities[skill] = []
                        skill_opportunities[skill].append(opp)
                else:
                    # For longer skills, simple substring match is fine
                    if skill in criteria_text:
                        skill_stats[skill] += 1
                        if skill not in skill_opportunities:
                            skill_opportunities[skill] = []
                        skill_opportunities[skill].append(opp)

    # Build gap analysis for missing skills
    gap_analysis = []
    total_opps = len(opportunities)

    for skill, frequency in skill_stats.most_common(20):
        if skill not in user_skills_lower and frequency >= 2:
            # Calculate match rates
            related_opps = skill_opportunities.get(skill, [])

            # Current match rate (without this skill)
            current_matches = sum(
                1 for opp in related_opps
                if any(s.lower() in " ".join(opp.eligibility_criteria).lower()
                       for s in user_profile.skills)
            )
            current_rate = (current_matches / len(related_opps) * 100) if related_opps else 0

            # Potential match rate (with this skill)
            potential_rate = min(100, current_rate + 30)  # Estimate

            # Calculate priority score
            priority_score = _calculate_skill_priority(
                skill, frequency, current_rate, total_opps
            )

            gap_analysis.append({
                "skill": skill,
                "category": _get_skill_category(skill),
                "frequency": frequency,
                "percentage_of_opps": round(frequency / total_opps * 100, 1) if total_opps else 0,
                "current_match_rate": round(current_rate, 1),
                "potential_match_rate": round(potential_rate, 1),
                "priority_score": priority_score,
                "learning_resources": _get_learning_resources(skill),
            })

    # Sort by priority score
    gap_analysis.sort(key=lambda x: x["priority_score"], reverse=True)

    return gap_analysis[:10]  # Return top 10


def _calculate_skill_priority(
    skill: str,
    frequency: int,
    current_rate: float,
    total_opps: int,
) -> int:
    """Calculate priority score for a skill (0-100)."""
    # Base score from frequency
    freq_score = min(frequency / total_opps * 50, 50) if total_opps else 0

    # Bonus for low current match rate
    gap_bonus = (100 - current_rate) / 100 * 30

    # Bonus for high-demand skill categories
    category_bonus = 0
    if skill in SKILL_PATTERNS["Data & ML"]:
        category_bonus = 15
    elif skill in SKILL_PATTERNS["Programming Languages"]:
        category_bonus = 10
    elif skill in SKILL_PATTERNS["Web Technologies"]:
        category_bonus = 8

    return int(min(freq_score + gap_bonus + category_bonus, 100))


def _get_learning_resources(skill: str) -> List[str]:
    """Get suggested learning resources for a skill."""
    skill_lower = skill.lower()

    # General resources
    resources = [
        f"Complete '{skill} for Beginners' on Coursera",
        f"Build a portfolio project using {skill}",
        f"Practice {skill} on LeetCode/HackerRank",
    ]

    # Skill-specific additions
    if skill_lower in ["python", "java", "javascript"]:
        resources.insert(0, f"Official {skill} documentation and tutorials")
    elif skill_lower in ["machine learning", "deep learning"]:
        resources.insert(0, "Andrew Ng's ML Course on Coursera")
    elif skill_lower in ["aws", "azure", "gcp"]:
        resources.insert(0, f"Official {skill.upper()} Certification path")
    elif skill_lower in ["react", "angular", "vue"]:
        resources.insert(0, f"Build a full-stack project with {skill}")

    return resources[:4]


# =============================================================================
# TIMELINE SUGGESTIONS
# =============================================================================

def generate_timeline_suggestions(
    user_profile: StudentProfile,
    opportunities: List[Opportunity],
    reference_date: Optional[Any] = None,
) -> List[Dict[str, Any]]:
    """Generate timeline-based suggestions for opportunity preparation.

    Based on deadlines, suggests when to:
    - Start working on missing skills
    - Request recommendation letters
    - Draft application essays

    Args:
        user_profile: Current user profile
        opportunities: All available opportunities
        reference_date: Reference date for calculations (defaults to today)

    Returns:
        List of timeline milestones with:
        - deadline_date: Target date
        - milestone: What to accomplish
        - opportunities: Related opportunities
        - urgency: "critical", "high", "medium", "low"
        - estimated_hours: Estimated time required
    """
    from datetime import date, timedelta

    if reference_date is None:
        reference_date = date.today()

    milestones = []

    # Group opportunities by deadline
    deadline_groups = {
        "critical": [],  # <= 7 days
        "urgent": [],    # 8-30 days
        "upcoming": [],  # 31-60 days
        "future": [],    # > 60 days
    }

    for opp in opportunities:
        if opp.deadline_type == DeadlineType.HARD and opp.deadline_date:
            days_left = (opp.deadline_date - reference_date).days

            if days_left <= 7:
                deadline_groups["critical"].append(opp)
            elif days_left <= 30:
                deadline_groups["urgent"].append(opp)
            elif days_left <= 60:
                deadline_groups["upcoming"].append(opp)
            else:
                deadline_groups["future"].append(opp)
        elif opp.deadline_type == DeadlineType.ROLLING:
            # Rolling deadlines should be treated as urgent
            deadline_groups["urgent"].append(opp)

    # Generate milestones for each time period

    # Immediate (this week)
    if deadline_groups["critical"]:
        milestones.append({
            "timeframe": "This Week",
            "deadline_date": reference_date + timedelta(days=7),
            "milestone": "Finalize and submit applications for critical deadlines",
            "opportunities": [opp.title for opp in deadline_groups["critical"][:3]],
            "urgency": "critical",
            "estimated_hours": 15,
            "actions": [
                "Complete application forms",
                "Gather all required documents",
                "Review and proofread everything",
                "Submit before deadline",
            ],
        })

    # Short-term (next 2-4 weeks)
    if deadline_groups["urgent"] or deadline_groups["critical"]:
        all_urgent = deadline_groups["urgent"] + deadline_groups["critical"]
        milestones.append({
            "timeframe": "Next 2-4 Weeks",
            "deadline_date": reference_date + timedelta(days=30),
            "milestone": "Prepare applications for urgent deadlines",
            "opportunities": [opp.title for opp in all_urgent[:5]],
            "urgency": "high",
            "estimated_hours": 25,
            "actions": [
                "Request recommendation letters NOW (give 2+ weeks notice)",
                "Draft personal statements",
                "Update resume/CV",
                "Request transcripts",
            ],
        })

    # Medium-term (1-2 months)
    if deadline_groups["upcoming"]:
        milestones.append({
            "timeframe": "1-2 Months",
            "deadline_date": reference_date + timedelta(days=60),
            "milestone": "Build skills and prepare for upcoming deadlines",
            "opportunities": [opp.title for opp in deadline_groups["upcoming"][:5]],
            "urgency": "medium",
            "estimated_hours": 40,
            "actions": [
                "Start intensive skill-building for missing requirements",
                "Draft and revise application essays",
                "Build portfolio projects",
                "Network with potential references",
            ],
        })

    # Long-term (3+ months)
    if deadline_groups["future"]:
        milestones.append({
            "timeframe": "3+ Months",
            "deadline_date": reference_date + timedelta(days=90),
            "milestone": "Long-term profile building",
            "opportunities": [opp.title for opp in deadline_groups["future"][:5]],
            "urgency": "low",
            "estimated_hours": 100,
            "actions": [
                "Enroll in courses for key missing skills",
                "Secure internships or research positions",
                "Build substantial portfolio projects",
                "Cultivate relationships with potential references",
            ],
        })

    # Note: Rolling deadline opportunities are already added to "urgent" group
    # No separate handling needed since they're treated with high priority

    # Sort by urgency
    urgency_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    milestones.sort(key=lambda x: urgency_order.get(x["urgency"], 4))

    return milestones


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def get_skill_suggestion_for_demo(
    skill: str,
    opportunities: List[Opportunity],
) -> Dict[str, Any]:
    """Get a formatted skill suggestion for demo purposes."""
    count = sum(
        1 for opp in opportunities
        if skill.lower() in " ".join(opp.eligibility_criteria).lower()
    )

    return {
        "skill": skill,
        "unlocks": count,
        "message": f"Add {skill} → unlocks {count} more opportunities",
        "priority": "high" if count >= 3 else "medium",
    }


def format_impact_summary(
    current_matches: int,
    potential_matches: int,
    total_opportunities: int,
) -> str:
    """Format a human-readable impact summary."""
    improvement = potential_matches - current_matches
    percentage = (improvement / total_opportunities * 100) if total_opportunities else 0

    return (
        f"You currently match {current_matches}/{total_opportunities} opportunities. "
        f"With recommended improvements, you could match {potential_matches}/{total_opportunities} "
        f"(+{improvement}, +{percentage:.0f}%)"
    )
