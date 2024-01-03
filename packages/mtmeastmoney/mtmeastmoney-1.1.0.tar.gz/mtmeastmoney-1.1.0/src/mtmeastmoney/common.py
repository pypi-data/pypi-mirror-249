import datetime


def today(fmt="%Y%m%d"):
    return datetime.datetime.now().strftime(fmt)


def yesterday(fmt="%Y%m%d"):
    return (datetime.datetime.now() - datetime.timedelta(days=1)).strftime(fmt)
