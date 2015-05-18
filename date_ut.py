import calendar
from datetime import date

def get_date_range(date_str):
    if not date_str:
        return []
    date_str = str(date_str)
    year = int(date_str[:4])
    month = int(date_str[5:])
    if date_str[4] == 'M':
        if month < 1:
            month = 1
        if month > 12:
            month = 12
        end = "%d-%02d-%02d" % (year, month, calendar.monthrange(year, month)[1])
        start = "%d-%02d-%02d" % (year, month, 1)
    elif date_str[4] == 'Q':
        quarter = month
        if quarter < 1:
            quarter = 1
        if quarter > 4:
            quarter = 4
        mon_end = quarter * 3
        mon_start = mon_end - 2
        end = "%d-%02d-%02d" % (year, mon_end, calendar.monthrange(year, mon_end)[1])
        start = "%d-%02d-%02d" % (year, mon_start, 1)
    return [start, end]

def test():
    for i in range(0,13):
        print "month %d" % i
        print get_date_range("2015M%d" % i)
    for i in range(0,5):
        print "quarter %d" % i
        print get_date_range("2015Q%d" % i)

#test()
