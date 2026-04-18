# Spec: Opportunity Inbox Copilot

## Objective

Build an AI-powered email processing system that helps university students identify, prioritize, and act on career/academic opportunities from their inbox.

**Target Users:** University students overwhelmed by opportunity emails (scholarships, internships, competitions, fellowships)

**Core Value Proposition:** Transform email chaos into a personalized, ranked action list with clear next steps and evidence-backed reasoning.

### User Stories

1. As a student, I can upload/paste multiple emails and my profile to get a ranked list of genuine opportunities
2. As a student, I can see why each opportunity is ranked where it is with evidence from the email
3. As a student, I receive a clear action checklist for each opportunity (documents needed, deadlines, links)

### Success Criteria

- [ ] System correctly classifies real opportunities vs spam/newsletters (>90% accuracy on test set)
- [ ] System extracts structured data: deadline, eligibility, required docs, application link, opportunity type
- [ ] Ranking reflects student profile match, urgency, and completeness
- [ ] Each ranking includes evidence-backed reasoning (quotes from email)
- [ ] Action checklist generated for each opportunity
- [ ] Clean, student-friendly web interface
- [ ] End-to-end demo completes in <30 seconds for 5-15 emails

---

## Tech Stack

| Component       | Choice                              | Reason                                             |
| --------------- | ----------------------------------- | -------------------------------------------------- |
| Frontend        | Streamlit                           | Rapid prototyping, Python-native, built-in widgets |
| Backend         | Python 3.11+                        | Fast development, rich ecosystem                   |
| LLM             | use Groq/cerebrum APIs              | Strong structured output, reasoning capabilities   |
| Data Validation | Pydantic                            | Type-safe, JSON schema enforcement                 |
| Date Parsing    | dateparser                          | Handles fuzzy deadline extraction                  |
| Key Libraries   | pydantic, dateparser, python-dotenv |

---

## Commands

```bash
# Setup
pip install -r requirements.txt
cp .env.example .env  # Add your Groq/cerebrum

# Development
streamlit run app.py

# Testing
python -m pytest tests/

# Type Checking
mypy src/
```

---

## Project Structure

```
C:/Users/mypc/Downloads/AI-hackathon/
├── SPEC.md                    # This document
├── app.py                     # Streamlit entry point
├── requirements.txt           # Dependencies
├── .env                       # API keys (gitignored)
├── .env.example               # Template for env vars
├── src/
│   ├── __init__.py
│   ├── models.py              # Pydantic models (Profile, Opportunity)
│   ├── pipeline.py            # Main processing pipeline
│   ├── extraction.py          # LLM extraction layer
│   ├── scoring.py             # Deterministic scoring engine
│   ├── utils.py               # Date parsing, text cleaning
│   └── sample_emails.py       # Test data
├── tests/
│   ├── __init__.py
│   ├── test_extraction.py
│   ├── test_scoring.py
│   └── test_pipeline.py
└── README.md                  # Setup and usage
```

---

## Code Style

### Naming Conventions

- `snake_case` for functions, variables, filenames
- `PascalCase` for classes (Pydantic models)
- `SCREAMING_SNAKE_CASE` for constants

### Pydantic Model Example

```python
from pydantic import BaseModel, Field
from datetime import date
from typing import List, Optional

class StudentProfile(BaseModel):
    degree: str = Field(..., description="e.g., Computer Science")
    year: int = Field(..., ge=1, le=6, description="Current year of study")
    cgpa: float = Field(..., ge=0, le=4.0)
    skills: List[str] = Field(default_factory=list)
    interests: List[str] = Field(default_factory=list)
    preferred_types: List[str] = Field(..., description="scholarship, internship, etc.")
    financial_need: bool = False
    location_pref: Optional[str] = None
    experience: List[str] = Field(default_factory=list)

class Opportunity(BaseModel):
    is_opportunity: bool
    confidence: float = Field(..., ge=0, le=1)
    title: Optional[str] = None
    organization: Optional[str] = None
    opportunity_type: Optional[str] = None
    deadline: Optional[date] = None
    eligibility_criteria: List[str] = Field(default_factory=list)
    required_documents: List[str] = Field(default_factory=list)
    application_link: Optional[str] = None
    contact_email: Optional[str] = None
    raw_excerpts: List[str] = Field(default_factory=list, description="Evidence quotes")
```

### Scoring Engine Pattern

```python
def calculate_urgency_score(deadline: date) -> tuple[float, str]:
    """Returns (score, explanation)."""
    days_left = (deadline - date.today()).days
    if days_left < 7:
        return (100, f"Deadline in {days_left} days - urgent")
    elif days_left < 30:
        return (70, f"Deadline in {days_left} days - approaching")
    elif days_left < 90:
        return (40, f"Deadline in {days_left} days - moderate time")
    else:
        return (20, f"Deadline in {days_left} days - plenty of time")
```

---

## Testing Strategy

| Test Type   | Framework    | Location                 | Coverage Target              |
| ----------- | ------------ | ------------------------ | ---------------------------- |
| Unit Tests  | pytest       | `tests/`                 | >80% for scoring, extraction |
| Integration | pytest       | `tests/test_pipeline.py` | Core pipeline                |
| Manual      | Streamlit UI | Browser                  | Full user flow               |

### Test Categories

1. **Extraction Tests:** Verify LLM extracts correct fields from sample emails
2. **Scoring Tests:** Verify deterministic scoring produces expected rankings
3. **Edge Cases:** Malformed dates, missing fields, spam classification

### Sample Test

```python
def test_urgency_score_near_deadline():
    from datetime import date, timedelta
    from src.scoring import calculate_urgency_score

    deadline = date.today() + timedelta(days=5)
    score, explanation = calculate_urgency_score(deadline)

    assert score == 100
    assert "5 days" in explanation
    assert "urgent" in explanation
```

---

## Boundaries

### Always Do

- Run the full pipeline on test emails before declaring done
- Include evidence excerpts from source emails in outputs
- Validate LLM outputs against Pydantic schemas
- Show score breakdown (weighted components) in UI
- Handle missing/invalid dates gracefully
- Use temperature=0 for LLM extraction calls

### Ask First

- Add new dependencies to requirements.txt
- Change scoring weights/formulas
- Modify Pydantic models (breaking changes)
- Add new opportunity types beyond: scholarship, internship, fellowship, competition, research, job, other
- Commit API keys or .env files

### Never Do

- Commit secrets or API keys
- Use LLM for scoring (must be deterministic)
- Skip validation on LLM outputs
- Remove test files without approval
- Add "vibe coding" features outside spec scope
- Build email fetching/OAuth (out of MVP scope)

---

## Architecture Overview

### Hybrid Pipeline

```
Input: Raw Emails + Student Profile
    │
    ▼
┌─────────────────────────────────────┐
│  LLM Layer (Extraction)             │
│  - Classify: opportunity?           │
│  - Extract: structured fields       │
│  - Gather: evidence excerpts        │
└─────────────────────────────────────┘
    │
    ▼ Structured Opportunity objects
┌─────────────────────────────────────┐
│  Deterministic Scoring Engine       │
│  - Profile Fit (40-50%)             │
│  - Urgency (25-30%)                 │
│  - Completeness (20-30%)            │
└─────────────────────────────────────┘
    │
    ▼ Ranked opportunities
┌─────────────────────────────────────┐
│  Action Generator                  │
│  - Checklist per opportunity        │
│  - Evidence-backed reasoning        │
└─────────────────────────────────────┘
    │
    ▼ Output: Ranked list with actions
```

### Scoring Weights (Configurable)

| Component    | Weight | Factors                                                                                      |
| ------------ | ------ | -------------------------------------------------------------------------------------------- |
| Profile Fit  | 45%    | Degree match, skills overlap, CGPA threshold, location, financial need, experience alignment |
| Urgency      | 30%    | Days until deadline, limited spots language                                                  |
| Completeness | 25%    | Info completeness, required docs match student assets, perceived value                       |

---

## Open Questions

1. **Sample Data:** Do you have 5-15 real opportunity emails for testing, or should I create realistic synthetic examples?
2. **API Key:** Do you have an Anthropic API key, or should the spec include setup instructions for obtaining one?
3. **Deadline Ambiguity:** How should we handle emails with vague deadlines (e.g., "rolling basis", "early applications encouraged")?
4. **Scope:** Should I include a simple "profile improvement suggestions" feature (e.g., "Add Python skills to match more AI internships")?
5. **UI Polish:** Any specific visual preferences (dark/light theme, specific color for urgency indicators)?

---

## Implementation Phases

### Phase 1: Foundation (30 min)

- Set up project structure
- Define Pydantic models
- Create sample email data
- Build Streamlit skeleton

### Phase 2: Extraction Layer (60 min)

- LLM classification prompt
- Structured extraction with Pydantic
- Evidence gathering
- Error handling and retries

### Phase 3: Scoring Engine (45 min)

- Profile fit calculator
- Urgency calculator
- Completeness checker
- Composite scoring

### Phase 4: UI & Integration (45 min)

- Profile form
- Email input (paste/upload)
- Results display (ranked cards)
- Score explanation expander

### Phase 5: Polish & Demo (60 min)

- Test on sample emails
- Edge case handling
- Visual polish
- Prepare demo flow

---

_Spec Version: 1.0_
_Last Updated: 2026-04-18_
_Status: Draft - awaiting review_
