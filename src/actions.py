"""Action checklist generator for Opportunity Inbox Copilot.

This module generates actionable checklists for students based on
extracted opportunities and their student profile. Actions are categorized
by type and assigned priority levels to help students focus on what matters.
"""

from typing import List, Dict, Any, Optional
from datetime import date

from src.models import Opportunity, StudentProfile, DeadlineType
from src.utils import calculate_days_left


# Document type to action description mappings
DOCUMENT_ACTIONS = {
    "transcript": {
        "description": "Request unofficial transcript from registrar",
        "priority": "high"
    },
    "transcripts": {
        "description": "Request unofficial transcript from registrar",
        "priority": "high"
    },
    "resume": {
        "description": "Update resume with relevant projects",
        "priority": "high"
    },
    "cv": {
        "description": "Update CV with recent achievements",
        "priority": "high"
    },
    "recommendation": {
        "description": "Contact professor for recommendation letter",
        "priority": "high"
    },
    "recommendations": {
        "description": "Contact professors for recommendation letters",
        "priority": "high"
    },
    "recommendation letter": {
        "description": "Contact professor for recommendation letter",
        "priority": "high"
    },
    "personal statement": {
        "description": "Draft personal statement (500 words)",
        "priority": "medium"
    },
    "statement of purpose": {
        "description": "Draft statement of purpose",
        "priority": "medium"
    },
    "cover letter": {
        "description": "Write tailored cover letter",
        "priority": "medium"
    },
    "essay": {
        "description": "Prepare application essay",
        "priority": "medium"
    },
    "portfolio": {
        "description": "Prepare portfolio of relevant work",
        "priority": "medium"
    },
    "writing sample": {
        "description": "Prepare writing sample submission",
        "priority": "medium"
    },
}


def create_action_item(
    category: str,
    description: str,
    priority: str = "medium"
) -> Dict[str, Any]:
    """Create a standardized action item dictionary.

    Args:
        category: Type of action (document, step, urgency_message, link)
        description: Human-readable description of the action
        priority: Priority level (high, medium, low)

    Returns:
        Dictionary representing the action item
    """
    return {
        "category": category,
        "description": description,
        "completed": False,
        "priority": priority
    }


def generate_document_checklist(opportunity: Opportunity) -> List[Dict[str, Any]]:
    """Generate checklist items based on required documents from the opportunity.

    Maps common document types to specific actionable steps with appropriate
    priorities. Falls back to generic actions for unrecognized document types.

    Args:
        opportunity: The opportunity containing required_documents

    Returns:
        List of action items for document preparation
    """
    actions = []
    seen_descriptions = set()  # Avoid duplicates

    for doc in opportunity.required_documents:
        doc_lower = doc.lower().strip()

        # Try to find exact match first
        if doc_lower in DOCUMENT_ACTIONS:
            action_info = DOCUMENT_ACTIONS[doc_lower]
            if action_info["description"] not in seen_descriptions:
                actions.append(create_action_item(
                    category="document",
                    description=action_info["description"],
                    priority=action_info["priority"]
                ))
                seen_descriptions.add(action_info["description"])
        else:
            # Try partial matches
            matched = False
            for key, action_info in DOCUMENT_ACTIONS.items():
                if key in doc_lower:
                    if action_info["description"] not in seen_descriptions:
                        actions.append(create_action_item(
                            category="document",
                            description=action_info["description"],
                            priority=action_info["priority"]
                        ))
                        seen_descriptions.add(action_info["description"])
                    matched = True
                    break

            # Fallback for unrecognized documents
            if not matched:
                fallback_desc = f"Prepare: {doc}"
                if fallback_desc not in seen_descriptions:
                    actions.append(create_action_item(
                        category="document",
                        description=fallback_desc,
                        priority="medium"
                    ))
                    seen_descriptions.add(fallback_desc)

    return actions


def generate_deadline_actions(opportunity: Opportunity) -> List[Dict[str, Any]]:
    """Generate deadline-aware actions based on opportunity deadline type.

    Creates urgency-appropriate actions:
    - HARD deadlines within 3 days: Critical urgency messages
    - HARD deadlines within 7 days: Start this week message
    - ROLLING: Apply ASAP message
    - SOFT_EARLY: Submit early for priority consideration
    - UNKNOWN: Verify deadline message

    Args:
        opportunity: The opportunity with deadline information

    Returns:
        List of deadline-related action items
    """
    actions = []

    if opportunity.deadline_type == DeadlineType.HARD:
        if opportunity.deadline_date:
            days_left = calculate_days_left(opportunity.deadline_date)

            if days_left <= 3 and days_left >= 0:
                # Critical urgency
                actions.append(create_action_item(
                    category="urgency_message",
                    description="URGENT: Submit application TODAY",
                    priority="high"
                ))
                actions.append(create_action_item(
                    category="step",
                    description="Set reminder for 24 hours before deadline",
                    priority="high"
                ))
            elif days_left <= 7 and days_left >= 0:
                # Urgent but manageable
                actions.append(create_action_item(
                    category="urgency_message",
                    description="Start application process this week",
                    priority="high"
                ))
            elif days_left < 0:
                # Deadline passed
                actions.append(create_action_item(
                    category="urgency_message",
                    description="DEADLINE PASSED: Check if extensions are available",
                    priority="high"
                ))
        else:
            # Hard deadline without date
            actions.append(create_action_item(
                category="urgency_message",
                description="Confirm exact deadline date on official portal",
                priority="high"
            ))

    elif opportunity.deadline_type == DeadlineType.ROLLING:
        actions.append(create_action_item(
            category="urgency_message",
            description="Apply ASAP - rolling basis means spots fill quickly",
            priority="high"
        ))

    elif opportunity.deadline_type == DeadlineType.SOFT_EARLY:
        actions.append(create_action_item(
            category="urgency_message",
            description="Submit early for priority consideration",
            priority="medium"
        ))

    elif opportunity.deadline_type == DeadlineType.RELATIVE:
        if opportunity.deadline_text:
            actions.append(create_action_item(
                category="urgency_message",
                description=f"Deadline is relative: {opportunity.deadline_text}",
                priority="medium"
            ))
        actions.append(create_action_item(
            category="step",
            description="Pinpoint exact deadline date",
            priority="medium"
        ))

    elif opportunity.deadline_type == DeadlineType.UNKNOWN:
        actions.append(create_action_item(
            category="urgency_message",
            description="Verify deadline on official portal",
            priority="medium"
        ))

    return actions


def generate_application_steps(opportunity: Opportunity) -> List[Dict[str, Any]]:
    """Generate step-by-step application guide.

    Creates a standard 5-step application process with opportunity-specific
    details like application links and contact information.

    Args:
        opportunity: The opportunity with application details

    Returns:
        List of step-by-step action items
    """
    actions = []

    # Step 1: Visit application portal
    if opportunity.application_link:
        actions.append(create_action_item(
            category="link",
            description=f"Visit application portal: {opportunity.application_link}",
            priority="high"
        ))
    else:
        actions.append(create_action_item(
            category="step",
            description="Find and visit official application portal",
            priority="high"
        ))

    # Step 2: Account creation
    actions.append(create_action_item(
        category="step",
        description="Create account or log in",
        priority="medium"
    ))

    # Step 3: Personal information
    actions.append(create_action_item(
        category="step",
        description="Complete personal information section",
        priority="medium"
    ))

    # Step 4: Document upload
    if opportunity.required_documents:
        actions.append(create_action_item(
            category="step",
            description="Upload required documents",
            priority="high"
        ))
    else:
        actions.append(create_action_item(
            category="step",
            description="Review and upload any additional documents",
            priority="low"
        ))

    # Step 5: Submission
    if opportunity.deadline_type == DeadlineType.HARD and opportunity.deadline_date:
        days_left = calculate_days_left(opportunity.deadline_date)
        if days_left >= 0:
            actions.append(create_action_item(
                category="step",
                description=f"Submit before deadline ({days_left} days left)",
                priority="high"
            ))
        else:
            actions.append(create_action_item(
                category="step",
                description="Deadline has passed - verify opportunity status",
                priority="high"
            ))
    else:
        actions.append(create_action_item(
            category="step",
            description="Submit before deadline",
            priority="high"
        ))

    return actions


def generate_profile_specific_tips(
    opportunity: Opportunity,
    profile: StudentProfile
) -> List[Dict[str, Any]]:
    """Generate personalized tips based on student profile.

    Analyzes the student profile against opportunity requirements to provide
    tailored advice about skills to highlight or gaps to address.

    Args:
        opportunity: The opportunity to check against
        profile: The student's profile

    Returns:
        List of personalized tip action items
    """
    actions = []

    # Check eligibility criteria for profile alignment
    if opportunity.eligibility_criteria:
        for criterion in opportunity.eligibility_criteria:
            criterion_lower = criterion.lower()

            # Check for CGPA requirements
            if "gpa" in criterion_lower or "cgpa" in criterion_lower:
                actions.append(create_action_item(
                    category="step",
                    description=f"Verify your CGPA meets requirement: {criterion}",
                    priority="medium"
                ))

            # Check for year requirements
            if "year" in criterion_lower and any(str(y) in criterion_lower for y in range(1, 5)):
                actions.append(create_action_item(
                    category="step",
                    description=f"Confirm year eligibility: {criterion}",
                    priority="medium"
                ))

    # Skills to highlight
    if profile.skills and opportunity.eligibility_criteria:
        matching_skills = []
        for skill in profile.skills:
            skill_lower = skill.lower()
            for criterion in opportunity.eligibility_criteria:
                if skill_lower in criterion.lower():
                    matching_skills.append(skill)
                    break

        if matching_skills:
            skills_str = ", ".join(matching_skills[:3])
            actions.append(create_action_item(
                category="step",
                description=f"Highlight relevant skills in application: {skills_str}",
                priority="medium"
            ))

    return actions


def generate_action_checklist(
    opportunity: Opportunity,
    profile: Optional[StudentProfile] = None
) -> List[Dict[str, Any]]:
    """Generate a comprehensive action checklist for an opportunity.

    Combines document requirements, deadline actions, application steps,
    and optionally personalized tips based on student profile.

    Each action item contains:
    - category: "document", "step", "urgency_message", "link"
    - description: Human-readable description
    - completed: False (default)
    - priority: "high", "medium", "low"

    Args:
        opportunity: The opportunity to generate actions for
        profile: Optional student profile for personalized tips

    Returns:
        List of actionable step dictionaries
    """
    all_actions = []

    # Add deadline urgency actions first (highest priority)
    deadline_actions = generate_deadline_actions(opportunity)
    all_actions.extend(deadline_actions)

    # Add document checklist
    document_actions = generate_document_checklist(opportunity)
    all_actions.extend(document_actions)

    # Add application steps
    application_actions = generate_application_steps(opportunity)
    all_actions.extend(application_actions)

    # Add profile-specific tips if profile provided
    if profile:
        profile_actions = generate_profile_specific_tips(opportunity, profile)
        all_actions.extend(profile_actions)

    # Sort by priority (high -> medium -> low)
    priority_order = {"high": 0, "medium": 1, "low": 2}
    all_actions.sort(key=lambda x: priority_order.get(x.get("priority", "medium"), 1))

    return all_actions


def format_opportunity_summary(opportunity: Opportunity) -> str:
    """Returns a formatted summary string for display.

    Creates a readable summary containing key opportunity details
    including title, organization, deadline, and benefits.

    Args:
        opportunity: The opportunity to summarize

    Returns:
        Formatted summary string
    """
    lines = []

    # Title and organization
    title = opportunity.title or "Untitled Opportunity"
    org = opportunity.organization or "Unknown Organization"
    lines.append(f"{title} - {org}")

    # Opportunity type
    if opportunity.opportunity_type:
        lines.append(f"Type: {opportunity.opportunity_type.value}")

    # Deadline information
    if opportunity.deadline_type == DeadlineType.HARD and opportunity.deadline_date:
        days_left = calculate_days_left(opportunity.deadline_date)
        if days_left >= 0:
            lines.append(f"Deadline: {opportunity.deadline_date} ({days_left} days left)")
        else:
            lines.append(f"Deadline: {opportunity.deadline_date} (EXPIRED)")
    elif opportunity.deadline_text:
        lines.append(f"Deadline: {opportunity.deadline_text}")
    else:
        lines.append(f"Deadline: {opportunity.deadline_type.value}")

    # Benefits
    if opportunity.benefits:
        lines.append(f"Benefits: {opportunity.benefits}")

    # Location
    if opportunity.location:
        lines.append(f"Location: {opportunity.location}")

    # Duration
    if opportunity.duration:
        lines.append(f"Duration: {opportunity.duration}")

    return "\n".join(lines)


def generate_evidence_quotes(opportunity: Opportunity) -> List[str]:
    """Returns formatted evidence excerpts with context.

    Processes raw excerpts from the source email to create clean,
    display-ready evidence quotes with context indicators.

    Args:
        opportunity: The opportunity containing raw_excerpts

    Returns:
        List of formatted evidence quote strings
    """
    if not opportunity.raw_excerpts:
        return []

    formatted_quotes = []

    for excerpt in opportunity.raw_excerpts:
        if not excerpt or not excerpt.strip():
            continue

        # Clean up the excerpt
        cleaned = excerpt.strip()

        # Remove excessive whitespace
        cleaned = " ".join(cleaned.split())

        # Truncate if too long (keep first 200 chars)
        if len(cleaned) > 200:
            cleaned = cleaned[:197] + "..."

        # Wrap in quotes for clarity
        formatted_quotes.append(f'"{cleaned}"')

    return formatted_quotes
