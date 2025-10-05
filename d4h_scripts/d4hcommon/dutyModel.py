import datetime
from . import commonDates
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

  def memberId(self):
    member = self.duty['member']
    return member['id']

  def memberName(self):
    member = self.duty['member']
    return member['name']

  def memberLast(self):
    member = self.duty['member']
    return member['name'].split()[-1]

  def memberEmail(self):
    email = self.duty['member']['email']
    return email['value']

  def type(self):
    return self.duty['type']

  def roleTitle(self):
    role = self.duty['role']
    if 'title' in role:
      return role['title']
    return ''

  def notes(self):
    return self.duty["notes"]

  def status(self):
    astatus = AvailStatus.Available if self.type().lower() == "on" else AvailStatus.Unavailable
    if "Unavailable" in self.roleTitle():
      astatus = AvailStatus.Unavailable
    elif "Marginal" in self.roleTitle():
      if "All" in self.roleTitle():
        astatus = AvailStatus.Marginal
      else:
        astatus = AvailStatus.Work
    return astatus

  def memberIdFromEquipmentNote(self):
    list = self.notes().split(',')
    if not list:
      return 0
    memberId = list[0]
    if memberId:
      return int(memberId)
    return 0

  def commentFromEquipmentNote(self):
    list = self.notes().split(',')
    if len(list) < 2:
      return ""
    return list[1];

