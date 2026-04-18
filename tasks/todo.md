# Task List: Opportunity Inbox Copilot

## Phase 1: Foundation

- [ ] **Task 1:** Project Structure and Dependencies
  - [ ] Create `requirements.txt`
  - [ ] Create `.env.example`
  - [ ] Create package inits
  - **Files:** requirements.txt, .env.example, src/__init__.py, tests/__init__.py
  - **Scope:** XS

- [ ] **Task 2:** Pydantic Models with DeadlineType Enum
  - [ ] Create `src/models.py`
  - [ ] Implement `DeadlineType` enum (hard, rolling, soft_early, relative, unknown)
  - [ ] Define `StudentProfile`, `Opportunity`, `RankedOpportunity`
  - **Files:** src/models.py
  - **Scope:** S

- [ ] **Task 3:** Sample Email Dataset
  - [ ] Create `src/sample_emails.py`
  - [ ] 12 varied emails covering all deadline types
  - [ ] Include spam examples for classification testing
  - **Files:** src/sample_emails.py
  - **Scope:** S

- [ ] **Task 4:** Basic Streamlit Skeleton
  - [ ] Create `app.py` with 3 screens
  - [ ] Add design system color constants
  - [ ] Test `streamlit run app.py`
  - **Files:** app.py
  - **Scope:** S

### Checkpoint 1: Foundation Complete
- [ ] All files import without errors
- [ ] Streamlit skeleton loads
- [ ] Sample emails accessible
- [ ] Pydantic models validate

---

## Phase 2: Extraction Layer

- [ ] **Task 5:** Groq API Client and Prompts
  - [ ] Create `src/extraction.py`
  - [ ] Write extraction prompt with DeadlineType detection
  - [ ] Implement retry logic (3 retries)
  - [ ] Test with Groq API
  - **Files:** src/extraction.py
  - **Scope:** M

- [ ] **Task 6:** Date Parsing Utilities
  - [ ] Create `src/utils.py`
  - [ ] Fuzzy date parsing with dateparser
  - [ ] Relative date helpers
  - **Files:** src/utils.py
  - **Scope:** XS

- [ ] **Task 7:** Extraction Tests
  - [ ] Create `tests/test_extraction.py`
  - [ ] Test all 12 sample emails
  - [ ] Verify DeadlineType classifications
  - **Files:** tests/test_extraction.py
  - **Scope:** S

### Checkpoint 2: Extraction Working
- [ ] All 12 emails extract successfully
- [ ] DeadlineType correct
- [ ] Evidence excerpts captured
- [ ] API calls succeed

---

## Phase 3: Deterministic Scoring

- [ ] **Task 8:** Profile Fit Scoring
  - [ ] Create `src/scoring.py`
  - [ ] Implement `calculate_profile_fit()`
  - [ ] Degree match, CGPA, skills overlap
  - **Files:** src/scoring.py
  - **Scope:** S

- [ ] **Task 9:** Urgency Scoring with DeadlineType
  - [ ] Implement `calculate_urgency_score()`
  - [ ] Hard deadline: days_left calculation
  - [ ] Other types: baseline scores
  - **Files:** src/scoring.py
  - **Scope:** S

- [ ] **Task 10:** Completeness and Composite Scoring
  - [ ] Implement `calculate_completeness_score()`
  - [ ] Implement `calculate_composite_score()`
  - [ ] Weights: 45%/30%/25%
  - **Files:** src/scoring.py
  - **Scope:** S

- [ ] **Task 11:** Scoring Tests
  - [ ] Create `tests/test_scoring.py`
  - [ ] Test each DeadlineType path
  - [ ] Test edge cases
  - **Files:** tests/test_scoring.py
  - **Scope:** S

### Checkpoint 3: Scoring Working
- [ ] All tests pass
- [ ] Each DeadlineType produces correct score
- [ ] Composite scores correct
- [ ] Edge cases handled

---

## Phase 4: Pipeline and Actions

- [ ] **Task 12:** Action Checklist Generator
  - [ ] Create `src/actions.py`
  - [ ] `generate_action_checklist()` function
  - [ ] Document steps, links, urgency messages
  - **Files:** src/actions.py
  - **Scope:** S

- [ ] **Task 13:** Pipeline Orchestrator
  - [ ] Create `src/pipeline.py`
  - [ ] `process_inbox()` async function
  - [ ] Wire: extract → score → actions
  - [ ] Filter by confidence > 0.5
  - [ ] Sort by composite score
  - **Files:** src/pipeline.py
  - **Scope:** M

- [ ] **Task 14:** Pipeline Integration Tests
  - [ ] Create `tests/test_pipeline.py`
  - [ ] End-to-end flow tests
  - [ ] Verify output structure
  - **Files:** tests/test_pipeline.py
  - **Scope:** S

### Checkpoint 4: Pipeline Complete
- [ ] Full pipeline runs end-to-end
- [ ] Rankings are logical
- [ ] Action checklists actionable
- [ ] Integration tests pass

---

## Phase 5: UI with Design System

- [ ] **Task 15:** Profile Input Screen
  - [ ] Progress indicator (STEP 1 of 2)
  - [ ] Form fields: degree, year, CGPA, skills, types
  - [ ] Financial need, location
  - [ ] Real-time validation
  - **Files:** app.py (update)
  - **Scope:** M

- [ ] **Task 16:** Email Input Screen
  - [ ] Text area with "---" delimiter
  - [ ] File uploader (.txt, .eml)
  - [ ] Real-time email count
  - [ ] "Analyze" CTA button (indigo)
  - **Files:** app.py (update)
  - **Scope:** S

- [ ] **Task 17:** Processing State Screen
  - [ ] Animated progress bar
  - [ ] Step indicators with checkmarks
  - [ ] Rotating tips
  - **Files:** app.py (update)
  - **Scope:** XS

- [ ] **Task 18:** Results Dashboard
  - [ ] Summary bar: Critical | Urgent | Moderate | Comfortable
  - [ ] Filter tabs: All | Scholarship | Internship | etc.
  - [ ] Sort dropdown
  - **Files:** app.py (update)
  - **Scope:** M

- [ ] **Task 19:** Opportunity Cards
  - [ ] Left accent bar (4px, urgency color)
  - [ ] Rank number + urgency badge + match score
  - [ ] Title, type, location, award
  - [ ] "Why this rank?" expandable
  - [ ] Action buttons
  - **Files:** app.py (update)
  - **Scope:** M

- [ ] **Task 20:** Action Checklist Panel
  - [ ] Expanded card with full checklist
  - [ ] Document checkboxes
  - [ ] Evidence quotes
  - [ ] Deadline countdown
  - **Files:** app.py (update)
  - **Scope:** S

### Checkpoint 5: UI Complete
- [ ] All screens render
- [ ] Colors match design_system.md
- [ ] Urgency colors correct
- [ ] Expandables work
- [ ] Mobile responsive

---

## Phase 6: Testing and Edge Cases

- [ ] **Task 21:** Edge Case Handling
  - [ ] Empty email input
  - [ ] Single spam email
  - [ ] Past deadlines
  - [ ] Malformed links
  - [ ] API error retry
  - **Files:** Various
  - **Scope:** M

- [ ] **Task 22:** Final Integration Test
  - [ ] Run full demo flow
  - [ ] Verify <30 seconds
  - [ ] Test all interactions
  - **Scope:** Manual

### Checkpoint 6: Core Complete
- [ ] Edge cases handled
- [ ] Demo flow works
- [ ] Performance OK

---

## Phase 7: Bonus Features (If Time)

- [ ] **Task 23:** Profile Improvement Suggestions
  - [ ] Analyze missed opportunities
  - [ ] Suggest skills to add
  - [ ] Show match potential
  - **Files:** src/suggestions.py (new)
  - **Scope:** M

- [ ] **Task 24:** Export Functionality
  - [ ] Export to PDF
  - [ ] Export to CSV
  - [ ] Copy to clipboard
  - **Files:** src/export.py (new)
  - **Scope:** S

- [ ] **Task 25:** Opportunity Summary Insights
  - [ ] Dashboard widgets
  - [ ] Summary statistics
  - **Files:** app.py (update)
  - **Scope:** S

---

## Progress Tracking

**Current Phase:** _Not started_
**Tasks Completed:** 0/25
**Checkpoints Cleared:** 0/6

**Time Budget:** 6 hours
- [ ] Phase 1: 45 min
- [ ] Phase 2: 90 min
- [ ] Phase 3: 60 min
- [ ] Phase 4: 45 min
- [ ] Phase 5: 90 min
- [ ] Phase 6: 30 min
- [ ] Phase 7: Remaining time
