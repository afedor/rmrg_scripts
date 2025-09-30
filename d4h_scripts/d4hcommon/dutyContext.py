#!/usr/bin/env python3
#
# DutyContext
# Track duties
#
import datetime
from . import apiHelper
from . import commonDates
from .ordinalCallSignup import OrdinalCallSignup
from .dutyModel import DutyModel
from .dutyModel import AvailStatus
from .memberContext import MemberContext

class DutyContext:

  def __init__(self):
    """
    Get the all duties
    """
    self.duties = []
    today = datetime.datetime.today()
    startDate = today - datetime.timedelta(days=40)
    response = apiHelper.requestGet('duties', {"after": startDate.strftime('%Y-%m-%dT%H:%M:%SZ')})
    results = response['results']
    totalSize = int(response['totalSize'])
    page = 1
    while totalSize >= 250:
      response = apiHelper.requestGet('duties', {"after": startDate.strftime('%Y-%m-%dT%H:%M:%SZ'), "page": page})
      results = results + response['results']
      totalSize -= 250
      page = page + 1
    for dict in results:
      model = DutyModel(dict)
      self.duties.append(model)

  def getCalltakerDuties(self) -> list:
    """
    Get the calltaker duties
    """
    calltakers = []
    for model in self.duties:
      if model.roleTitle() == 'Calltaker':
        calltakers.append(model)
    return calltakers

  def callSignupsFromDutyModel(self, duty) -> list:
    """
    Separates a multi-day duty into individual days and returns a list of signups
    for each day
    """
    list = []
    days = commonDates.numberOfDays(duty.startDate(), duty.endDate())
    for i in range(0, days):
      signup = OrdinalCallSignup(duty, i)
      list.append(signup)
    return list
