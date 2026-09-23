# R4 server-commit span interpretation

## Can GitHub commit timestamps support PRODUCTIVE_WINDOW?

They can support a conservative statement that goal-directed durable work occurred at specific server-side points after START. They cannot establish continuous active work between those points because reasoning/tool latency/other activity is not directly observed.

## Permitted use

- identify first/last durable substantive-work anchors,
- corroborate that work continued after START,
- count durable decision-relevant outputs,
- detect long unexplained gaps for later investigation.

## Forbidden use

- compute `active_work_sec` as last_commit - first_commit,
- call the entire span productive time,
- replace START/END marker WORKED,
- infer model reasoning time.

## R4 reporting

Use `active_work_sec=null` and `productive_ratio=null` unless better instrumentation appears. Report substantive-unit count and optionally server-side durable-work span as supporting evidence only.
