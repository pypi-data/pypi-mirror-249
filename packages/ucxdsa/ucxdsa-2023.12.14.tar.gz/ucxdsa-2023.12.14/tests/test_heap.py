import unittest

from dsa.heap import Heap

class TestHeap(unittest.TestCase):
    def test_create(self):
        h = Heap()
        self.assertEqual(h.count(), 0)
    
    def test_add(self):
        h = Heap()

        for _ in range(20):
            h.insert(_)
        self.assertEqual(h.count(), 20)

    def test_delete(self):
        h = Heap()

        for _ in range(20):
            h.insert(_)

        i = 19
        while not h.is_empty():
            v = h.pop()
            self.assertEqual(v, i)
            i = i - 1

        self.assertTrue(h.is_empty())
