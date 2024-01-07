import unittest
from EasyToCacheLib.easy_to_cache import Cache
import time


class Test(unittest.TestCase):
    def setUp(self) -> None:
        self.cache = Cache("EasyToCacheLib/Data/TestFolder/test_file.json", False)

    def test_add(self):
        self.cache.clear()
        self.cache.add("a", 10)
        self.cache.add("b", 20)
        self.cache.add("c", 100000)
        self.assertEqual(3, self.cache.length)
        self.assertEqual("a", self.cache.pop_items(0)[0])
        self.assertEqual("b", self.cache.pop_items(0)[0])
        self.assertEqual("c", self.cache.pop_items(0)[0])

    def test_sort_by_date(self):
        self.cache.clear()
        for letter in "abc":
            self.cache.add(letter, letter*5)
            time.sleep(0.1)

        self.cache.sort_by_date()
        self.assertEqual(3, self.cache.length)
        self.assertEqual("c", self.cache.pop_items(0)[0])
        self.assertEqual("b", self.cache.pop_items(0)[0])
        self.assertEqual("a", self.cache.pop_items(0)[0])

    def test_take_skip_reverse(self):
        self.cache.clear()
        for letter in "abcdefgh":
            self.cache.add(letter, letter*5)

        self.cache.skip(2).take(4).revere()

        self.cache.sort_by_date()
        self.assertEqual(4, self.cache.length)
        self.assertEqual("f", self.cache.pop_items(0)[0])
        self.assertEqual("e", self.cache.pop_items(0)[0])
        self.assertEqual("d", self.cache.pop_items(0)[0])
        self.assertEqual("c", self.cache.pop_items(0)[0])

    def test_handler(self):
        self.cache.clear()

        self.cache.set_key_handler(lambda x: False if x == "c" else True)\
            .set_value_handler(lambda x: False if x == "bbbbb" else True)

        for letter in "abcdefgh":
            self.cache.add(letter, letter*5)

        self.assertEqual(False, self.cache.contain("c"))
        self.assertEqual(False, self.cache.contain("b"))


def main():
    Test()


if __name__ == "__main__":
    main()

