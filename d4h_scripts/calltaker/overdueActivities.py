#!/usr/bin/env python3
#
# OverdueActivitiesReminder
# Downloads past activities and flags ones that are still in draft form
#
import sys
import argparse
import datetime
# HTML
import dominate
from dominate.tags import *
# Custom
import apiHelper
import commonDates
from activityModel import ActivityModel
from activityContext import ActivityContext
from config import *
# Email
import smtplib
from email.message import EmailMessage
from email.headerregistry import Address
from calltakerContext import CalltakerContext

context=0

def overdueActivities() -> list:
  context = ActivityContext()
  context.initContext()
  calltakerContext = CalltakerContext()
  calltakerContext.getDuties()

  list = context.draftActivities()
  overdue = []
  for activity in list:
    dict = {}
    coordinator = calltakerContext.getCalltakerForTime(activity.startDate())
    name = ""
    email = ""
    if activity.type() != "Incident":
      name = "Group Leader"
      email = "1901@rockymountainrescue.org"
    elif coordinator is not None:
      name = coordinator.memberName()
      email = coordinator.memberEmail()
    dict["name"] = name
    dict["email"] = email
    dict["activity"] = activity
    overdue.append(dict)
  return overdue

def formatCallTakerHtml(dict):
  """
  Format overdue activity
  """
  doc = dominate.document(title='Overdue Activity')
  with doc:
    p("The following activity is still in draft form and should be completed and approved.  You are being notified because you are listed as calltaker or a responsible party")
    br()
    p("Date:     ", str(dict["activity"].startDate()))
    p("Activity: ", dict["activity"].synopsis())
    p("Update:   ", dict["activity"].viewURL())
    if dict["activity"].type() != "Incident":
      p("Lead:     ", dict["name"])
      br()
      p("Practice leaders, mark yourself as 'Practice Lead', Meeting leaders, mark yourself as 'Lecture Lead'")
      p("Please forward this to the practice or meeting lead if you were not in charge")
    else:
      p("Calltaker:", dict["name"])
      br()
      p("Please forward this to the operations lead if you were not in charge")

  return doc
  
def emailMessage(doc, name, email):
  """
  Email when calltakers are needed
  """
  global context
  msg = EmailMessage()
  msg['Subject'] = "Overdue activity needs approval"
  msg['From'] = Address("Adam Fedor", "adam.fedor", "rockymountainrescue.org")
  #if name:
  #  msg['To'] = name + "<" + email + ">"
  #msg['Bcc'] = ", ".join(summary_email_list)
  msg['Bcc'] = Address("Adam Fedor", "adam.fedor", "rockymountainrescue.org")
  msg.set_content(" - plain content goes here - ")
  msg.add_alternative(str(doc), subtype='html')
  # Send the message via local SMTP server.
  with smtplib.SMTP('localhost') as s:
    s.send_message(msg)

def callMain():
  global context
  parser = argparse.ArgumentParser(description='Overdue Activities', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("-l", "--live", dest='live', action='store_true', help='Run live and send email')
  args = parser.parse_args()
  if 'summary_email_list' not in globals():
    print('Error: summary email list not set')

  apiHelper.requestContext()
  list = overdueActivities()
  for dict in list:
    doc = formatCallTakerHtml(dict)
    if args.live:
      emailMessage(doc, dict["name"], dict["email"])
    else:
      print("-------------- Send email to " + dict["email"] + " --------------------")
      print(doc)

callMain()
