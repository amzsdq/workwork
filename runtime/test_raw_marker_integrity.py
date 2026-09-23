import unittest
from RAW_MARKER_INTEGRITY import validate_marker, validate_lifecycle

class RawMarkerTests(unittest.TestCase):
    def m(self,i,body,t):return {"id":i,"body":body,"created_at":t}
    def test_current_compact_role_format(self):
        r=self.m(1,"START_MARKER probe_id=P case_id=C","2026-01-01T00:00:00Z")
        self.assertTrue(validate_marker(r,1,"START","P","C").valid)
    def test_id_mismatch(self):
        r=self.m(9,"START_MARKER probe_id=P","2026-01-01T00:00:00Z")
        self.assertFalse(validate_marker(r,1,"START","P").valid)
    def test_probe_mismatch(self):
        r=self.m(1,"START_MARKER probe_id=OTHER","2026-01-01T00:00:00Z")
        self.assertFalse(validate_marker(r,1,"START","P").valid)
    def test_bad_created_at(self):
        r=self.m(1,"START_MARKER probe_id=P","local-time")
        self.assertFalse(validate_marker(r,1,"START","P").valid)
    def test_lifecycle_order(self):
        ids={"START":1,"WORK_START":2,"PRE_CLOSE":3,"END":4}
        out=validate_lifecycle(
            self.m(1,"START_MARKER probe_id=P","2026-01-01T00:00:00Z"),
            self.m(2,"WORK_START_MARKER probe_id=P","2026-01-01T00:00:10Z"),
            self.m(3,"PRE_CLOSE_MARKER probe_id=P","2026-01-01T00:00:09Z"),
            self.m(4,"END_MARKER probe_id=P","2026-01-01T00:00:20Z"),ids,"P")
        self.assertFalse(out["valid"]);self.assertIn("LIFECYCLE_ORDER_INVALID",out["errors"])

if __name__=="__main__":unittest.main()
