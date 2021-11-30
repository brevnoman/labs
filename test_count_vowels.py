from count_vowels import get_res
import unittest


class CountVowelsTest(unittest.TestCase):

    def test_count_vowels(self):
        input_string = "allow eto ti?"
        result = get_res(input_string)
        self.assertEqual(result, 5)
