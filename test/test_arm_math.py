import unittest
import range

class TestRange(unittest.TestCase):

    def test_range(self):
        min_val = -10
        max_val = 10
        mid_point = (max_val + min_val) / 2.0

        r = range.Range(min_val, max_val)
        self.assertEqual(r.min_val, min_val)
        self.assertEqual(r.max_val, max_val)
        self.assertEqual(r.interpolate(0.5), 0)

        self.assertTrue(r.contains(min_val))
        self.assertTrue(r.contains(max_val))
        self.assertTrue(r.contains(mid_point))
        self.assertFalse(r.contains(min_val-1))
        self.assertFalse(r.contains(max_val+1))

        self.assertEqual(r.clip(min_val - 1), min_val)
        self.assertEqual(r.clip(min_val), min_val)
        self.assertEqual(r.clip(mid_point), mid_point)
        self.assertEqual(r.clip(max_val), max_val)
        self.assertEqual(r.clip(max_val + 1), max_val)

        self.assertEqual(r.normalize(0), .5)
        self.assertEqual(r.normalize(-20), 0)
        self.assertEqual(r.normalize(300), 1)
        self.assertEqual(r.normalize(-10), 0)
        self.assertEqual(r.normalize(10), 1)
        self.assertEqual(r.normalize(3), .65)



if __name__ == '__main__':
    unittest.main()
