# A unit 002 — scheduler isolation analysis

The probe has one intentional scheduler handoff point: PRIMARY_A schedules B once at start, then stops scheduler writes. B may schedule only the later observer after its own parallel work is durable.

This avoids simultaneous scheduler writers during the intended A/B overlap. It also means scheduler conflict count can be interpreted cleanly: any collision during the overlap is a protocol failure rather than expected contention.

For future multi-worker generalization, a single dispatcher/owner should allocate wake slots while workers use immutable claims. Allowing every parallel worker to reschedule the same automation would scale poorly because the schedule is a single mutable register.
