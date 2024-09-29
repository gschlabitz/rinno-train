import unittest
from datetime import datetime
from main import (
    aggregate_training_programs,
    has_completed_training_program,
    count_program_completions,
    date_from_string,
    is_within_fiscal_year,
    generate_completion_report_by_year,
    index_expired_programs,
    index_expiring_programs,
    generate_expiration_report_by_date
)


class TestAggregateTrainingPrograms(unittest.TestCase):
    training_records = [
        {'name': 'Jim', 'completions': [{'name': 'A'}]},
        {'name': 'Jack', 'completions': [{'name': 'A'}, {'name': 'B'}]},
        {'name': 'John', 'completions': [{'name': 'C'}, {'name': 'C'}]},
        {'name': 'Jill', 'completions': []},
        {'name': 'James', 'completions': [{'name': 'D'}, {'name': 'E'}]},
        {'name': 'Jane', 'completions': [
            {'name': 'F'}, {'name': 'A'}, {'name': 'C'}]},
    ]

    def test_aggregate_programs(self):
        result = aggregate_training_programs(self.training_records)
        self.assertEqual(result, ['A', 'B', 'C', 'D', 'E', 'F'])


class TestHasCompletedTrainingProgram(unittest.TestCase):
    completions = [{'name': 'A'}, {'name': 'B'}, {'name': 'C'}]

    def test_has_completed_program(self):
        self.assertTrue(has_completed_training_program('A', self.completions))

    def test_has_not_completed_program(self):
        self.assertFalse(has_completed_training_program('F', self.completions))


class TestCountProgramCompletions(unittest.TestCase):
    training_records = [
        {'name': 'Jim', 'completions': [{'name': 'A'}]},
        {'name': 'Jack', 'completions': [{'name': 'A'}, {'name': 'B'}]},
        {'name': 'John', 'completions': [{'name': 'C'}, {'name': 'C'}]},
        {'name': 'Jill', 'completions': []},
        {'name': 'James', 'completions': [{'name': 'D'}, {'name': 'E'}]},
        {'name': 'Jane', 'completions': [
            {'name': 'F'}, {'name': 'A'}, {'name': 'C'}]},
    ]

    def test_count_programs(self):
        result = count_program_completions(
            ['A', 'B', 'C'],
            self.training_records
        )
        self.assertEqual(result, {'A': 3, 'B': 1, 'C': 2})


class TestDateFromString(unittest.TestCase):
    def test_valid_date(self):
        self.assertEqual(date_from_string('1/1/2024'), datetime(2024, 1, 1))

    def test_invalid_date(self):
        self.assertEqual(date_from_string('13/1/2024'), None)


class TestIsWithinFiscalYear(unittest.TestCase):
    def test_within_fiscal_year(self):
        self.assertTrue(is_within_fiscal_year(2024, '7/1/2023'))
        self.assertTrue(is_within_fiscal_year(2024, '1/1/2024'))
        self.assertTrue(is_within_fiscal_year(2024, '6/30/2024'))

    def test_outside_fiscal_year(self):
        self.assertFalse(is_within_fiscal_year(2024, '1/1/2023'))
        self.assertFalse(is_within_fiscal_year(2024, '6/30/2023'))
        self.assertFalse(is_within_fiscal_year(2024, '7/2/2024'))
        self.assertFalse(is_within_fiscal_year(2024, '10/10/2024'))


class TestGenerateCompletionReportByYear(unittest.TestCase):
    training_records = [
        {'name': 'Jim', 'completions': [
            {'name': 'A', 'timestamp': '1/1/2024'}
        ]},
        {'name': 'Jack', 'completions': [
            {'name': 'A', 'timestamp': '7/2/2023'},
            {'name': 'B', 'timestamp': '7/1/2023'}
        ]},
        {'name': 'John', 'completions': [
            {'name': 'C', 'timestamp': '2/11/2024'},
            {'name': 'C', 'timestamp': '2/12/2023'}
        ]},
        {'name': 'Jill', 'completions': []},
        {'name': 'James', 'completions': [
            {'name': 'A', 'timestamp': '6/30/2023'},
            {'name': 'B', 'timestamp': '7/1/2024'},
            {'name': 'C', 'timestamp': '7/2/2024'},
            {'name': 'E', 'timestamp': '1/1/2024'}
        ]},
        {'name': 'Jane', 'completions': [
            {'name': 'A', 'timestamp': '6/30/2024'},
            {'name': 'C', 'timestamp': '3/30/2024'},
            {'name': 'F', 'timestamp': '3/30/2024'}
        ]},
    ]

    def test_generate_completion_report_by_year(self):
        result = generate_completion_report_by_year(
            self.training_records,
            2024,
            ['A', 'B', 'C']
        )
        self.assertEqual(result, {
            'A': ['Jack', 'Jane', 'Jim'],
            'B': ['Jack'],
            'C': ['Jane', 'John'],
        })


class TestIndexExpiredPrograms(unittest.TestCase):
    completions = [
        {'name': 'A', 'expires': '1/1/2024'},
        {'name': 'A', 'expires': '1/1/2023'},
        {'name': 'A', 'expires': '1/1/2022'},
        {'name': 'B', 'expires': '10/11/2024'},
        {'name': 'B', 'expires': '1/11/2024'},
        {'name': 'B', 'expires': '10/11/2023'},
        {'name': 'C', 'expires': '8/10/2024'},
        {'name': 'C', 'expires': '9/10/2024'},
        {'name': 'C', 'expires': '10/10/2024'},
        {'name': 'D', 'expires': '10/9/2024'},
        {'name': 'D', 'expires': '1/9/2024'},
        {'name': 'D', 'expires': '10/9/2023'},
        {'name': 'E', 'expires': '1/1/2025'},
        {'name': 'F', 'expires': '11/1/2024'}
    ]

    def test_no_completions(self):
        result = index_expired_programs([], datetime(2024, 1, 1))
        self.assertEqual(result, {})

    def test_expired_programs(self):
        result = index_expired_programs(
            self.completions, datetime(2024, 10, 10))
        self.assertEqual(result, {
            'A': '1/1/2024',
            'D': '10/9/2024'
        })

    def test_expires_soon(self):
        result = index_expiring_programs(
            self.completions, datetime(2024, 10, 10), 30)
        self.assertEqual(result, {
            'B': '10/11/2024',
            'C': '10/10/2024',
            'F': '11/1/2024'
        })


class TestGenerateExpirationReportByDate(unittest.TestCase):
    training_records = [
        {'name': 'Jim', 'completions': [
            {'name': 'A', 'expires': '1/1/2024'},
            {'name': 'B', 'expires': '7/1/2024'},
            {'name': 'C', 'expires': '10/1/2024'}
        ]},
        {'name': 'Jack', 'completions': [
            {'name': 'D', 'expires': None}
        ]},
        {'name': 'John', 'completions': [
            {'name': 'A', 'expires': '9/30/2024'},
            {'name': 'A', 'expires': '1/30/2024'},
            {'name': 'A', 'expires': '9/30/2023'}
        ]},
        {'name': 'Jill', 'completions': [
            {'name': 'D', 'expires': '1/9/2025'}
        ]},
        {'name': 'James', 'completions': [
            {'name': 'E', 'expires': '1/1/2025'}
        ]},
        {'name': 'Jane', 'completions': [
            {'name': 'F', 'expires': '10/10/2024'},
            {'name': 'F', 'expires': '8/10/2024'},
            {'name': 'F', 'expires': '5/10/2024'}
        ]}
    ]

    def test_generate_expiration_report_by_date(self):
        result = generate_expiration_report_by_date(
            self.training_records,
            '10/1/2024'
        )
        self.assertEqual(result, [
            {
                'name': 'Jane',
                'expired_training': [
                    {'name': 'F', 'expiration': '10/10/2024',
                        'status': 'expires soon'}
                ]
            },
            {
                'name': 'Jim',
                'expired_training': [
                    {'name': 'A', 'expiration': '1/1/2024', 'status': 'expired'},
                    {'name': 'B', 'expiration': '7/1/2024', 'status': 'expired'},
                    {'name': 'C', 'expiration': '10/1/2024',
                        'status': 'expires soon'}
                ]
            },
            {
                'name': 'John',
                'expired_training': [
                    {'name': 'A', 'expiration': '9/30/2024', 'status': 'expired'}
                ]
            }
        ])


if __name__ == '__main__':
    unittest.main()
