import datetime
from . import commonDates

class AttendanceModel:

  def __init__(self, model):
    self.model = model
    self.attRoleName = ""

  def __eq__(self, other):
    if isinstance(other, self.__class__):
      return self.identifier() == other.identifier()
    return False

  def identifier(self):
    return self.model['id']
  
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
