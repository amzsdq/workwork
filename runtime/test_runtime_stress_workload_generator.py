import unittest
from math import gcd
from RUNTIME_STRESS_WORKLOAD_GENERATOR import batch, validate_semantic_uniqueness, epoch_parameters

class GeneratorTests(unittest.TestCase):
    def test_50000_identity_and_semantic_unique(self):
        rows=batch("stress",0,50000)
        self.assertEqual(len({r["case_id"] for r in rows}),50000)
        self.assertTrue(validate_semantic_uniqueness(rows))

    def test_epoch_zero_and_one_are_not_id_only_variants(self):
        self.assertNotEqual(epoch_parameters(0),epoch_parameters(1))

    def test_reserve_step_is_coprime(self):
        self.assertEqual(gcd(17,91),1)

    def test_full_close_reserve_coverage(self):
        reserves={epoch_parameters(e)[2] for e in range(91)}
        self.assertEqual(reserves,set(range(30,121)))

    def test_marker_skew_full_cycle(self):
        skews={epoch_parameters(e)[1] for e in range(121)}
        self.assertEqual(skews,set(range(-60,61)))

    def test_near_boundary_signs(self):
        self.assertEqual(epoch_parameters(0)[0],-1)
        self.assertEqual(epoch_parameters(1)[0],1)
        self.assertEqual(epoch_parameters(2)[0],-2)
        self.assertEqual(epoch_parameters(3)[0],2)

if __name__=="__main__":unittest.main()
