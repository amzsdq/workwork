# Control overhead accounting

Controlled overlap can reduce idle while adding control-plane work. Separate:
- authoritative substantive work;
- useful SHADOW preparation that would otherwise occur after predecessor close;
- required checkpoint/authority/scheduler control work;
- redundant control work from excessive polling/tiny units.

The objective is long-run useful utilization. Zero idle is not automatically better if control overhead or abandoned predecessor capacity is excessive.

Prefer checks at natural unit boundaries rather than tight polling. Shorter units near handoff are justified only when authoritative measurements show reduced transfer tail outweighs added control cost.

Quantitative time/overlap/control-duration comparisons require authoritative server-side timing endpoints. Without them, report qualitative control-work counts/side effects rather than model-derived seconds.
