#!/usr/bin/env python3
#
# RoleContext
# Track roles
#
import apiHelper

class RoleContext:

  def __init__(self):
    response = apiHelper.requestGet('roles', {})
    self.list = response['results']

  def roleNameForId(self, identity):
    for dict in self.list:
      if dict["id"] == identity:
        return dict["title"]
    return ""
