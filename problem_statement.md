**LLM-Optimized, High-Signal, Readable Version:**

### **AI Hackathon Project: Opportunity Inbox Copilot**

#### **Project Title**

**Opportunity Inbox Copilot: Email Parsing + Personalized Opportunity Ranking**

#### **Problem Statement**

University students receive hundreds of emails about scholarships, internships, competitions, admissions, fellowships, and other career/academic opportunities. Most of these emails are ignored, misread, or lost in spam/promotions.

Students struggle to:

- Identify which emails contain **real, actionable** opportunities
- Extract key details (deadlines, eligibility, requirements)
- Understand which opportunities are **most relevant and urgent** for them personally

**Goal**: Build an AI-powered system that acts as a smart personal copilot — it scans opportunity-related emails, extracts structured information, matches them against the student’s profile, and delivers a clear, **evidence-backed priority ranking** with actionable next steps.

#### **What You Need to Build (Core Requirements)**

Create a working prototype that does the following:

**Input:**

- A batch of 5–15 opportunity-related emails (uploaded or pasted as text)
- Optional: Additional notice/content in plain text
- A **structured student profile** (form-based, not free text)

**Student Profile Fields (Suggested):**

- Degree / Program
- Current Semester / Year
- CGPA
- Skills & Interests
- Preferred opportunity types (scholarship, internship, fellowship, competition, etc.)
- Financial need (Yes/No + level)
- Location preference
- Relevant past experience

**Output:**
For every genuine opportunity, the system must:

1. **Classify** whether the email contains a real opportunity
2. **Extract** structured data:
   - Opportunity type
   - Deadline
   - Eligibility criteria
   - Required documents
   - Application link / contact information
   - Other key details
3. **Score & Rank** opportunities based on:
   - Relevance to student profile
   - Urgency (deadline proximity)
   - Completeness of match
4. Generate a **personalized priority list** (highest to lowest) with:
   - Clear explanation of why each opportunity is ranked where it is
   - Highlighted urgency
   - Evidence-backed reasoning (quotes/references from email + profile match)
   - Practical **action checklist** (what to do next, documents needed, etc.)

#### **Core AI Challenges (Beyond Simple Summarization)**

The AI must perform advanced tasks:

- **Opportunity Detection**: Distinguish real opportunities from spam, newsletters, or irrelevant announcements
- **Structured Extraction**: Pull clean fields from messy, natural-language emails (deadlines, clauses, requirements)
- **Reasoning & Scoring**: Build a deterministic or hybrid scoring engine that evaluates profile fit, urgency, and feasibility
- **Explainability**: Provide transparent, evidence-based reasons for every ranking decision

#### **Realistic MVP Scope (Buildable in ~6 Hours)**

- Support 5–15 English emails as input
- Reliable opportunity classification
- Structured information extraction (type, deadline, eligibility, documents, links)
- Structured student profile input (form fields)
- Personalized ranking with explanations
- Clean, student-friendly output (priority list + action checklist)

#### **Suggested Demo Flow**

1. Show a cluttered student inbox with many ignored opportunity emails
2. User uploads/pastes the emails + fills their profile
3. System processes everything
4. Display clean, ranked list of real opportunities
5. For each opportunity: show extracted details, ranking justification, urgency flag, and exact next steps

---

**Tagline Idea**:  
_“Turn email chaos into your personal opportunity advantage.”_

This version is optimized for LLMs (clear sections, explicit requirements, no fluff, high readability, strong signal-to-noise ratio) while remaining very easy for humans to understand and work with.
