# Implementation Plan: Opportunity Inbox Copilot

## Overview

Build an AI-powered email processing system that helps university students identify, prioritize, and act on career/academic opportunities from their inbox. Uses a **hybrid architecture**: LLM (Groq API) for extraction/classification + deterministic Python scoring engine for ranking.

**Key Innovation:** 5-tier `DeadlineType` Enum handles ambiguous deadlines (rolling, early priority, relative) that traditional parsers fail on.

---

## Architecture Decisions

1. **LLM Choice:** Groq API (free tier, fast inference, no credit card needed)
2. **Scoring:** Deterministic rule-based engine (not LLM) for transparency and explainability
3. **Deadline Handling:** Enum-based classification with baseline urgency scores
4. **UI Framework:** Streamlit (rapid prototyping, Python-native, minimal CSS)
5. **Design:** Light mode primary, Indigo brand (#4F46E5), specific urgency colors per design_system.md

---

## Dependency Graph

```
src/models.py (Pydantic schemas)
    │
    ├── src/sample_emails.py (test data)
    │
    ├── src/utils.py (date parsing, helpers)
    │       │
    ├── src/extraction.py (Groq LLM extraction)
    │       │
    ├── src/scoring.py (deterministic scoring)
    │       │
    ├── src/actions.py (checklist generator)
    │       │
    └── src/pipeline.py (orchestrator)
            │
            └── app.py (Streamlit UI)
```

**Implementation Order:** Foundation → Extraction → Scoring → Pipeline → UI → Testing → Bonus

---

## Task List (Vertically Sliced)

### Phase 1: Foundation

**Task 1: Project Structure and Dependencies**
- Create `requirements.txt` with all dependencies
- Create `.env.example` for API key template
- Create `src/__init__.py` and `tests/__init__.py`
- **Scope:** XS (config files)

**Task 2: Pydantic Models with DeadlineType Enum**
- Create `src/models.py` with `StudentProfile`, `Opportunity`, `RankedOpportunity`
- Implement 5-tier `DeadlineType` enum per response.md
- Include validation and field descriptions
- **Scope:** S (1-2 files)

**Task 3: Sample Email Dataset**
- Create `src/sample_emails.py` with 12 high-quality, varied test emails
- Include: scholarships (3), internships (3), fellowships (2), competitions (2), spam (2)
- Each email must test different DeadlineType scenarios
- **Scope:** S (1 file, content creation)

**Task 4: Basic Streamlit Skeleton**
- Create `app.py` with minimal Streamlit structure
- Implement design system color constants
- Create placeholder screens: Input, Processing, Results
- **Scope:** S (1 file)

### Checkpoint 1: Foundation Complete
- [ ] All files created and import without errors
- [ ] `streamlit run app.py` shows skeleton UI
- [ ] Sample emails load correctly
- [ ] Pydantic models validate test data

---

### Phase 2: Extraction Layer

**Task 5: Groq API Client and Prompts**
- Create `src/extraction.py` with Groq client initialization
- Write extraction prompt with DeadlineType detection rules
- Implement retry logic and error handling
- **Scope:** M (3-5 files including prompt engineering)

**Task 6: Date Parsing Utilities**
- Create `src/utils.py` with fuzzy date parsing
- Implement date validation and normalization
- Add helper for relative date detection
- **Scope:** XS (1 file)

**Task 7: Extraction Tests**
- Create `tests/test_extraction.py` with unit tests
- Test all 12 sample emails
- Verify DeadlineType classifications
- **Scope:** S (1-2 files)

### Checkpoint 2: Extraction Working
- [ ] All 12 sample emails extract without errors
- [ ] DeadlineType classifications are correct
- [ ] Evidence excerpts are captured
- [ ] Groq API calls succeed

---

### Phase 3: Deterministic Scoring

**Task 8: Profile Fit Scoring**
- Create `src/scoring.py` with `calculate_profile_fit()`
- Implement degree match, CGPA threshold, skills overlap
- Return score + list of reasons
- **Scope:** S (1 file)

**Task 9: Urgency Scoring with DeadlineType**
- Implement `calculate_urgency_score()` with 5-tier enum support
- Hard deadline: days_left calculation
- Other types: baseline scores per plan
- **Scope:** S (same file)

**Task 10: Completeness and Composite Scoring**
- Implement `calculate_completeness_score()`
- Implement `calculate_composite_score()` with weighted formula
- 45% profile fit, 30% urgency, 25% completeness
- **Scope:** S (same file)

**Task 11: Scoring Tests**
- Create `tests/test_scoring.py` with comprehensive coverage
- Test each DeadlineType path
- Test edge cases (past deadlines, missing data)
- **Scope:** S (1-2 files)

### Checkpoint 3: Scoring Working
- [ ] All scoring functions have unit tests passing
- [ ] Each DeadlineType produces expected urgency score
- [ ] Composite scores calculate correctly with weights
- [ ] Edge cases handled gracefully

---

### Phase 4: Pipeline and Actions

**Task 12: Action Checklist Generator**
- Create `src/actions.py` with `generate_action_checklist()`
- Generate document preparation steps
- Add deadline-aware urgency messages
- Include application link guidance
- **Scope:** S (1 file)

**Task 13: Pipeline Orchestrator**
- Create `src/pipeline.py` with `process_inbox()` async function
- Wire extraction → scoring → action generation
- Filter non-opportunities (confidence < 0.5)
- Sort by composite score descending
- **Scope:** M (3-5 files integration)

**Task 14: Pipeline Integration Tests**
- Create `tests/test_pipeline.py` with end-to-end tests
- Test full flow: email → ranked opportunity
- Verify output structure
- **Scope:** S (1-2 files)

### Checkpoint 4: Pipeline Complete
- [ ] Full pipeline runs end-to-end
- [ ] Rankings are logical and deterministic
- [ ] Action checklists are actionable
- [ ] Integration tests pass

---

### Phase 5: UI with Design System

**Task 15: Profile Input Screen**
- Build form with progress indicator (STEP 1 of 2)
- Fields: degree, year, CGPA, skills (tags), preferred types (checkboxes)
- Financial need + location preference
- Real-time validation
- **Scope:** M (1 file, complex UI)

**Task 16: Email Input Screen**
- Text area with delimiter support ("---")
- File uploader (.txt, .eml)
- Real-time email count
- "Analyze My Opportunities" CTA (indigo, full-width)
- **Scope:** S (1 file)

**Task 17: Processing State Screen**
- Animated progress bar
- Step indicators with checkmarks
- Rotating tips about rolling deadlines
- **Scope:** XS (1 file)

**Task 18: Results Dashboard**
- Summary bar: Critical | Urgent | Moderate | Comfortable counts
- Filter tabs: All | Scholarship | Internship | etc.
- Sort dropdown
- **Scope:** M (1 file)

**Task 19: Opportunity Cards**
- Left accent bar (4px, urgency color per design_system.md)
- Rank number + urgency badge + match score
- Title, type chip, location, award
- "Why this rank?" expandable
- [See Action Checklist] and [Apply Now] buttons
- **Scope:** M (1 file, complex component)

**Task 20: Action Checklist Panel**
- Expanded card view with full checklist
- Document checkboxes, next steps
- Evidence quotes from email
- Deadline countdown
- **Scope:** S (1 file)

### Checkpoint 5: UI Complete
- [ ] All screens render correctly
- [ ] Colors match design_system.md exactly
- [ ] Cards show urgency colors properly
- [ ] Expandable sections work
- [ ] Mobile responsive (test viewport resize)

---

### Phase 6: Testing and Edge Cases

**Task 21: Edge Case Handling**
- Empty email input
- Single spam email
- Past deadlines
- Malformed application links
- API errors (retry logic)
- **Scope:** M (3-5 files, bug fixes)

**Task 22: Final Integration Test**
- Run full demo flow
- Verify end-to-end <30 seconds
- Test all user interactions
- **Scope:** S (manual testing)

### Checkpoint 6: Core Complete
- [ ] All edge cases handled
- [ ] Demo flow works end-to-end
- [ ] Performance <30 seconds

---

### Phase 7: Bonus Features (If Time Permits)

**Task 23: Profile Improvement Suggestions**
- Analyze missed opportunities
- Suggest skills to add
- Show match potential
- **Scope:** M (2-3 files)

**Task 24: Export Functionality**
- Export to PDF
- Export to CSV
- Copy to clipboard
- **Scope:** S (1-2 files)

**Task 25: Opportunity Summary Insights**
- "You have X scholarships matching financial need"
- "Y opportunities expire this week"
- Dashboard widgets
- **Scope:** S (1 file)

---

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Groq API rate limits or downtime | High | Implement 3-retry logic; cache responses |
| LLM extraction hallucinations | Medium | Use temperature=0; Pydantic validation; evidence excerpts |
| Deadline parsing edge cases | Low | DeadlineType enum covers ambiguity; graceful fallbacks |
| UI complexity exceeds time | Medium | Use Streamlit native widgets; minimal custom CSS |
| Time overrun | High | Cut bonus features; ensure core pipeline works first |

---

## Parallelization Opportunities

**Can run in parallel (after Checkpoint 1):**
- Task 5 (Groq client) + Task 6 (utils) + Task 8 (profile scoring)
- Task 9 (urgency scoring) + Task 10 (completeness scoring)
- Task 15 (profile UI) + Task 16 (email input UI)
- Task 17 (processing screen) + Task 18 (results dashboard)

**Must be sequential:**
- Models must exist before extraction
- Extraction must work before pipeline
- Pipeline must work before UI integration

---

## Success Criteria (Final)

- [ ] System correctly classifies real opportunities vs spam (>90% on test set)
- [ ] DeadlineType enum handles all 5 ambiguity cases correctly
- [ ] Deterministic scoring produces transparent, explainable rankings
- [ ] Evidence excerpts from emails displayed for each opportunity
- [ ] Action checklists generated with practical next steps
- [ ] UI matches design_system.md (light mode, indigo #4F46E5, urgency colors)
- [ ] End-to-end demo completes in <30 seconds
- [ ] All tests pass

---

**Estimated Total Time:** 6 hours
- Phase 1: 45 min (Foundation)
- Phase 2: 90 min (Extraction)
- Phase 3: 60 min (Scoring)
- Phase 4: 45 min (Pipeline)
- Phase 5: 90 min (UI)
- Phase 6: 30 min (Testing)
- Phase 7: Remaining time (Bonus)
