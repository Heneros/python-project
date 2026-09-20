import unittest
from name_func import get_formatted_name

class NamesTest(unittest.TestCase):

    def test_first(self):
        form_text = get_formatted_name('Jackie', 'Chan')
        self.assertEqual(form_text, 'Jackie Chan')

if __name__ == '__main__':
    unittest.main()


