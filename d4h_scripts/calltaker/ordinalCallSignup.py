import datetime
import commonDates
from dutyModel import DutyModel

class OrdinalCallSignup:

  def __init__(self, model, offset):
    self.dutyModel = model
    self.dayOffset = offset

  def startDate(self):
    if self.dayOffset > 0:
      newDate = commonDates.withoutTime(self.dutyModel.startDate()) + datetime.timedelta(days=self.dayOffset)
      return newDate
    return self.dutyModel.startDate()

  def endDate(self):
    days = commonDates.numberOfDays(self.dutyModel.startDate(), self.dutyModel.endDate())
    if self.dayOffset+1 < days:
      return commonDates.withoutTime(self.startDate()) + datetime.timedelta(days=self.dayOffset+1)
    return self.dutyModel.endDate()

  def startHour(self):
    return self.startDate().hour + self.startDate().minute / 60.0;

  def endHour(self):
    endHour = self.endDate().hour + self.endDate().minute / 60.0;
    if endHour == 0:
      endHour = 24
    return endHour

  def __eq__(self, other):
      return self.startDate() == other.startDate()

  def __lt__(self, other):
      return self.startDate() < other.startDate()
