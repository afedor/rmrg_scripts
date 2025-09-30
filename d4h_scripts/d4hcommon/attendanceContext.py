#!/usr/bin/env python3
#
# Attendance
# Gets information event attendance
#
import datetime
from . import apiHelper
from . import commonDates
from .attendanceModel import AttendanceModel
from .roleContext import RoleContext

class AttendanceContext:

  def __init__(self, activityId):
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


