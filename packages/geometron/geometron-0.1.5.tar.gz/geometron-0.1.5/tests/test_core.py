import unittest
from .context import geometron


class CoreTestCase(unittest.TestCase):
    def test_fake_function(self):
        actual = geometron.core.fake_function()
        expected = "Hello world!"
        self.assertEqual(expected, actual)

    def test(self):
        fake = geometron.core.FakeClass();
        actual = fake.name
        expected = 'unknown'
        self.assertEqual(expected, actual)
        fake = geometron.core.FakeClass(name="test")
        actual = fake.name
        expected = 'test'
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
