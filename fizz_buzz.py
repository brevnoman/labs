import unittest


def get_reply(number):
	if number%5==0 and number%3==0:
		return 'FizzBuzz'
	elif number%3==0:
		return 'Fizz'
	elif number%5==0:
		return 'Buzz'
	else:
		return ''


class FizzBuzzTest(unittest.TestCase):
	def test_fizz(self):
		input_num = 3
		result = get_reply(input_num)
		self.assertEqual(result, "Fizz")
	def test_buzz(self):
		input_num = 5
		result = get_reply(input_num)
		self.assertEqual(result, "Buzz")
	def test_fizzbuzz(self):
		input_num = 15
		result = get_reply(input_num)
		self.assertEqual(result, "FizzBuzz")
	def test_else(self):
		input_num = 4
		result = get_reply(input_num)
		self.assertTrue(result == "")
