#!/usr/bin/env python3
#
# Attendance
# Gets information event attendance
#
from . import apiHelper
from .attendanceModel import AttendanceModel
from .roleContext import RoleContext

class AttendanceContext:

  def __init__(self, activityId):
    self.activityId = activityId
    self.list = []
    self.roleContext = RoleContext()
    response = apiHelper.requestGet("attendance", {'activity_id': activityId})
    for dict in response['results']:
      attendance = AttendanceModel(dict)
      self.list.append(attendance)

  def attendanceCount(self):
    total = 0
    for model in self.list:
      if model.status() == "ATTENDING":
        total += 1
    return total
  
  def attendanceList(self):
    return self.list.copy()
  
  def memberAttendance(self, memberId):
    for attendance in self.list:
      if attendance.memberId() == memberId:
        return attendance
    return None

  def allLeadRoleAttendance(self):
    leads = []
    for model in self.list:
      if model.status() != "ATTENDING":
        continue
      roleName = self.roleContext.roleNameForId(model.roleId())
      if "Lead" in roleName or "Calltaker" in roleName:
        model.setRoleName(roleName)
        leads.append(model)
    return leads

  def putAttending(self, dict):
    request = apiHelper.requestPost("attendance", dict)

  def updateAttending(self, identifier, dict):
    request = apiHelper.requestPatch(f"attendance/{identifier}", dict)

  def deleteAttending(self, identifier):
    request = apiHelper.requestDelete(f"attendance/{identifier}")