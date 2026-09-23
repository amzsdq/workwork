# Unit 23 — W3 profile risk note

Probe: PROBE-14M-20260923T095323KST

W3 MIXED_IO is operationally relevant because frequent read/write boundaries introduce tool latency and checkpoint opportunities resembling ordinary relay maintenance. A clean W3 pass therefore has better operational relevance than a pure compute-only stress run, but it may also include external latency that should not be mistaken for useful-work seconds.

Classification remains based on elapsed runtime + clean close, with independent tool failures separated when explicit.
