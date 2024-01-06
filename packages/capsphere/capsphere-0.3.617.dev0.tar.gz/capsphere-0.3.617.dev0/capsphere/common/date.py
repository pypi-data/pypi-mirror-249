import re
import time

from datetime import datetime

from dateutil.relativedelta import relativedelta

## Date Formats
# "ddmmm"
# "dd/mm/yyyy"
# "dd/mm"
# "dd/mm/yy"
# "ddmmyy"
# "dd-mm-yyyy"
# "mmm dd"

MONTH_DICT = {
    '01': 'Jan',
    '02': 'Feb',
    '03': 'Mar',
    '04': 'Apr',
    '05': 'May',
    '06': 'Jun',
    '07': 'Jul',
    '08': 'Aug',
    '09': 'Sep',
    '10': 'Oct',
    '11': 'Nov',
    '12': 'Dec'
}


def convert_date(date_string: str, year_str: str = None):
    current_year = int(time.strftime('%Y')[-2:])
    current_century = int(time.strftime('%Y')[:-2]) * 100

    if '-' in date_string:

        date_obj = datetime.strptime(date_string, '%d-%m-%Y')
        formatted_date = date_obj.strftime('%b %Y')

    elif '/' in date_string:

        if len(date_string) == 5:

            month_num = date_string.split('/')[1]
            month = MONTH_DICT.get(month_num)
            formatted_date = month + " " + year_str

        else:

            date_obj = datetime.strptime(date_string, '%d/%m/%Y')
            formatted_date = date_obj.strftime('%b %Y')

    elif len(date_string) == 4:

        raise NotImplementedError("format: dmyy")

    elif len(date_string) == 5:

        if '-' in date_string:

            month_num, year = date_string.split('-')

        elif re.search('[a-zA-Z]', date_string):

            month_num = [k for k, v in MONTH_DICT.items() if v == date_string[2:5]][0]
            year = year_str

        else:

            month_num, year = date_string[1:3], date_string[3:]

        if len(year) == 2:
            year_int = int(year)
            century_adjustment = current_century if year_int <= current_year else (current_century - 100)
            year = str(century_adjustment + year_int)

        formatted_date = datetime.strptime(month_num + year, '%m%Y').strftime('%b %Y')

    elif len(date_string) == 6:

        month_num, year = date_string[2:4], date_string[4:]

        if len(year) == 2:
            year_int = int(year)
            century_adjustment = current_century if year_int <= current_year else (current_century - 100)
            year = str(century_adjustment + year_int)

        formatted_date = datetime.strptime(month_num + year, '%m%Y').strftime('%b %Y')

    else:

        raise ValueError(f'Invalid date: date_string: {date_string}, year: {year_str}')

    return formatted_date


def modify_datestr(date_str: str,
                   years: int = 0,
                   months: int = 0,
                   days: int = 0) -> str:
    """
    Modify a date by adding or subtracting years, months, and days.

    :param date_str: The date as a string in the format 'YYYY-MM-DD'.
    :param years: The number of years to add (or subtract if negative).
    :param months: The number of months to add (or subtract if negative).
    :param days: The number of days to add (or subtract if negative).
    :return: The modified date as a string.
    """
    # Convert the string to a datetime object
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")

    # Modify the date
    modified_date_obj = date_obj + relativedelta(years=years, months=months, days=days)

    # Convert the new datetime object back to a string
    modified_date_str = modified_date_obj.strftime("%Y-%m-%d")

    return modified_date_str
