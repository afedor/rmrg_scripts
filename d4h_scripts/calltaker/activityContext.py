#!/usr/bin/env python3
#
# ActivityContext
# Gets information about events, incidents, and exercises
#
import datetime
import apiHelper
import commonDates
from activityModel import ActivityModel

class ActivityContext:

  def __init__(self):
    self.activities = []

  def requestActivities(self):
    self.requestActivitiesOfType('incidents')
    self.requestActivitiesOfType('events')
    self.requestActivitiesOfType('exercises')

  def requestActivitiesOfType(self, type):
    todaydate = datetime.datetime.now(datetime.timezone.utc)
    startDate = todaydate - datetime.timedelta(days=120)
    response = apiHelper.requestGet(type, {'after': startDate.strftime('%Y-%m-%dT%H:%M:%SZ')})
    for dict in response['results']:
      activity = ActivityModel(dict)
      self.activities.append(activity)

  def initContext(self):
    self.requestActivities()

  def draftActivities(self) -> list:
    list = []
    allowDate = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=5)
    for activity in self.activities:
      if activity.published() == False and activity.startDate() < allowDate:
        list.append(activity)
    return list
