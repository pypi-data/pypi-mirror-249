from capsphere.data.db.entity import LoanPaymentEntity
from capsphere.data.db.entity.abstract_entity import DbEntity
from capsphere.data.model.loan_payment import LoanPayment
from capsphere.service import DataProcessor


class LoanPaymentCreator(DataProcessor[DbEntity, DbEntity]):
    """
    This class processes the creation of a LoanPayment record in the loan_payments table
    """

    def __init__(self,
                 data: dict,
                 loan_payment_entity: LoanPaymentEntity):
        super().__init__(data,
                         loan_payment_entity=loan_payment_entity)
        self.loan_payment_entity = loan_payment_entity

    # TODO add validation

    def process(self) -> LoanPayment:
        loan_payment = LoanPayment.from_dict(self.data)
        loan_payment.created_by_id = int(self.data["user_id"])
        loan_payment.updated_by_id = int(self.data["user_id"])
        return self.loan_payment_entity.create(loan_payment)
