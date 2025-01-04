#!/usr/bin/env python3
#
# MemberContext
# Gets information about members and groups
#
import datetime
import apiHelper
import commonDates

class MemberContext:

  def __init__(self):
    self.groups = []
    self.members = []
    self.memberGroups = []

  def requestGroups(self):
    response = apiHelper.requestGet('member-groups', {})
    self.groups = response['results']

  def requestMembers(self):
    response = apiHelper.requestGet('members', {})
    self.members = response['results']

  def requestMemberGroups(self, groupid):
    response = apiHelper.requestGet('member-group-memberships', {"group_id": groupid})
    self.memberGroups = response['results']

  def initContext(self):
    self.requestGroups()
    self.requestMembers()
    callGroup = self.groupIdentWithName("Calltaker")
    self.requestMemberGroups(callGroup)

  def groupIdentWithName(self, groupName) -> int:
    for group in self.groups:
      if group['title'] == groupName:
        return group['id']
    return 0;

  def memberWithIdent(self, ident) -> dict:
    for member in self.members:
      if ident == member["id"]:
        return member
    return {}

  def memberInGroup(self, member, groupId) -> bool:
    for memberGroup in self.memberGroups:
      gid = memberGroup["group"]["id"]
      gmemberId = memberGroup["member"]["id"]
      if gid == groupId and member["id"] == gmemberId:
        return True
    return False
    
  def membersInGroup(self, groupIdent) -> list:
    list = []
    for member in self.members:
      if self.memberInGroup(member, groupIdent):
        list.append(member)
    return list

  def memberGroupEmails(self, groupList) -> list:
    """
    Return the emails contained in the list
    """
    list = []
    for member in groupList:
      list.append(member['email']['value'])
    return list

  def memberGroupNames(self, groupList) -> list:
    """
    Return the names contained in the list
    """
    list = []
    for member in groupList:
      list.append(member['name'])
    return list
