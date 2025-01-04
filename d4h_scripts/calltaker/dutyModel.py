import datetime
import commonDates
from enum import Enum

class AvailStatus(Enum):
  NoStatus = 0
  Available = 1
  Work = 2
  Marginal = 3
  Unavailable = 4

class DutyModel:

  def __init__(self, model):
    self.duty = model

  def startDate(self):
    return commonDates.strToDatetime(self.duty['startsAt'])
    
  def endDate(self):
    return commonDates.strToDatetime(self.duty['endsAt'])

  def memberName(self):
    member = self.duty['member']
    return member['name']

  def memberLast(self):
    member = self.duty['member']
    return member['name'].split()[-1]

  def type(self):
    return self.duty['type']

  def roleTitle(self):
    role = self.duty['role']
    if 'title' in role:
      return role['title']
    return ''

  def status(self):
    astatus = AvailStatus.Available if self.type().lower() == "on" else AvailStatus.Unavailable
    if "Marginal" in self.roleTitle():
      if "All" in self.roleTitle():
        astatus = AvailStatus.Marginal
      else:
        astatus = AvailStatus.Work
    return astatus
