from datetime import datetime, timedelta

# Get the last trading date.
def getLastDate():
    if datetime.today().date().weekday() == 5:
        # Saturday
        return (datetime.today() - timedelta(days=1)).date()
    elif datetime.today().date().weekday() == 6:
        # Sunday
        return (datetime.today() - timedelta(days=2)).date()
    else:
        return datetime.today().date()


# Given a date, get the previous trading date.
def getPreviousDate(curDate):
    givenDate = datetime.fromisoformat(curDate.strftime('%Y-%m-%d'))
    if curDate.weekday() == 0:
        # Monday
        return (givenDate - timedelta(days=3)).date()
    elif curDate.weekday() == 5:
        # Saturday
        return (givenDate - timedelta(days=1)).date()
    elif curDate.weekday() == 6:
        # Sunday
        return (givenDate - timedelta(days=2)).date()
    else:
        return (givenDate - timedelta(days=1)).date()
