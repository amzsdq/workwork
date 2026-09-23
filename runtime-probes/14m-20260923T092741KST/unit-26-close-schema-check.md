# Unit 26 — Close schema check

Probe: STRICT-14M-20260923T092741KST

Final close will not invent useful_work_sec. Because connector waits cannot be separated with stopwatch precision, active/useful work will be represented by the sustained evidence-producing window plus completed unit count, with useful_work_sec left null/unknown where precision is unavailable.

This preserves measurement integrity while still demonstrating sustained substantive work.
