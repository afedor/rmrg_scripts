import datetime
from . import commonDates
from enum import Enum

class ActivityModel:

  def __init__(self, model):
    self.model = model

  def identity(self):
    return self.model['id']

  def startDate(self):
    return commonDates.strToDatetime(self.model['startsAt'])
    
  def endDate(self):
    return commonDates.strToDatetime(self.model['endsAt'])

  def synopsis(self):
    return self.model['referenceDescription']

  def countAttendance(self):
    return self.model['countAttendance']

  def type(self):
    return self.model['resourceType']

  def published(self):
    return self.model['published']

  def viewURL(self):
    typeName = self.type().lower() + 's'
    return "https://rmrg.team-manager.us.d4h.com/team/" + typeName + "/view/" + str(self.identity())

