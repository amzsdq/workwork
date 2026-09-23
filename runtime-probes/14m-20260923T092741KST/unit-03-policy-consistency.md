# Unit 03 — Policy/close-reserve consistency

Probe: STRICT-14M-20260923T092741KST

Useful checks completed:
- Close reserve estimator correctly refuses numeric reserve when no direct samples exist and keeps close overhead separate from safety margin.
- Utility model correctly treats planned gap and actual idle gap as different quantities.
- Therefore this probe must preserve direct timestamps and avoid deriving a production cap from theoretical duty-cycle improvement.

Implication for later Phase B/C:
A longer observed runtime is useful only if repeated clean-close and continuation evidence remains strong. Current coarse ascent should focus on identifying the empirical boundary; policy complexity remains deferred.

W3 activity: read -> reconcile -> decision analysis -> immutable checkpoint write.
