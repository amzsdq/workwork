# Handoff-window task admission

Before successor READY, owner continues useful work. Near expected handoff, prefer bounded units so a large new unit does not dominate transfer latency.

Baseline:
- outside handoff window: normal substantive units;
- inside handoff window before READY: prefer bounded units whose estimated duration fits remaining lead/safety budget;
- after valid READY: admit no new ordinary unit; finish current safe unit, checkpoint, transfer.

Estimated unit duration is a control estimate, not empirical timing proof. Actual unit-tail/lead/handoff timing used to validate this rule must come from authoritative server-side endpoints; otherwise record the quantitative outcome as unresolved.

Compare adaptive estimation only if authoritative observations show meaningful benefit over this simple bounded-window rule.
