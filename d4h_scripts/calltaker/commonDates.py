import datetime

def strToDatetime(string):
  """
  Convert string to datetime in the local timezone
  """
  newdate = datetime.datetime.strptime(string, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=datetime.timezone.utc)
  return newdate.astimezone()
  
def numberOfDays(startDate, endDate) -> int:
  """
  Calculate over how many days the time span is, e.g. 3/19 12:30 to 3/20 11:00 is 2 days
  """
  addOne = 1 if endDate.hour > 0 or endDate.minute > 0 else 0
  delta = endDate.date() - startDate.date()
  return delta.days + addOne

def withoutTime(theDate):
  return theDate.replace(hour=0, minute=0, second=0, microsecond=0)
