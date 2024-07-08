from datetime import datetime, timedelta


def format_date(date):
    try:
        return datetime.strptime(date, "%d/%m/%Y %H:%M:%S")
    except Exception as ex:
        raise Exception("Error when formatting date: " + ex.__str__())


def is_date_interval_valid(initial_date, final_date):
    return initial_date <= final_date


def is_valid_date_interval_within_limit(initial_date, final_date, max_interval):
    return final_date <= initial_date + timedelta(days=max_interval)


def is_date_within_limit(date, max_interval, assume_valid_interval=True):
    today = datetime.today()

    if assume_valid_interval:
        return is_valid_date_interval_within_limit(today, date, max_interval)

    return is_date_interval_valid(today, date) and is_valid_date_interval_within_limit(today, date, max_interval)





