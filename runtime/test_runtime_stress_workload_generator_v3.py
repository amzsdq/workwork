import unittest
from itertools import islice
from runtime.RUNTIME_STRESS_WORKLOAD_GENERATOR import (
    UNITS_PER_EPOCH, PROOF_ID, iter_units, expected_invariants,
    evaluate_concrete_checks, iter_evaluated_chunks,
)

class GeneratorV3IntegrationTests(unittest.TestCase):
    def test_high_offset_remains_o1_addressable_semantics(self):
        rows=list(islice(iter_units("x",10**9),3))
        self.assertEqual([r.ordinal for r in rows],[10**9,10**9+1,10**9+2])
    def test_labels_do_not_drive_executed_count(self):
        u=next(iter_units())
        self.assertGreater(len(expected_invariants(u)),0)
        c=next(iter_evaluated_chunks(chunk_size=1))
        self.assertEqual(c.executed_assertion_count,len(evaluate_concrete_checks(u)))
    def test_actual_checks_are_invoked(self):
        u=next(iter_units())
        outcomes=evaluate_concrete_checks(u)
        self.assertTrue(outcomes)
        self.assertTrue(all(isinstance(o.passed,bool) for o in outcomes))
    def test_chunk_counts_actual_outcomes(self):
        c=next(iter_evaluated_chunks(chunk_size=7))
        per=len(evaluate_concrete_checks(next(iter_units())))
        self.assertEqual(c.executed_assertion_count,7*per)
        self.assertEqual(c.failed_assertion_count,0)
    def test_chunk_is_bounded_and_contiguous(self):
        c=next(iter_evaluated_chunks(start_ordinal=123,chunk_size=11))
        self.assertEqual((c.ordinal_start,c.ordinal_end_exclusive),(123,134))
        self.assertEqual(c.proven_unique_units,11)
    def test_chunk_hash_deterministic(self):
        a=next(iter_evaluated_chunks("s",9,5)); b=next(iter_evaluated_chunks("s",9,5))
        self.assertEqual(a.chunk_hash,b.chunk_hash)
    def test_chunk_hash_changes_with_range(self):
        a=next(iter_evaluated_chunks("s",9,5)); b=next(iter_evaluated_chunks("s",10,5))
        self.assertNotEqual(a.chunk_hash,b.chunk_hash)
    def test_runtime_duplicate_guard_bounded_per_chunk(self):
        c=next(iter_evaluated_chunks(chunk_size=UNITS_PER_EPOCH+1))
        self.assertEqual(c.duplicate_ids_rejected,0)
    def test_proof_is_units_not_assertions(self):
        c=next(iter_evaluated_chunks(chunk_size=3))
        self.assertEqual(c.proof_id,PROOF_ID)
        self.assertEqual(c.proven_unique_units,3)
        self.assertGreater(c.executed_assertion_count,c.proven_unique_units)
    def test_chunk_hash_changes_with_seed(self):
        a=next(iter_evaluated_chunks("seed-a",9,5))
        b=next(iter_evaluated_chunks("seed-b",9,5))
        self.assertNotEqual(a.chunk_hash,b.chunk_hash)
    def test_multiple_chunks_preserve_continuity(self):
        it=iter_evaluated_chunks("s",123,4)
        a=next(it); b=next(it); c=next(it)
        self.assertEqual((a.ordinal_start,a.ordinal_end_exclusive),(123,127))
        self.assertEqual(b.ordinal_start,a.ordinal_end_exclusive)
        self.assertEqual(c.ordinal_start,b.ordinal_end_exclusive)
        self.assertEqual(c.ordinal_end_exclusive,135)
        self.assertEqual(a.anomaly_count+b.anomaly_count+c.anomaly_count,0)
    def test_chunk_hash_chain_links_predecessors(self):
        it=iter_evaluated_chunks("chain",100,3)
        a=next(it); b=next(it); c=next(it)
        self.assertEqual(a.previous_chunk_hash,"")
        self.assertEqual(b.previous_chunk_hash,a.chunk_hash)
        self.assertEqual(c.previous_chunk_hash,b.chunk_hash)

    def test_chain_context_changes_later_hash(self):
        chained=iter_evaluated_chunks("chain",100,3)
        next(chained); second=next(chained)
        independent=next(iter_evaluated_chunks("chain",103,3))
        self.assertNotEqual(second.chunk_hash,independent.chunk_hash)

    def test_invalid_chunk_size(self):
        with self.assertRaises(ValueError): next(iter_evaluated_chunks(chunk_size=0))

if __name__=="__main__": unittest.main()
