#!/usr/bin/env python3
#
# CalltakerContext
# Track calltaker data
#
import sys
import datetime
sys.path.insert(1, '..')
import d4hcommon
from d4hcommon import commonDates

class CalltakerContext:

  def __init__(self):
    self.memberContext = d4hcommon.MemberContext()
    self.memberContext.initContext()
    self.dutyContext = d4hcommon.DutyContext()
 
  def dayCoverageHours(self, currentDate) -> int:
    """
    Returns total number of calltaker (half)hours
    """
    signUpHours = [0 for i in range(48)]
    calltakers = self.dutyContext.getCalltakerDuties()
    for dutyModel in calltakers:
      signups = self.dutyContext.callSignupsFromDutyModel(dutyModel)
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
    calltakers = self.dutyContext.getCalltakerDuties()
    for model in calltakers:
      signups = self.dutyContext.callSignupsFromDutyModel(model)
      for signup in signups:
        if signup.startDate().date() == day.date():
          list.append(signup)
    list.sort()
    return list

  def getCalltakerForTime(self,time) -> list:
    """
    Get the calltakers who was signed up at the time
    """
    calltakers = self.dutyContext.getCalltakerDuties()
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
      map[name] = [d4hcommon.AvailStatus.NoStatus for i in range(30)]
    todaydate = datetime.datetime.today()
    for model in self.dutyContext.duties:
      signups = self.dutyContext.callSignupsFromDutyModel(model)
      for signup in signups:
        if signup.dutyModel.memberName() not in names:
          continue
        delta = commonDates.differenceInDays(todaydate, signup.startDate())
        if delta >= 0 and delta < 30:
          map[signup.dutyModel.memberName()][delta] = signup.dutyModel.status()
    return map
