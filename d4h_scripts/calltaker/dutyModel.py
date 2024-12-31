import datetime
import commonDates

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

  def roleTitle(self):
    role = self.duty['role']
    if 'title' in role:
      return role['title']
    return ''
