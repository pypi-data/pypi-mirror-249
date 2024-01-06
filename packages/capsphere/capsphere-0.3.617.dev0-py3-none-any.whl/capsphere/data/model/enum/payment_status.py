from enum import Enum


class LoanStage(Enum):
    NORMAL = "NORMAL"
    DEFAULTED = "DEFAULTED"
    EXPIRED = "EXPIRED"


class PaidStatus(Enum):
    PAID = "Borrower Paid",
    MISS = "Miss"


class LoanPaymentStatus(Enum):
    MANAGER_APPROVED = 'Manager Approved'
    MANAGER_REJECTED = 'Manager Rejected'
    PENDING = 'Pending'
