import date_utils


def check_date_interval(initial_date, final_date):
    if not date_utils.is_date_interval_valid(initial_date, final_date):
        raise Exception("A data inicial deve ser menor do que ou igual à data final!")