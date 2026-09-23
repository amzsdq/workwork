import unittest
from RUNTIME_EVIDENCE_PROCESSOR_REFERENCE import Probe,SERVER_CLOCK,HARNESS_V2,classify,retrospective_wake,derive_bounds

def base(**kw):
    d=dict(probe_id="P",target_runtime_sec=10,clock_protocol=SERVER_CLOCK,start_marker_comment_id=1,start_marker_created_at="2026-01-01T00:00:00Z",end_marker_comment_id=2,end_marker_created_at="2026-01-01T00:00:11Z",harness_version=HARNESS_V2,scheduler_write_ok=True,scheduler_state_ok=True,checkpoint_saved=True,clean_close=True,substantive_unit_count=100)
    d.update(kw);return Probe(**d)

class HarnessQualityGateTests(unittest.TestCase):
    def test_id_only_work_cannot_clean_pass(self):
        r=classify(base(harness_valid=False,generated_unique_units=2048,semantic_unique_units=0))
        self.assertEqual(r["result"],"AMBIGUOUS")
        self.assertIn("HARNESS_V2_SEMANTIC_WORK_NOT_PROVEN",r["anomalies"])
    def test_semantic_work_can_clean_pass(self):
        r=classify(base(harness_valid=True,generated_unique_units=100,semantic_unique_units=100))
        self.assertEqual(r["result"],"CLEAN_PASS_PENDING_WAKE")
    def test_wake_cannot_rescue_tainted_harness(self):
        r=retrospective_wake(classify(base(harness_valid=False,semantic_unique_units=0)),True)
        self.assertEqual(r["result"],"AMBIGUOUS")
        self.assertIsNone(derive_bounds([r])["server_clock_safe_lower_bound_sec"])

if __name__=="__main__":unittest.main()
