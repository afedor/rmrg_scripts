import datetime
from . import commonDates

class AttendanceModel:

  def __init__(self, model):
    self.model = model
    self.attRoleName = ""

  def date(self):
    return commonDates.strToDatetime(self.model['startsAt'])
    
  def endDate(self):
    return commonDates.strToDatetime(self.model['endsAt'])

  def memberId(self):
    return self.model['member']['id']

  def type(self):
    return self.model['activity']['resourceType']

  def roleId(self):
    return self.model['role']['id']

  def status(self):
    return self.model['status']

  def setRoleName(self, name):
    self.attRoleName = name

  def roleName(self):
    return self.attRoleName
