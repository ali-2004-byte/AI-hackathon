**Hybrid LLM for extraction/classification + deterministic rule-based/weighted scoring engine is the optimal path.** This directly addresses the critical differentiator ("deterministic engine, not just AI summaries"), is highly feasible in 6 hours, wins on judging criteria (accuracy, explainability, innovation, UX, feasibility), and scales into a real SaaS product.

### Why This Approach Over Alternatives?

- **Pure rule-based/regex**: Too brittle. Opportunity emails vary wildly in format, sender styles, and language (especially across universities, countries, and opportunity types). You'll spend all your time on edge cases and miss nuanced eligibility or implicit deadlines.
- **Pure Trad ML**: Requires labeled data you don't have in 6 hours; overkill and less flexible for extraction.
- **Pure GenAI/LLM summarization**: Fails the judging bar. LLMs hallucinate fields, outputs aren't reproducible, and "it summarized well" won't impress. Scoring must be traceable and deterministic.
- **Full multi-agent/agentic (e.g., LangGraph with extractor, critic, ranker, researcher agents)**: Promising for v2 (e.g., a verifier agent that cross-checks extraction confidence and triggers human-in-loop or web lookup), but introduces latency, complexity, and prompt management risk in 6 hours. Keep it **sequential pipeline** for MVP. You can _talk about_ agentic extensions in your demo/presentation for extra innovation points.
- **Hybrid (recommended)**: LLM (strong structured output) handles the "messy perception" layer — classifying real opportunity vs. noise and extracting structured fields reliably. Then a pure Python deterministic engine does scoring/ranking with weighted rules, keyword/semantic matching, date calculations, and thresholds. This is auditable ("Score breakdown: Profile Fit 42/50 because skills overlap on Python & ML..."), transparent, and exactly what judges want.

**LLM choice for hackathon**: Prioritize models strong at structured JSON output and following schemas (Claude 3.5/Opus or Sonnet, GPT-4o, or fast/cheap Groq Llama 3.1 70B). Use Pydantic models + JSON mode / Outlines / LangChain PydanticOutputParser + validation retries for near-zero hallucinations on schema.

**Scoring engine design (core differentiator)**: Weighted composite score (configurable weights, show them):

- **Profile Fit (40-50%)**: Exact matches (degree/program, semester, CGPA threshold, location, financial need, preferred types). Semantic/keyword overlap or Jaccard on skills/interests/experience vs. eligibility_criteria (use sentence-transformers for embeddings if time; else simple keyword lists). Bonus for strong past experience alignment.
- **Urgency (25-30%)**: Parse deadline → days until (use `dateparser` + LLM-extracted date string). Formula: e.g., <7 days = 100, <30=70, <90=40, etc. Bonus for "limited spots" or "early deadline" language.
- **Completeness/Value (20-30%)**: % of required_docs that student likely has (or inverse effort), how complete the extracted info is, perceived value (stipend amount, prestige keywords).
- **Overall**: Normalized weighted sum (0-100). Rank descending. Generate reasons via templated text from which rules fired (e.g., "High fit: matches your CS degree, 3.8 CGPA > 3.5 min, Python skill listed"). Add action checklist: "Gather transcript by X", "Draft SOP mentioning Y", "Apply via link before Z", "Prepare recommendation from professor".

This is fully deterministic, traceable, and explainable. You can log every rule contribution.

### Path to a Marketable, Money-Making Product

Market gap exists: Many AI scholarship/internship _search_ tools (profile → recommendations), but few triage _actual university/career center inbox emails_ that students drown in. Your "Opportunity Inbox Copilot" solves real pain (inbox overload, missed deadlines, poor prioritization).

**Product Vision (post-hack)**:

- Web app or Gmail/Outlook add-on: OAuth connect inbox (filter by sender lists or label "opportunities"), profile setup (form + iterative feedback), daily/weekly ranked digest + alerts for high-urgency items.
- Core loop: Ingest → Classify/Filter → Extract → Deterministic Score/Rank → Personalized reasons + actionable checklist + one-click "save to Notion/Airtable" or "draft application email".
- Evolution: User feedback loop (thumbs up/down on rankings) to adjust weights or fine-tune a small extraction model (GLiNER or domain-specific SLM for cost/determinism). Add RAG over past opportunities, AI resume/cover letter drafter tailored to extracted eligibility, auto-apply for simple forms, or web-scraping supplement for more opps.
- **Monetization (practical path to revenue)**:
  - Freemium: Free tier (limited emails/day, basic ranking). Premium ($9-19/mo or $49/year): unlimited, priority alerts, application tracker, essay helper, export to calendar.
  - B2B: University/career center licenses (white-label dashboard for advisors, aggregate insights on popular opps), corporate sponsorships (companies pay to feature internships).
  - Upsells: Premium templates, 1:1 coaching integration.
- **GTM**: Start with Pakistani universities (leverage SOFTEC win, FAST NUCES network). Expand via student ambassadors, LinkedIn/Reddit career groups, partnerships with career services. Hackathon prize + demo video = strong PR. Target students with money (or parents/unis paying). Micro-SaaS principles: solve repetitive pain, charge for time saved.
- **Tech Scaling**: FastAPI backend, Postgres (profiles, history), Celery/ background jobs for email processing, vector DB (Pinecone/Chroma) for better matching, cheaper fine-tuned extractor. Add multi-agent later for complex cases (e.g., research missing eligibility details online).

This can realistically become a sustainable business — students get overwhelmed by emails; unis want better engagement; deterministic transparency builds trust over pure black-box AI.

### High-Level, Step-by-Step Implementation Plan (6-Hour MVP)

**Goal**: Functional end-to-end on 5–15 sample emails, polished UI, clear demo of deterministic scoring + explanations. Prioritize core pipeline over perfection.

1. **Setup & Data Models (30-45 min)**: Streamlit app skeleton. Define Pydantic models for `StudentProfile` (degree, cgpa, skills:list, interests, preferred_types:list, financial_need, location_prefs, experience) and `Opportunity` (title, org, deadline, eligibility_text, required_docs:list, link, contact, opp_type, benefits, raw_excerpts for evidence). Prepare 8-12 diverse sample emails (hardcode or upload).

2. **UI/Inputs (45-60 min)**: Profile form (st.form with selects, multiselect, number inputs). Email input (text areas, file uploader for .eml/.txt, or multiple pastes). "Process Inbox" button. Tabs: Profile, Raw Inbox, Ranked Opportunities, Scoring Engine Explanation.

3. **Classification & Extraction Pipeline (1.5-2 hours)**:
   - Prompt engineering: Few-shot examples (2-3 good/bad emails per class). First LLM call: Classify + confidence + reason. Filter to real opportunities.
   - Second call (or combined with schema): Extract to JSON matching Pydantic. Instruct to quote evidence from email. Post-process (date parsing, normalization). Add retry logic on validation failure. Use temperature 0 for consistency.

4. **Deterministic Scoring & Ranking Engine (45-75 min)**: Pure functions. Implement matchers (skills overlap, CGPA check, eligibility keyword scan). Urgency calculator (days_left). Completeness heuristic. Composite score + per-component breakdown. Templated or light LLM explanation generator that references specific rules and email quotes. Sort and attach action checklists (rule-based templates, e.g., if docs missing → "Prepare these documents").

5. **Output & Explanations (45-60 min)**: Ranked cards or table (score badge, title, key reasons bullet list with evidence, extracted fields, action checklist, "Why this rank?" expander showing formula breakdown). Overall inbox summary ("X opportunities found, Y high priority").

6. **Polish, Testing, Presentation (remaining time ~1-1.5 hours)**: Test on your samples (show accuracy, edge cases like vague deadlines or spam that looks real). Add visuals (progress bars for scores, color-coding urgency). Write a one-page "How it works" (highlight hybrid + deterministic). Prepare 3-5 min demo: problem → profile setup → process emails → ranked actionable output → scoring transparency → product vision (Gmail integration, scaling). Emphasize UX, reliability, and real-world feasibility.

**Tips to Win**:

- Judge on functionality, innovation (deterministic + actionable beyond summary), UX (clean, student-friendly), explainability, and startup potential.
- Show before/after (raw inbox chaos → prioritized action list).
- Mention product roadmap and market fit in presentation.
- Edge: Add simple semantic matching or a "profile improvement suggestions" feature (e.g., "Add ML skills to match more AI internships").

**Post-Hack Next Steps**: Deploy to Streamlit Community Cloud or Vercel. Add real Gmail API (simple OAuth). Collect feedback. Iterate scoring with real users. Build landing page highlighting the hackathon win.

This plan is executable in 6 hours by a small team (one on prompts/UI, one on scoring logic, one on integration/testing). It positions you to win _and_ have a defensible, useful product foundation with clear revenue path. Focus on reliability and transparency — that's your moat. Good luck; this has strong winner potential. If building, start with schemas and prompts first.
