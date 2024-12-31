#!/usr/bin/env python3
#
# CalltakerContext
# Track calltaker data
#
import datetime
import apiHelper
import commonDates
from ordinalCallSignup import OrdinalCallSignup
from dutyModel import DutyModel

class CalltakerContext:

  def __init__(self):
    self.calltakers = []
 
  def callSignupsFromData(self, calltaker) -> list:
    """
    Separates a multi-day calltaker duty into individual days and returns a list of signups
    for each day
    """
    list = []
    days = commonDates.numberOfDays(calltaker.startDate(), calltaker.endDate())
    for i in range(0, days):
      signup = OrdinalCallSignup(calltaker, i)
      list.append(signup)
    return list
    
  def isDayComplete(self, currentDate) -> bool:
    """
    Returns true if calltaker timeslots fill up the entire day
    """
    signUpHours = [0 for i in range(48)]
    for dutyModel in self.calltakers:
      signups = self.callSignupsFromData(dutyModel)
      for signup in signups:
        if currentDate.date() != signup.startDate().date():
          continue
        for j in range(int(signup.startHour() * 2), int(signup.endHour() * 2)):
          signUpHours[j] = True
    total = signUpHours.count(True)
    return (total == 48)
        
  def getCalltakerDuties(self) -> list:
    """
    Get the calltaker duties
    """
    today = datetime.datetime.today()
    startMonth = commonDates.withoutTime(datetime.datetime(today.year, today.month, 1))
    response = apiHelper.requestGet('duties', {"after": startMonth.strftime('%Y-%m-%dT%H:%M:%SZ')})
    results = response['results']
    totalSize = int(response['totalSize']) 
    page = 1
    while totalSize >= 250:
      response = apiHelper.requestGet('duties', {"after": startMonth.strftime('%Y-%m-%dT%H:%M:%SZ'), "page": page})
      results = results + response['results']
      totalSize -= 250
    self.calltakers = []
    for dict in results:
      model = DutyModel(dict)
      if model.roleTitle() == 'Calltaker':
        self.calltakers.append(model)
  
    return self.calltakers

  def getSignupsForDay(self,day) -> list:
    """
    Get the calltakers who are signed up for a particular day. Returns a list of OrdinalCallSignup
    """
    list = []
    for model in self.calltakers:
      signups = self.callSignupsFromData(model)
      for signup in signups:
        if signup.startDate().date() == day.date():
          list.append(signup)
    return list    #.sort(key=signup.compare)

