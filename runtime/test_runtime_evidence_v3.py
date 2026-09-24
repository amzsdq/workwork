import unittest
from dataclasses import replace
from runtime.RUNTIME_EVIDENCE_V3 import *

def marker(cid, ts, fetched=True): return RawMarkerEvidence(cid,fetched,ts)
def manifest(**kw):
    d=dict(schema_version="3",generator_version="g3",proof_id="proof",seed=7,ordinal_start=0,ordinal_end_exclusive=10,chunk_size=5,chunk_count=2,proven_unique_units=10,executed_assertion_count=4,failed_assertion_count=0,duplicate_ids_rejected=0,semantic_repeats_rejected=0,anomaly_count=0,ordered_chunk_hashes=("a","b"),previous_manifest_hash=None,manifest_hash=None); d.update(kw); return ManifestV3(**d)

class EvidenceV3Tests(unittest.TestCase):
    def test_clock_missing(self): self.assertEqual(eval_clock(marker(None,None),marker(2,"2026-01-01T00:20:00Z"),840).status,PredicateStatus.NOT_EXECUTED)
    def test_clock_unverified(self): self.assertEqual(eval_clock(marker(1,"2026-01-01T00:00:00Z",False),marker(2,"2026-01-01T00:20:00Z"),840).status,PredicateStatus.NOT_EXECUTED)
    def test_clock_bad_timestamp(self): self.assertEqual(eval_clock(marker(1,"bad"),marker(2,"2026-01-01T00:20:00Z"),840).status,PredicateStatus.FAIL)
    def test_clock_reversed(self): self.assertEqual(eval_clock(marker(1,"2026-01-01T00:20:00Z"),marker(2,"2026-01-01T00:00:00Z"),840).status,PredicateStatus.FAIL)
    def test_clock_under_target(self): self.assertEqual(eval_clock(marker(1,"2026-01-01T00:00:00Z"),marker(2,"2026-01-01T00:13:59Z"),840).status,PredicateStatus.FAIL)
    def test_clock_pass(self): self.assertEqual(eval_clock(marker(1,"2026-01-01T00:00:00Z"),marker(2,"2026-01-01T00:14:00Z"),840).status,PredicateStatus.PASS)
    def test_scheduler_no_attempt(self): self.assertEqual(eval_scheduler(SchedulerEvidence()).status,PredicateStatus.NOT_EXECUTED)
    def test_scheduler_no_readback(self): self.assertEqual(eval_scheduler(SchedulerEvidence(attempted=True)).status,PredicateStatus.NOT_EXECUTED)
    def test_scheduler_mismatch(self): self.assertEqual(eval_scheduler(SchedulerEvidence(True,True,False,"r")).status,PredicateStatus.FAIL)
    def test_scheduler_pass(self): self.assertEqual(eval_scheduler(SchedulerEvidence(True,True,True,"r")).status,PredicateStatus.PASS)
    def test_wake_missing_identity(self): self.assertEqual(eval_wake(WakeEvidence()).status,PredicateStatus.NOT_EXECUTED)
    def test_wake_incomplete(self): self.assertEqual(eval_wake(WakeEvidence("x")).status,PredicateStatus.NOT_EXECUTED)
    def test_wake_verified_miss(self): self.assertEqual(eval_wake(WakeEvidence("x",True,False,True,"r")).status,PredicateStatus.FAIL)
    def test_wake_pass(self): self.assertEqual(eval_wake(WakeEvidence("x",False,True,False,"r")).status,PredicateStatus.PASS)
    def test_substantive_proof_only(self): self.assertEqual(eval_substantive(ExecutedCheckEvidence(structural_proof_only=True)).status,PredicateStatus.NOT_EXECUTED)
    def test_substantive_missing_artifact(self): self.assertEqual(eval_substantive(ExecutedCheckEvidence(executed_count=1)).status,PredicateStatus.NOT_EXECUTED)
    def test_substantive_bad_hash(self): self.assertEqual(eval_substantive(ExecutedCheckEvidence("a",False,1,0)).status,PredicateStatus.FAIL)
    def test_substantive_zero_executed(self): self.assertEqual(eval_substantive(ExecutedCheckEvidence("a",True,0,0)).status,PredicateStatus.NOT_EXECUTED)
    def test_substantive_failed(self): self.assertEqual(eval_substantive(ExecutedCheckEvidence("a",True,3,1)).status,PredicateStatus.FAIL)
    def test_substantive_invalid_failed_count(self): self.assertEqual(eval_substantive(ExecutedCheckEvidence("a",True,1,2)).status,PredicateStatus.FAIL)
    def test_substantive_pass(self): self.assertEqual(eval_substantive(ExecutedCheckEvidence("a",True,3,0)).status,PredicateStatus.PASS)
    def test_aggregate_excludes_not_executed(self):
        rs=[PredicateResult("a",PredicateStatus.PASS),PredicateResult("b",PredicateStatus.FAIL),PredicateResult("c",PredicateStatus.NOT_EXECUTED)]
        self.assertEqual(aggregate_results(rs),{"executed_assertion_count":2,"failed_assertion_count":1})
    def test_promotion_blocks_fail(self): self.assertFalse(promotion_eligible([PredicateResult("a",PredicateStatus.FAIL)],True,True))
    def test_promotion_blocks_not_executed(self): self.assertFalse(promotion_eligible([PredicateResult("a",PredicateStatus.NOT_EXECUTED)],True,True))
    def test_promotion_requires_hash_terminal(self):
        rs=[PredicateResult("a",PredicateStatus.PASS)]; self.assertFalse(promotion_eligible(rs,False,True)); self.assertFalse(promotion_eligible(rs,True,False))
    def test_promotion_pass(self): self.assertTrue(promotion_eligible([PredicateResult("a",PredicateStatus.PASS)],True,True))
    def test_hash_deterministic(self):
        m=manifest(); self.assertEqual(compute_manifest_hash(m),compute_manifest_hash(m))
    def test_covered_field_changes_hash(self):
        m=manifest(); self.assertNotEqual(compute_manifest_hash(m),compute_manifest_hash(replace(m,seed=8)))
    def test_hash_ignores_manifest_hash_field(self):
        m=manifest(); self.assertEqual(compute_manifest_hash(m),compute_manifest_hash(replace(m,manifest_hash="junk")))
    def test_chain_valid(self):
        a=with_manifest_hash(manifest()); b=with_manifest_hash(manifest(ordinal_start=10,ordinal_end_exclusive=20,previous_manifest_hash=a.manifest_hash)); self.assertTrue(verify_manifest_chain([a,b]))
    def test_chain_detects_mutation(self):
        a=with_manifest_hash(manifest()); b=with_manifest_hash(manifest(ordinal_start=10,ordinal_end_exclusive=20,previous_manifest_hash=a.manifest_hash)); self.assertFalse(verify_manifest_chain([a,replace(b,seed=99)]))
    def test_eval_idempotent(self):
        e=SchedulerEvidence(True,True,True,"r"); self.assertEqual(eval_scheduler(e),eval_scheduler(e))

if __name__=="__main__": unittest.main()
