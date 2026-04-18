"""Pydantic models for Opportunity Inbox Copilot."""

from datetime import date
from enum import Enum
from typing import List, Optional, Dict, Any

from pydantic import BaseModel, Field, ConfigDict


class DeadlineType(str, Enum):
    """5-tier enum for handling deadline ambiguity.

    The key innovation: instead of forcing every deadline into a datetime
    (and failing on 'rolling basis'), we classify ambiguity and handle
    each type with appropriate urgency scoring.
    """
    HARD = "hard"              # Specific date: "March 15, 2025"
    ROLLING = "rolling"          # "Rolling basis" - high urgency baseline
    SOFT_EARLY = "soft_early"    # "Early applications encouraged"
    RELATIVE = "relative"        # "End of month", "Next Friday"
    UNKNOWN = "unknown"          # No deadline mentioned


class UrgencyTier(str, Enum):
    """Visual urgency classification for UI display."""
    CRITICAL = "critical"        # <= 3 days
    URGENT = "urgent"            # 4-7 days
    MODERATE = "moderate"        # 8-30 days
    COMFORTABLE = "comfortable"    # 31-60 days
    ROLLING = "rolling"          # Rolling basis (special handling)
    UNKNOWN = "unknown"          # No deadline info


class OpportunityType(str, Enum):
    """Types of opportunities supported."""
    SCHOLARSHIP = "scholarship"
    INTERNSHIP = "internship"
    FELLOWSHIP = "fellowship"
    COMPETITION = "competition"
    RESEARCH = "research"
    JOB = "job"
    EXCHANGE = "exchange"
    OTHER = "other"


class StudentProfile(BaseModel):
    """Student profile for opportunity matching.

    Captures academic standing, skills, and preferences to enable
    personalized ranking of opportunities.
    """
    model_config = ConfigDict(strict=False)

    degree: str = Field(
        ...,
        description="Degree program (e.g., 'Computer Science', 'Mechanical Engineering')"
    )
    year: int = Field(
        ...,
        ge=1,
        le=8,
        description="Current year of study (1-8 for flexibility)"
    )
    cgpa: float = Field(
        ...,
        ge=0,
        le=4.0,
        description="Current CGPA on 4.0 scale"
    )
    skills: List[str] = Field(
        default_factory=list,
        description="Skills and competencies (e.g., ['Python', 'Machine Learning', 'Data Analysis'])"
    )
    interests: List[str] = Field(
        default_factory=list,
        description="Areas of interest (e.g., ['AI', 'Web Development', 'Robotics'])"
    )
    preferred_types: List[OpportunityType] = Field(
        default_factory=list,
        description="Types of opportunities to prioritize"
    )
    financial_need: bool = Field(
        default=False,
        description="Whether student has financial need for need-based opportunities"
    )
    location_pref: Optional[str] = Field(
        default=None,
        description="Location preference (e.g., 'Remote', 'Onsite', 'Hybrid', 'Europe', 'US')"
    )
    experience: List[str] = Field(
        default_factory=list,
        description="Prior experience (e.g., ['2 internships', '1 research project'])"
    )


class Opportunity(BaseModel):
    """Extracted opportunity from email.

    Represents a structured, LLM-extracted opportunity with all relevant
    metadata for scoring and ranking.
    """
    model_config = ConfigDict(strict=False)

    # Classification fields
    is_opportunity: bool = Field(
        ...,
        description="Whether this email represents a genuine actionable opportunity"
    )
    confidence: float = Field(
        ...,
        ge=0,
        le=1,
        description="Confidence score for classification (0-1)"
    )

    # Core opportunity info
    title: Optional[str] = Field(
        default=None,
        description="Title of the opportunity (e.g., 'Google Generation Scholarship')"
    )
    organization: Optional[str] = Field(
        default=None,
        description="Organization offering the opportunity"
    )
    opportunity_type: Optional[OpportunityType] = Field(
        default=None,
        description="Type of opportunity"
    )

    # Deadline handling with 5-tier enum
    deadline_type: DeadlineType = Field(
        default=DeadlineType.UNKNOWN,
        description="Type of deadline classification"
    )
    deadline_date: Optional[date] = Field(
        default=None,
        description="Parsed deadline date (only populated for HARD deadlines)"
    )
    deadline_text: Optional[str] = Field(
        default=None,
        description="Raw deadline text from email (for RELATIVE, ROLLING, etc.)"
    )

    # Eligibility and requirements
    eligibility_criteria: List[str] = Field(
        default_factory=list,
        description="List of eligibility requirements"
    )
    required_documents: List[str] = Field(
        default_factory=list,
        description="Documents required for application"
    )

    # Application details
    application_link: Optional[str] = Field(
        default=None,
        description="URL to application portal"
    )
    contact_email: Optional[str] = Field(
        default=None,
        description="Contact email for questions"
    )
    benefits: Optional[str] = Field(
        default=None,
        description="Benefits/award (e.g., '$10,000 scholarship', '$5,000/month stipend')"
    )
    location: Optional[str] = Field(
        default=None,
        description="Location of opportunity (e.g., 'Remote', 'Mountain View, CA')"
    )
    duration: Optional[str] = Field(
        default=None,
        description="Duration if applicable (e.g., '3 months', '1 year')"
    )

    # Evidence from source email
    raw_excerpts: List[str] = Field(
        default_factory=list,
        description="Evidence quotes from the source email supporting key claims"
    )

    # Reasoning for spam/opportunity classification
    classification_reason: Optional[str] = Field(
        default=None,
        description="Why this was classified as opportunity or not"
    )


class ScoreBreakdown(BaseModel):
    """Detailed scoring breakdown for transparency."""
    profile_fit: float = Field(..., ge=0, le=100)
    urgency: float = Field(..., ge=0, le=100)
    completeness: float = Field(..., ge=0, le=100)
    weights: Dict[str, float] = Field(default_factory=dict)


class RankedOpportunity(BaseModel):
    """Final ranked opportunity with scores and actions.

    The output of the pipeline - ready for UI display with all
    information needed for student decision-making.
    """
    model_config = ConfigDict(strict=False)

    opportunity: Opportunity = Field(..., description="The opportunity being ranked")
    composite_score: float = Field(
        ...,
        ge=0,
        le=100,
        description="Final composite score (0-100)"
    )
    scores: ScoreBreakdown = Field(..., description="Component scores")
    ranking_reasons: List[str] = Field(
        default_factory=list,
        description="Human-readable reasons for the ranking"
    )
    action_checklist: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Actionable next steps for this opportunity"
    )
    urgency_tier: Optional[UrgencyTier] = Field(
        default=None,
        description="Visual urgency classification"
    )

    # Calculated fields for display
    days_left: Optional[int] = Field(
        default=None,
        description="Days until deadline (for HARD deadlines)"
    )
