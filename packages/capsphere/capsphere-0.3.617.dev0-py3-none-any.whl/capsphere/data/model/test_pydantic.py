import unittest

from capsphere.data.model.investment import Investment


class TestPydantic(unittest.TestCase):

    def test_investment(self):
        investment = Investment(invested_amount=2500.00, created_by='me', updated_by='you',
                                investor_application_id=10, loan_id=25, invested_amount_percent=25.00,
                                created_at='datetime.date.today()', updated_at='datetime.date.today()')
        print(investment)
        data = {}
        investment_base = Investment.from_dict(data)
        print(investment_base)
