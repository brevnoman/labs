import unittest


def get_res(txt):
    return sum([1 for x in txt.lower() if x in 'aeiou'])



class CountVowelsTest(unittest.TestCase):
    def test_count_viwels(self):
        input_string = "allow eto ti?"
        result = get_res(input_string)
        self.assertEqual(result, 5)