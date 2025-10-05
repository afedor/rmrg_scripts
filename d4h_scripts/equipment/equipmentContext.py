#!/usr/bin/env python3
#
# Equipment
# Track equipment data
#
import sys
import datetime
sys.path.insert(1, '..')
import d4hcommon
from d4hcommon import commonDates

class EquipmentContext:

  def __init__(self):
    self.memberContext = d4hcommon.MemberContext()
    self.memberContext.initContext()
    self.dutyContext = d4hcommon.DutyContext()
 
  def truckAndOhvEquipment(self) -> list:
    tid = self.memberContext.groupIdentWithName("Trucks")
    self.memberContext.requestMemberGroups(tid)
    truckList = self.memberContext.membersInGroup(tid)
    oid = self.memberContext.groupIdentWithName("OHV")
    self.memberContext.requestMemberGroups(oid)
    ohvList = self.memberContext.membersInGroup(oid)
    truckList.extend(ohvList)
    return truckList

  def equipmentCheckouts(self, member) -> list:
    return self.dutyContext.dutiesForMember(member["id"])

  def memberWithCheckout(self, duty):
    memberId = duty.memberIdFromEquipmentNote()
    return self.memberContext.memberWithIdent(memberId)


