# Control overhead accounting

Controlled overlap can reduce idle while adding control-plane work. Track that cost instead of treating all overlap as free.

Separate:
- authoritative substantive work,
- useful SHADOW preparation that would otherwise occur after predecessor close,
- required checkpoint/authority/scheduler control work,
- redundant control work caused by overly frequent polling or tiny units.

The target is maximum long-run useful utilization. A handoff with zero idle is not automatically better if it requires excessive repeated state reads/writes or abandons large predecessor residual capacity.

Prefer event checks at natural unit boundaries rather than tight polling. During the handoff window, modestly shorter units are justified only when they reduce measured transfer tail enough to offset added control overhead.
