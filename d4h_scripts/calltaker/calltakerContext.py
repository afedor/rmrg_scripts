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
from dutyModel import AvailStatus
from memberContext import MemberContext

class CalltakerContext:

  def __init__(self):
    self.duties = []
    self.memberContext = MemberContext()
    self.memberContext.initContext()
 
  def getDuties(self) -> list:
    """
    Get the all duties
    """
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
    return self.duties

  def getCalltakerDuties(self) -> list:
    """
    Get the calltaker duties
    """
    calltakers = []
    for model in self.duties:
      if model.roleTitle() == 'Calltaker':
        calltakers.append(model)
    return calltakers

  def callSignupsFromDutyModel(self, calltaker) -> list:
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
    
  def dayCoverageHours(self, currentDate) -> int:
    """
    Returns total number of calltaker (half)hours
    """
    signUpHours = [0 for i in range(48)]
    calltakers = self.getCalltakerDuties()
    for dutyModel in calltakers:
      signups = self.callSignupsFromDutyModel(dutyModel)
      for signup in signups:
        if currentDate.date() != signup.startDate().date():
          continue
        for j in range(int(signup.startHour() * 2), int(signup.endHour() * 2)):
          signUpHours[j] = True
    total = signUpHours.count(True)
    return total

  def isDayComplete(self, currentDate) -> bool:
    """
    Returns true if calltaker timeslots fill up the entire day
    """
    total = self.dayCoverageHours(currentDate)
    return (total == 48)
        
  def getSignupsForDay(self,day) -> list:
    """
    Get the calltakers who are signed up for a particular day. Returns a list of OrdinalCallSignup
    """
    list = []
    calltakers = self.getCalltakerDuties()
    for model in calltakers:
      signups = self.callSignupsFromDutyModel(model)
      for signup in signups:
        if signup.startDate().date() == day.date():
          list.append(signup)
    list.sort()
    return list

  def getCalltakerForTime(self,time) -> list:
    """
    Get the calltakers who was signed up at the time
    """
    calltakers = self.getCalltakerDuties()
    for model in calltakers:
      if model.startDate() < time and model.endDate() > time:
        return model
    return None

  def calltakerEmailList(self) -> list:
    gid = self.memberContext.groupIdentWithName("Calltaker")
    memberList = self.memberContext.membersInGroup(gid)
    return self.memberContext.memberGroupEmails(memberList)

  def calltakerNameList(self) -> list:
    gid = self.memberContext.groupIdentWithName("Calltaker")
    memberList = self.memberContext.membersInGroup(gid)
    return self.memberContext.memberGroupNames(memberList)

  def calltakerStatusMap(self) -> dict:
    names = self.calltakerNameList()
    map = {}
    for name in names:
      map[name] = [AvailStatus.NoStatus for i in range(30)]
    todaydate = datetime.datetime.today()
    for model in self.duties:
      signups = self.callSignupsFromDutyModel(model)
      for signup in signups:
        if signup.dutyModel.memberName() not in names:
          continue
        delta = commonDates.differenceInDays(todaydate, signup.startDate())
        if delta >= 0 and delta < 30:
          map[signup.dutyModel.memberName()][delta] = signup.dutyModel.status()
    return map
