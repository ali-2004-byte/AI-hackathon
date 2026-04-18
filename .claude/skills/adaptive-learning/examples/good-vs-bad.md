# Good vs. Bad Reflections

````carousel
```markdown
### [2026-04-03] Windows Pathing
- MISTAKE/PREFERENCE: Agent used / in PowerShell.
- WHY: Linux habits.
- NEW RULE: Always use \ for Windows tool calls.
```
**SIGNAL LEVEL: HIGH (10/10)** 
Why: It's actionable, specific, and solves a recurring technical bottleneck.
<!-- slide -->
```markdown
### [2026-04-03] Code Style
- MISTAKE/PREFERENCE: The user wants the code to be good.
- WHY: Better readability.
- NEW RULE: Write better code.
```
**SIGNAL LEVEL: LOW (1/10)** 
Why: This is "Token-Slop." It provides zero actionable guidance for the next agent session.
<!-- slide -->
```markdown
### [2026-04-03] Architecture - React Hooks
- MISTAKE/PREFERENCE: Preference for 'useMemo' on all expensive object literals.
- WHY: Prevents unnecessary downstream re-renders in the heavy dashboard.
- NEW RULE: In `src/features/*`, always wrap complex style/config objects in `useMemo`.
```
**SIGNAL LEVEL: TOP-TIER (10/10)** 
Why: It captures "Tribal Knowledge" that a generic model would never know.
````
