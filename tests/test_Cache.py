from Cache import Cache
import unittest

class TestCache(unittest.TestCase):

    def test_empty(self):
        cache = Cache()
        response = cache.query([])
        self.assertEqual(response, None)

    def test_sum_tuple(self):
        cache = Cache()
        cache.add([], "test")
        response = cache.query([])
        self.assertEqual(response, "test")
        response = cache.query([[[1,2], [3,4]]])
        self.assertEqual(response, None)

if __name__ == '__main__':
    unittest.main()

