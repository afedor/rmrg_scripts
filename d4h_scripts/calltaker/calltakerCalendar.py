#
# Subclass of HTML calendar for creating calltaker schedule
import calendar
import datetime
from calendar import HTMLCalendar

# Based on https://stackoverflow.com/a/1458077/1639671
class CalltakerCalendar(HTMLCalendar):
  def __init__(self, context, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.context = context
    self.monthDate = datetime.datetime.today()

  def setCurrentMonthDate(self, thedate):
    self.monthDate = thedate

  def formatday(self, day, weekday):
    """
    Return a day as a table cell.
    """
    if day == 0:
      return super().formatday(day, weekday)

    todayDate = datetime.datetime.today()
    tomorrowDate = datetime.datetime.today() + datetime.timedelta(1)
    currentDate = datetime.datetime(self.monthDate.year, self.monthDate.month, day)
    isComplete = self.context.isDayComplete(currentDate)
    dayclass = ''
    if todayDate.date() == currentDate.date():
      dayclass = 'todcomp' if isComplete else 'todpart'
    elif tomorrowDate.date() == currentDate.date():
      dayclass = 'daycomp' if isComplete else 'tmrpart'
    else:
      dayclass = 'daycomp' if isComplete else 'daypart'
    callList = self.context.getSignupsForDay(currentDate)
    htmlString = '<td class="%s">%d' % (dayclass, day)
    if len(callList) > 0:
      htmlString += '<ul>'
      for call in callList:
        startStr = str(call.startDate().strftime('%H%M'))
        endStr = str(call.endDate().strftime('%H%M'))
        if endStr == '0000':
          endStr = '2400'
        htmlString += '<li>' + call.dutyModel.memberLast() + ': ' + startStr + '-' + endStr + '</li>'
      htmlString += '</ul>'
    htmlString += '</td>'
    return htmlString

