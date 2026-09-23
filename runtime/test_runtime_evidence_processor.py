import unittest
from RUNTIME_EVIDENCE_PROCESSOR_REFERENCE import Probe, SERVER_CLOCK, classify, retrospective_wake, derive_bounds

class RuntimeEvidenceProcessorTests(unittest.TestCase):
    def clean(self, **kw):
        base=dict(probe_id="P",target_runtime_sec=1320,case_id="SC-A22",clock_protocol=SERVER_CLOCK,start_marker_comment_id=1,start_marker_created_at="2026-01-01T00:00:00Z",end_marker_comment_id=2,end_marker_created_at="2026-01-01T00:22:02Z",scheduler_write_ok=True,scheduler_state_ok=True,checkpoint_saved=True,clean_close=True,substantive_unit_count=1)
        base.update(kw); return Probe(**base)

    def test_target_survives_classification(self):
        r=classify(self.clean()); self.assertEqual(r["target_runtime_sec"],1320)

    def test_clean_wake_advances_bound(self):
        r=retrospective_wake(classify(self.clean()),True)
        self.assertEqual(r["result"],"CLEAN_PASS_WAKE_OK")
        self.assertEqual(derive_bounds([r])["server_clock_safe_lower_bound_sec"],1320)

    def test_pending_without_wake_does_not_advance(self):
        r=retrospective_wake(classify(self.clean()),False)
        self.assertIsNone(derive_bounds([r])["server_clock_safe_lower_bound_sec"])

    def test_reversed_main_pair_invalid(self):
        r=classify(self.clean(start_marker_created_at="2026-01-01T00:23:00Z"))
        self.assertEqual(r["result"],"CLOCK_EVIDENCE_INVALID")

    def test_missing_marker_id_invalid(self):
        r=classify(self.clean(start_marker_comment_id=None))
        self.assertEqual(r["result"],"CLOCK_EVIDENCE_INVALID")

    def test_non_duration_precedence(self):
        p=self.clean(non_duration_failure=True,start_marker_comment_id=None,end_marker_comment_id=None)
        r=classify(p); self.assertEqual(r["result"],"NON_DURATION_FAIL"); self.assertEqual(r["boundary_effect"],"NONE")

    def test_forced_stop_precedes_clean_pass(self):
        r=classify(self.clean(forced_stop_or_timeout=True))
        self.assertEqual(r["result"],"DURATION_FAIL_CANDIDATE")

    def test_workload_exhaustion_under_target_is_harness_defect(self):
        r=classify(self.clean(end_marker_created_at="2026-01-01T00:03:00Z",close_trigger="WORKLOAD_EXHAUSTED"))
        self.assertEqual(r["result"],"HARNESS_UNDER_TARGET")

    def test_productive_reverse_fails_closed_without_crash(self):
        p=self.clean(work_start_marker_comment_id=3,work_start_marker_created_at="2026-01-01T00:10:00Z",pre_close_marker_comment_id=4,pre_close_marker_created_at="2026-01-01T00:09:59Z")
        r=classify(p); self.assertIsNone(r["productive_window_sec"]); self.assertFalse(r["productive_marker_pair_valid"])

    def test_r9_exact_intervals(self):
        p=self.clean(probe_id="R9",start_marker_created_at="2026-09-23T17:47:04Z",work_start_marker_comment_id=3,work_start_marker_created_at="2026-09-23T17:47:12Z",pre_close_marker_comment_id=4,pre_close_marker_created_at="2026-09-23T18:08:09Z",end_marker_created_at="2026-09-23T18:09:06Z")
        r=classify(p); self.assertEqual(r["worked_sec"],1322); self.assertEqual(r["prearm_overhead_sec"],8); self.assertEqual(r["productive_window_sec"],1257); self.assertEqual(r["close_overhead_sec"],57)

if __name__ == "__main__": unittest.main()
