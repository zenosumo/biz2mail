import unittest
from grabphone import extract_phone_numbers

class TestPhoneNumberExtraction(unittest.TestCase):
    def test_single_phone_number(self):
        text = "Call me at +1 (555) 123-4567."
        result = extract_phone_numbers(text)
        self.assertEqual(result, "+1(555)1234567")

    def test_multiple_phone_numbers(self):
        text = "Here are two numbers: +1 (555) 123-4567, 0039 02 1234 5678."
        result = extract_phone_numbers(text)
        self.assertEqual(result, "+1(555)1234567;00390212345678")

    def test_no_phone_numbers(self):
        text = "There is no phone number here."
        result = extract_phone_numbers(text)
        self.assertEqual(result, "")

    def test_phone_numbers_with_varied_delimiters(self):
        text = "Contact us at (555)123.4567 or (555) 123 4567 or +1(555)123--4567."
        result = extract_phone_numbers(text)
        self.assertEqual(result, "(555)1234567;(555)1234567;+1(555)1234567")

    def test_international_phone_numbers(self):
        text = "International: +44 20 7946 0958, +33 1 42 68 53 00."
        result = extract_phone_numbers(text)
        self.assertEqual(result, "+442079460958;+33142685300")

    def test_commas_only_as_separators(self):
        text = "Numbers: +1 (555) 123-4567, (555) 654-3210."

if __name__ == '__main__':
    unittest.main()
