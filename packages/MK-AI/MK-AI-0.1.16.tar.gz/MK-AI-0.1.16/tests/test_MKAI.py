import unittest
import src.mk_ai.MKAI as MKAI

class TestMKAI(unittest.TestCase):
    def test_MKAI(self):
        self.assertEqual(MKAI().classify("/Users/jminding/Documents/Research/Star Images 2/O/Altinak.jpg"), ("O", 1.0))

unittest.main()



