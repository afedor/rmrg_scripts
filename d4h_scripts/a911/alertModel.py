import datetime, sys, os
from enum import Enum
# Custom
sys.path.insert(1, '..')
from d4hcommon import commonDates

class AlertModel:

  def __init__(self, model):
    self.alert = model

  def startDate(self):
    return commonDates.strToDatetime(self.alert['sent'])
    
  def description(self):
    return self.alert['description']

  def identifier(self):
    return self.alert['id']

  def cad_code(self):
    return self.alert['cad_code']

  def devices(self):
    responses = self.alert['responses']
    devices = []
    for response in responses:
      dev = response['device']['id']
      res = response['response']
      devices.append({'identifier': dev, 'response': res})
    return devices
