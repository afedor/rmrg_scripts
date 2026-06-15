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

  def startDateStr(self):
    return self.model['startsAt']
    
  def endDateStr(self):
    return self.model['endsAt']
  
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

  def hasCustomFields(self):
    return 'customFieldValues' in self.model
  
  def allCustomFieldValues(self):
    if self.hasCustomFields == False:
      return []
    values = []
    for field in self.model['customFieldValues']:
      values.append(field['value'])
    return values
  
  def cadCode(self):
    values = self.allCustomFieldValues()
    for value in values:
      if "BCFD" in value:
        return value[4:]
    return ""

