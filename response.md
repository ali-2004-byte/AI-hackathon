Based on the excellent framework in `response.md`, here is the final, strategic recommendation for handling deadline ambiguity in your Opportunity Inbox Copilot.

### The Final Suggestion: Treat Ambiguity as a Structured Data Type

Instead of trying to force every deadline into a strict `datetime` object (and failing when encountering words like "rolling"), you should **model deadline ambiguity as a first-class feature using a 5-tier Categorical Enum**.

Your LLM extraction layer must be instructed to output one of these specific tags: `DEADLINE_HARD`, `DEADLINE_ROLLING`, `DEADLINE_SOFT_EARLY`, `DEADLINE_RELATIVE`, or `DEADLINE_UNKNOWN`. Your deterministic scoring engine then applies fixed baseline scores or multipliers based on that tag.

### Justification and Explanation

**1. It accurately reflects real-world urgency (The "Opportunity Cost" factor)**
Treating a "Rolling Basis" deadline as a `None` or `Null` value is a critical failure because it usually results in the system giving it a score of 0. In reality, a rolling deadline is highly urgent because the opportunity could close tomorrow. Assigning it a baseline high score (e.g., 75/100) accurately models the real-world pressure to apply immediately, ensuring these don't get buried at the bottom of the student's list.

**2. It guarantees determinism and system stability**
By forcing the LLM to classify the ambiguity into one of five predefined Enums, you completely eliminate the unpredictability of fuzzy text parsing in your Python backend. Your scoring engine (`calculate_urgency_score`) becomes a simple, fail-proof switch statement or dictionary lookup rather than a complex mess of regex trying to decipher "end of the month."

**3. It elevates the tool from an "Extractor" to a true "Copilot"**
A standard parser just extracts data. A _Copilot_ tells you what to do with it. By detecting states like `DEADLINE_RELATIVE` or `DEADLINE_SOFT_EARLY`, you unlock the ability to inject dynamic advice into the Action Checklist. Prompting the student to _"Verify the actual deadline on the official portal"_ or _"Do not wait for the last date — this rewards early action"_ proves the AI understands context, massively increasing user trust.

**4. It fits perfectly within a 6-Hour Hackathon Scope**
Building a custom date-math engine to resolve relative dates is too time-consuming for an MVP. Offloading the categorization to the LLM (which is already reading the email) via a Pydantic schema is incredibly cheap to implement. One well-crafted prompt handles extraction, classification, and excerpt gathering simultaneously.

---

### Verdict

**VERDICT:** Implement a 5-tier `DeadlineType` Enum in your Pydantic schema to classify ambiguous deadlines, assigning inherently high urgency scores to "Rolling" and "Early Priority" opportunities so they rank appropriately above distant fixed dates.
