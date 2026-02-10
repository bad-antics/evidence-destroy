import unittest,sys,os,tempfile
sys.path.insert(0,os.path.join(os.path.dirname(__file__),"..","src"))
from evidence_destroy.core import SecureWiper

class TestWiper(unittest.TestCase):
    def test_dry_run(self):
        w=SecureWiper()
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"test data")
            path=f.name
        r=w.wipe_file(path,dry_run=True)
        self.assertEqual(r["status"],"would_wipe")
        self.assertTrue(os.path.exists(path))
        os.unlink(path)

if __name__=="__main__": unittest.main()
