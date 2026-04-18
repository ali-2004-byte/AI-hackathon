# UI/UX Design Specification: Opportunity Inbox Copilot

## Design Philosophy First

Before colors and components, anchor everything to **three HCI principles** that should drive every decision:

```
1. RECOGNITION OVER RECALL    → Students should see what matters, not hunt for it
2. PROGRESSIVE DISCLOSURE     → Show summary first, details on demand
3. ANXIETY REDUCTION          → Deadlines are stressful — design must calm, not alarm
```

> **Core emotional goal**: Transform the feeling of _"I'm overwhelmed"_ into _"I'm in control"_

---

## Theme Recommendation: Light Mode Primary

### Why Not Dark Mode?

```
❌ Dark mode = productivity/developer context
✅ Light mode = academic/document context (matches email, portals, university sites)

Students will use this:
- During daytime study sessions
- Alongside browser tabs, email clients (which are light)
- On phone screens in bright environments

Recommendation: Light mode default + dark mode toggle (don't force either)
```

---

## Color System

### Primary Palette

```
Background:     #F8F9FB   (Soft off-white — easier on eyes than pure white)
Surface/Cards:  #FFFFFF   (Pure white cards on soft background = clear depth)
Primary Brand:  #4F46E5   (Indigo — trustworthy, academic, not corporate-blue)
Text Primary:   #1A1D23   (Near-black — high contrast, not harsh)
Text Secondary: #6B7280   (Gray — metadata, labels)
Border/Divider: #E5E7EB   (Subtle — structure without visual noise)
```

### Urgency Color System (The Most Critical Design Decision)

**HCI Rationale**: Use a traffic-light system but **desaturate red** — full red triggers panic, which reduces rational decision-making.

```
┌─────────────────────────────────────────────────────────────────┐
│  URGENCY TIER    │  COLOR        │  HEX       │  PSYCHOLOGY     │
├─────────────────────────────────────────────────────────────────┤
│  🔴 CRITICAL     │  Warm Red     │  #EF4444   │  Act NOW        │
│  (≤ 3 days)      │  bg: #FEF2F2  │            │  Can't miss it  │
├─────────────────────────────────────────────────────────────────┤
│  🟠 URGENT       │  Amber        │  #F59E0B   │  This week      │
│  (4–7 days)      │  bg: #FFFBEB  │            │  Start soon     │
├─────────────────────────────────────────────────────────────────┤
│  🟡 MODERATE     │  Yellow-Green │  #84CC16   │  This month     │
│  (8–30 days)     │  bg: #F7FEE7  │            │  Plan for it    │
├─────────────────────────────────────────────────────────────────┤
│  🟢 COMFORTABLE  │  Teal Green   │  #10B981   │  Plenty of time │
│  (31–60 days)    │  bg: #ECFDF5  │            │  Bookmark it    │
├─────────────────────────────────────────────────────────────────┤
│  ⚪ UNKNOWN      │  Slate Gray   │  #94A3B8   │  Verify date    │
│  (No deadline)   │  bg: #F8FAFC  │            │  Don't ignore   │
├─────────────────────────────────────────────────────────────────┤
│  🔵 ROLLING      │  Indigo       │  #6366F1   │  Apply ASAP     │
│  (Rolling basis) │  bg: #EEF2FF  │            │  Special rule   │
└─────────────────────────────────────────────────────────────────┘

KEY RULE: Never use color alone — always pair with icon + text label
          (Accessibility: colorblind users must understand urgency too)
```

---

## Typography

```
Font Stack:
  Headings:   Inter (or system-ui) — clean, modern, readable
  Body:       Inter Regular 16px — never go below 14px for key info
  Monospace:  JetBrains Mono — for deadlines, links (draws the eye)

Hierarchy:
  Page Title:       28px / Bold    / #1A1D23
  Card Title:       18px / SemiBold/ #1A1D23
  Metadata Label:   12px / Medium  / #6B7280  UPPERCASE + tracked
  Body Text:        15px / Regular / #374151
  Deadline Text:    14px / Bold    / [urgency color] — always prominent
```

---

## Application Layout & Screen Flow

### Screen 1: Onboarding / Input (The "Setup" Screen)

```
┌─────────────────────────────────────────────────────────┐
│  🎯 Opportunity Inbox Copilot          [Dark Mode Toggle]│
│  "Turn email chaos into your personal opportunity edge" │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  STEP 1 OF 2 ●●○                                       │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │  📋 Your Profile                                 │   │
│  │                                                 │   │
│  │  Degree/Program      [Computer Science      ▼]  │   │
│  │  Year/Semester       [3rd Year              ▼]  │   │
│  │  CGPA                [___.__]                   │   │
│  │  Skills & Interests  [Python, ML, Design...  ]  │   │
│  │                      [+ Add more tags        ]  │   │
│  │                                                 │   │
│  │  I'm looking for:                               │   │
│  │  [✓ Scholarship] [✓ Internship] [ Fellowship]  │   │
│  │  [ Competition ] [ Research   ] [ Exchange  ]  │   │
│  │                                                 │   │
│  │  Financial Need      ○ No  ● Yes → [Medium  ▼] │   │
│  │  Location Preference [Open to Remote + Onsite▼] │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  STEP 2 OF 2 ●●●                                       │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │  📧 Paste Your Emails                           │   │
│  │  ┌───────────────────────────────────────────┐  │   │
│  │  │  Paste 5–15 emails here, separated by    │  │   │
│  │  │  "---" or upload .txt / .eml files       │  │   │
│  │  │                                           │  │   │
│  │  │  [                                      ] │  │   │
│  │  └───────────────────────────────────────────┘  │   │
│  │                                                 │   │
│  │  [📁 Upload Files]  or  [📋 Paste Text]        │   │
│  │                                                 │   │
│  │  Emails detected: 0        ✅ Min 5 required    │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│         [    🚀 Analyze My Opportunities    ]           │
│              Large, Indigo, Full-width CTA              │
└─────────────────────────────────────────────────────────┘
```

**HCI Notes for Input Screen:**

```
✅ Progress indicator (STEP 1 of 2) — reduces uncertainty
✅ Tag-based multi-select for opportunity types — recognition not recall
✅ Real-time email count — immediate feedback
✅ Single primary CTA — no decision paralysis
✅ Inline validation — errors caught before submission
```

---

### Screen 2: Processing State (The "Loading" Screen)

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│              🤖  Analyzing your inbox...                │
│                                                         │
│         ████████████████████░░░░░░░  68%               │
│                                                         │
│    ✅  Detected 11 emails                               │
│    ✅  Classified 8 real opportunities                  │
│    ⏳  Extracting deadlines and requirements...         │
│    ○   Scoring against your profile                    │
│    ○   Building your priority list                     │
│                                                         │
│    💡 Did you know? Rolling deadlines often mean        │
│       earlier = better chance of selection.            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**HCI Notes:**

```
✅ Real-time step progress — reduces abandonment during wait
✅ Show intermediate results (8 real opportunities found) — builds trust
✅ Tip card — makes wait feel productive
✅ Never show raw "Loading..." spinner alone — it creates anxiety
```

---

### Screen 3: Results Dashboard (The Core Screen)

#### Layout Architecture

```
┌──────────────────────────────────────────────────────────────┐
│  ← Back   🎯 Your Opportunity Dashboard      [Export PDF]    │
│           8 opportunities found · Ranked for you            │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  SUMMARY BAR                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ 🔴  2   │  │ 🟠  1   │  │ 🟡  3   │  │ 🟢  2   │   │
│  │ Critical │  │ Urgent   │  │ Moderate │  │ Comfort  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│                                                              │
│  FILTER BAR                                                  │
│  [All] [Scholarship] [Internship] [Fellowship] [Other]      │
│  Sort by: [Rank ▼]  [Deadline]  [Match Score]               │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  #1  ┌─────────────────────────────────────────────────┐   │
│      │ 🔴 CRITICAL · Due in 2 days                     │   │
│      │                                                  │   │
│      │ Google Generation Scholarship                   │   │
│      │ 💰 Scholarship  |  🌐 Remote  |  ★ 94% Match   │   │
│      │                                                  │   │
│      │ Deadline: March 15, 2025  (2 days left)         │   │
│      │ Award: $10,000 + Mentorship                     │   │
│      │ Eligibility: CS/IT students, CGPA ≥ 3.5        │   │
│      │                                                  │   │
│      │ Why #1?                                         │   │
│      │ "Highest urgency + strong profile match.        │   │
│      │  Your CGPA (3.8) meets threshold. CS degree     │   │
│      │  matches requirement. Financial need flag       │   │
│      │  aligns. Deadline in 2 days — act today."       │   │
│      │                                                  │   │
│      │ [▼ See Action Checklist]  [🔗 Apply Now]        │   │
│      └─────────────────────────────────────────────────┘   │
│                                                              │
│  #2  ┌─────────────────────────────────────────────────┐   │
│      │ 🔵 ROLLING · Apply ASAP                         │   │
│      │                                                  │   │
│      │ Microsoft Internship — Summer 2025              │   │
│      │ 💼 Internship  |  🏢 Hybrid  |  ★ 89% Match   │   │
│      │                  ...                             │   │
│      └─────────────────────────────────────────────────┘   │
│                                                              │
│  #3  [Collapsed card — click to expand]                     │
│  #4  [Collapsed card — click to expand]                     │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

### Expanded Action Checklist (Progressive Disclosure)

```
┌─────────────────────────────────────────────────────────────┐
│  ✅ Action Checklist — Google Generation Scholarship        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Deadline: March 15 (2 days)     ⏰ Set Reminder           │
│                                                             │
│  Documents Required:                                        │
│  ☐  Updated Resume/CV                                      │
│  ☐  Unofficial Transcript (CGPA proof)                     │
│  ☐  1 Recommendation Letter                                │
│  ☐  500-word Personal Statement                            │
│  ☐  Proof of enrollment                                    │
│                                                             │
│  Next Steps:                                               │
│  1. Visit application portal → [scholarships.google.com]   │
│  2. Create account or log in                               │
│  3. Complete Section A (Personal Info) — ~10 mins          │
│  4. Upload transcript and resume                           │
│  5. Write/paste personal statement                         │
│  6. Submit before 11:59 PM on March 15                    │
│                                                             │
│  ⚠️  From the email: "Applications after midnight          │
│      will not be reviewed regardless of timezone"          │
│                                                             │
│  [Mark as Applied ✓]    [Dismiss]    [🔗 Open Portal]     │
└─────────────────────────────────────────────────────────────┘
```

---

## Component Design Specifications

### Opportunity Card Anatomy

```
┌──── LEFT ACCENT BAR (4px, urgency color) ──────────────────┐
│                                                             │
│  [RANK #]  [URGENCY BADGE]                    [MATCH SCORE]│
│                                                             │
│  OPPORTUNITY TITLE (18px SemiBold)                         │
│  TYPE CHIP  |  LOCATION CHIP  |  AWARD/VALUE               │
│                                                             │
│  📅 Deadline: [DATE] — [RELATIVE TIME]  ← monospace font  │
│                                                             │
│  WHY THIS RANK? (Expandable — 2 lines preview)             │
│  Evidence quote in subtle blockquote style                 │
│                                                             │
│  [Checklist Button]                    [Apply Now →]       │
└─────────────────────────────────────────────────────────────┘

Design Details:
- Left accent bar color = urgency color (instant visual scan)
- Cards have 8px border radius, subtle box-shadow
- Hover state: slight elevation increase (shadow deepens)
- "Apply Now" button = filled indigo (primary action)
- "Checklist" button = outlined indigo (secondary action)
```

### Match Score Badge

```
★ 94% Match

Design:
- Ring/arc visualization (like a donut chart mini)
- Color: Green (80–100%), Yellow (60–79%), Gray (<60%)
- Tooltip on hover: "Based on degree, CGPA, skills, preferences"
- Never show a bad score prominently — gray it out below 50%
```

---

## Iconography System

```
Opportunity Types (consistent, recognizable):
💰 Scholarship      — Money bag / coin
💼 Internship       — Briefcase
🔬 Fellowship       — Microscope / scroll
🏆 Competition      — Trophy
📚 Research         — Books / magnifying glass
✈️  Exchange         — Airplane / globe

Urgency Icons:
🔴 Critical         — Filled red circle
🟠 Urgent           — Filled amber circle
🟡 Moderate         — Filled yellow-green circle
🟢 Comfortable      — Filled teal circle
🔵 Rolling          — Filled indigo circle
⚪ Unknown          — Outlined gray circle

Action Icons:
✅ Checklist item   — Checkbox
🔗 External link    — Chain link
⏰ Reminder         — Alarm clock
📋 Copy             — Clipboard
📤 Export           — Upload arrow
```

---

## Micro-interactions & Feedback

```
1. EMAIL UPLOAD
   - Drag & drop zone: highlights indigo on hover
   - On file drop: count animates up "Detected: 1... 2... 8 emails"
   - Success: green checkmark animates in

2. ANALYSIS BUTTON
   - Disabled state until min emails + profile filled
   - On click: button text changes to "Analyzing..." + spinner
   - Never disappear — always show what's happening

3. CARD EXPAND
   - Smooth accordion animation (200ms ease)
   - Checklist items have subtle slide-in stagger effect

4. MARK AS APPLIED
   - Card gets subtle green wash overlay
   - Strike-through on title
   - Moves to "Applied" section at bottom
   - Confetti micro-animation 🎉 (optional — celebrates action)

5. DEADLINE COUNTDOWN
   - Auto-refreshes if tab stays open
   - "2 days" → "1 day" transitions with subtle pulse animation
```

---

## Accessibility (Non-Negotiable)

```
✅ Color contrast ratio ≥ 4.5:1 for all text (WCAG AA)
✅ Never convey urgency by color alone — always icon + text label
✅ All interactive elements keyboard navigable
✅ Screen reader labels on all icon-only buttons
✅ Focus rings visible (indigo outline, 2px offset)
✅ Font size minimum 14px for any readable content
✅ Deadline dates in full format on hover (not just "2 days")
```

---

## Mobile Responsiveness

```
Desktop (>1024px):   2-column: sidebar profile + main card list
Tablet (768–1024px): Single column, full-width cards
Mobile (<768px):
  - Summary bar scrolls horizontally
  - Cards stack vertically, full width
  - "Apply Now" becomes sticky bottom bar on card expand
  - Checklist becomes bottom sheet (not inline)
  - Filter bar collapses into [Filter ▼] dropdown
```

---

## What Makes This Marketable

```
USEFUL:     Ranked list + checklist = zero cognitive load on student
USABLE:     Progressive disclosure = never overwhelming
TRUSTWORTHY: Evidence quotes from emails = "I can verify this"
SATISFYING: Match score + rank explanation = feels personalized
SHAREABLE:  Export to PDF = show advisor, share with friends
STICKY:     "Mark as Applied" tracker = reason to return
```

---

## Summary Card for Hackathon Team

```
┌─────────────────────────────────────────────────────────┐
│  DESIGN DECISIONS AT A GLANCE                          │
├─────────────────────────────────────────────────────────┤
│  Theme        Light mode default, dark toggle          │
│  Brand Color  Indigo #4F46E5 — academic + trustworthy  │
│  Critical     Red #EF4444 with soft red background     │
│  Urgent       Amber #F59E0B                            │
│  Moderate     Yellow-Green #84CC16                     │
│  Rolling      Indigo #6366F1 — distinct from urgency   │
│  Unknown      Slate Gray #94A3B8                       │
│  Font         Inter — clean, universal, free           │
│  Layout       Card list + progressive disclosure       │
│  Key UX       Recognition > Recall throughout          │
│  Mobile       Fully responsive, bottom sheets          │
└─────────────────────────────────────────────────────────┘
```

> **Design North Star**: Every visual decision should make a stressed student feel _seen, organized, and empowered_ — not more overwhelmed.
