import logging

from capsphere.common.domain.bank import bank_columns_mapping

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.ERROR)
logging.getLogger(__name__).setLevel(logging.DEBUG)


def get_total_columns(bank_name: str) -> int:
    try:
        bank_name_lower = bank_name.lower()
        return bank_columns_mapping[bank_name_lower]
    except KeyError:
        raise ValueError(f"Invalid bank name: {bank_name}. Please provide a valid bank name.")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {str(e)}")


# def convert_bank_schema(transaction_dict: dict) -> dict:
#
#     bank_name = transaction_dict['bank_name']
#
#     LOGGER.info(f"Getting output for bank {bank_name}...")
#
#     try:
#
#         match bank_name:
#
#             case 'AmBank' | 'AmBank Islamic':
#                 start_balance, end_balance, total_debit, total_credit, average_debit, average_credit, month = from_ambank(
#                     transaction_dict['transaction'])
#             case 'Maybank':
#                 start_balance, end_balance, total_debit, total_credit, average_debit, average_credit, month = from_maybank(
#                     transaction_dict['transaction'])
#             case 'Maybank Islamic':
#                 start_balance, end_balance, total_debit, total_credit, average_debit, average_credit, month = from_maybank_islamic(
#                     transaction_dict['transaction'])
#             case 'CIMB':
#                 bank_name = 'CIMB ISLAMIC'
#                 start_balance, end_balance, total_debit, total_credit, average_debit, average_credit, month = from_cimb(
#                     transaction_dict['transaction'])
#             case 'CIMB BANK' | 'CIMB ISLAMIC':
#                 start_balance, end_balance, total_debit, total_credit, average_debit, average_credit, month = from_cimb(
#                     transaction_dict['transaction'])
#             case 'RHB':
#                 start_balance, end_balance, total_debit, total_credit, average_debit, average_credit, month = from_rhb(
#                     transaction_dict['transaction'])
#             case 'Hong Leong':
#                 bank_name = 'Hong Leong Bank'
#                 start_balance, end_balance, total_debit, total_credit, average_debit, average_credit, month = from_hong_leong(
#                     transaction_dict['transaction'])
#             case 'PUBLIC BANK':
#                 start_balance, end_balance, total_debit, total_credit, average_debit, average_credit, month = from_public_bank(
#                     transaction_dict['transaction'])
#             case 'Alliance Bank Malaysia Berhad':
#                 start_balance, end_balance, total_debit, total_credit, average_debit, average_credit, month = from_alliance(
#                     transaction_dict['transaction'])
#             case 'BANK ISLAM':
#                 start_balance, end_balance, total_debit, total_credit, average_debit, average_credit, month = from_bank_islam(
#                     transaction_dict['transaction'])
#             case _:
#                 raise RuntimeError(f'{bank_name} is not included in function')
#
#         return {
#             'bank': bank_name,
#             'month': month,
#             'Total Debit': pd.to_numeric(total_debit),
#             'Total Credit': pd.to_numeric(total_credit),
#             'Average Debit': pd.to_numeric(average_debit),
#             'Average Credit': pd.to_numeric(average_credit),
#             'Opening Balance': pd.to_numeric(start_balance),
#             'Closing Balance': pd.to_numeric(end_balance)
#         }
#
#     except Exception as err:
#         raise RuntimeError(f'Error getting output for bank {bank_name}: {err}')
