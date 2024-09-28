import unittest
from datetime import datetime
from main import index_expired_programs


class TestIndexExpiredPrograms(unittest.TestCase):
    completions = [
        {'name': 'A', 'expires': '1/1/2024'},
        {'name': 'B', 'expires': '10/11/2024'},
        {'name': 'C', 'expires': '10/10/2024'},
        {'name': 'D', 'expires': '10/9/2024'},
        {'name': 'E', 'expires': '1/1/2025'},
        {'name': 'F', 'expires': '11/1/2024'}
    ]

    def test_no_completions(self):
        result = index_expired_programs([], datetime(2024, 1, 1))
        self.assertEqual(result, None)

    def test_expired_programs(self):
        result = index_expired_programs(
            self.completions, datetime(2024, 10, 10))
        self.assertEqual(result, {
            'A': '1/1/2024',
            'D': '10/9/2024'
        })

    def test_expires_soon(self):
        result = index_expired_programs(
            self.completions, datetime(2024, 10, 10), 30)
        self.assertEqual(result, {
            'B': '10/11/2024',
            'C': '10/10/2024',
            'F': '11/1/2024'
        })


if __name__ == '__main__':
    unittest.main()
