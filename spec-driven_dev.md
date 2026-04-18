**Spec-Driven Development (SDD) with coding agents** is a structured methodology that treats a detailed, living specification as the primary artifact and "contract" between you (the human architect/product owner) and AI coding agents (Claude Code, Cursor, Copilot, etc.). You create or co-create a clear Markdown spec _before_ implementation. The agent implements, verifies, and iterates against it. The spec defines outcomes, scope (including explicit boundaries on what _not_ to build), constraints, prior decisions, modular tasks, and verification criteria. It evolves as the source of truth; code is a generated, verifiable output. Maintaining software means evolving the specs.

This is the disciplined alternative to "**vibe coding**" (ad-hoc, conversational prompting that produces fast but often misaligned, inconsistent, or hard-to-maintain code). SDD moves beyond vague prompts by providing explicit context, reducing hallucinations, preserving intent across sessions, minimizing cognitive debt, and keeping you in control through gated verification. It draws from (but adapts) traditional specs, TDD principles, and model-driven ideas for the agentic era. Specs can be task-specific (for features) or anchored as living documents for long-term evolution.

### The Spec: A Contract with Six Essential Elements

A good AI spec is concise, behavior-oriented, and unambiguous—written in natural language but structured like a tight PRD/SRS. Leave any element open and the agent will "fill the gap" in undesirable ways. Use these six elements (adapted from practitioner guides):

1. **Outcomes/Success Criteria**: Specific, verifiable end-states. Not "build auth." Instead: "Users can sign up with email/password, receive a verification email, log in without errors, and have sessions persist across refreshes. Success: no OAuth, works offline-first where possible."
2. **Scope Boundaries (In and Explicitly Out)**: List what's included _and_ excluded. Agents love scope creep. "OAuth, social login, and password reset are out of scope for v1." This is often the highest-leverage section.
3. **Constraints & Assumptions**: Tech stack, performance, policies, non-functional requirements, compliance. Pair with a persistent **AGENTS.md** or **CLAUDE.md** (or equivalent rules file) for project-wide guardrails (e.g., "Always use this ORM; Never commit secrets; Ask before schema changes").
4. **Prior Decisions**: Architecture choices, schemas, libraries already selected. Prevents the agent from reinventing or conflicting.
5. **Task Breakdown**: Decompose into small, independent, reviewable subtasks. Critical—avoids massive undifferentiated code dumps. Enables parallel work or sequential verification.
6. **Verification Criteria**: Acceptance criteria, edge cases, test expectations, manual checks. "Run these tests; verify responsive breakpoints; check against design tokens from Figma MCP." This drives automated or adversarial verification.

**Template skeleton** (in `SPEC.md` or `specs/feature-x/spec.md`):

- Objective/Overview + User Journeys
- The 6 elements above
- References to related docs, architecture, or prior specs

Keep it team-reviewable; avoid bloat from over-frameworks. Version in Git.

### The Repeatable Workflow (Plan-Implement-Verify, Gated)

Use a **four-phase gated process** (don't advance until the current phase is validated by you or a verifier). The spec drives everything; it is living and updated in real time.

- **Specify**: Start high-level ("Build a task tracker with users, persistence, responsive UI. Focus on simple UX and data integrity."). Let the agent draft a detailed spec; you refine critically as the domain expert. Focus on _what_ and _why_ (user outcomes), not _how_.
- **Plan**: Feed technical constraints, stack, architecture, and existing codebase context. Agent produces a technical plan. Update your AGENTS.md/constitution with immutable principles.
- **Tasks**: Agent breaks the spec + plan into small, isolatable tasks with checklists. Review and approve.
- **Implement + Verify**: Agent implements task-by-task (or in parallel for non-overlapping work). You review focused diffs. Use tests, a separate verifier agent (adversarial pattern: implementer optimizes for "done"; verifier hunts for spec violations, drift, or missed edges), or LLM-as-judge. Update the spec with discoveries. Repeat.

**Plan-implement-verify loop** applies to both greenfield and existing codebases (e.g., spec how a new feature integrates without breaking legacy patterns). Automate repeatable parts with custom agent "skills." Use Plan/read-only modes for spec drafting to reduce risk.

For tools like **GitHub Spec Kit**, use CLI setup (`specify init`) and slash commands (`/specify`, `/plan`, `/tasks`) that generate artifacts and enforce the process with your chosen agent (Copilot, Claude, etc.). Other options: Kiro (IDE-native requirements → design → tasks), Cursor with rules files, or frameworks like Tessl for tighter spec-to-code generation.

### Actionable, Immediately Applicable Insights & Best Practices

- **Start today**: For your next non-trivial feature, write (or co-write) a SPEC.md with the six elements instead of prompting directly. Instruct the agent: "Read SPEC.md and AGENTS.md. Implement tasks sequentially. Update spec if gaps found. Verify against criteria before declaring done. Ask clarifying questions only." Review output ruthlessly against the spec.
- **Co-write with AI but own the edit**: High-level brief → AI draft → your critical refinement. Use your expertise for edges, trade-offs, and "NOT" statements. Best model for spec writing (errors propagate downstream).
- **Model tiering & adversarial pattern**: Top-tier (e.g., Claude 4/Opus-class) for specs/planning; solid mid-tier for implementation; fast/cheap for verification. Use coordinator → implementers → separate strict verifier to catch what self-checking misses.
- **Context hygiene**: Feed _relevant_ sections only (avoid full codebase dumps). Use MCP servers for live runtime, Figma integration, or repo-info agents. Persistent files (AGENTS.md) handle project rules so task specs stay focused.
- **Guardrails (Always/Ask/Never)**: In AGENTS.md: "Always run tests and respect existing patterns. Ask before cross-service changes. Never add unrequested features or use deprecated libs."
- **Scale & legacy**: Explicitly spec integrations, non-functional requirements, and brownfield constraints. For maintenance, evolve the spec first, then regenerate plan/tasks.
- **Verification is non-negotiable**: Tie to tests (TDD-like), checklists, edge cases, and manual review. Treat spec as executable—update it when reality diverges.
- **When to skip**: Trivial tasks or pure exploration. Reserve overhead for work where misalignment is expensive.
- **Measure effectiveness**: Reduced fix iterations, higher intent fidelity on first pass, easier onboarding/maintenance, specs that remain useful months later.

**Pitfalls to avoid**:

- Treating it as rigid waterfall (keep it iterative; update specs freely).
- Vague or incomplete specs.
- One massive prompt/task instead of modular breakdown.
- Over-documenting or ignoring human review (verbose specs don't replace code review).
- Assuming agents will perfectly follow without gates or adversarial verification. Tools and definitions are still maturing—experiment in small projects first.

**Resources for immediate depth**: DeepLearning.AI short course (with JetBrains) on the plan-implement-verify workflow; GitHub Spec Kit repo for templates/commands; practitioner posts from Addy Osmani, Augment Code, and related tooling (Kiro, Tessl).

SDD shifts the lingua franca upward: you focus on intent, architecture, and verification while agents handle implementation at scale. Done well, it produces more intentional, maintainable software faster than vibe coding or traditional solo development. The key is rigor in the spec and gates—start small, iterate on your spec-writing skill, and it compounds quickly.
