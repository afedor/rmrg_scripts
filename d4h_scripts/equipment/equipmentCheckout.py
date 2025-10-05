#!/usr/bin/env python3
#
# Equipment Checkout checker
# Checks if any equipment has been checked out recently and sends an email about it
#
import sys
import os
import argparse
import datetime
import requests
import calendar
# Custom
sys.path.insert(1, '..')
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
import d4hcommon
from d4hcommon import commonDates
from d4hcommon import apiHelper
from equipmentContext import EquipmentContext
# HTML
import dominate
from dominate.tags import *
# Email
import smtplib
from email.message import EmailMessage
from email.headerregistry import Address

context=0
checkpath = sys.path[0] + "/_equipment_check.txt"

def saveLastCheckDate():
  today = datetime.datetime.today()
  with open(checkpath, "w") as note:
    note.write(str(today))

def lastCheckDate() -> datetime:
  checkDate = 0
  zone = datetime.datetime.now().astimezone().tzinfo
  if os.path.isfile(checkpath):
    with open(checkpath, "r") as note:
      lines = note.readlines()
      if lines:
        date = datetime.datetime.strptime(lines[0], '%Y-%m-%d %H:%M:%S.%f').replace(tzinfo=zone)
        return date
  # If no date, go back just a few days so we don't accidentally send all previous checkouts
  today = datetime.datetime.today()
  past = today + datetime.timedelta(-4)
  past = past.replace(tzinfo=zone)
  return past

def latestCheckoutList(context) -> list:
  today = datetime.datetime.today()
  equipment = context.truckAndOhvEquipment()
  lastCheck = lastCheckDate()
  print("  Last check was at " + str(lastCheck))
  latestCheckouts = []
  for item in equipment:
    print("  Checking " + item["name"])
    checkouts = context.equipmentCheckouts(item)
    for checkout in checkouts:
      if lastCheck == None or checkout.startDate() > lastCheck:
        print("    got checkout ---" + str(checkout.startDate()) + " " + checkout.notes())
        latestCheckouts.append({'equipment': item, 'checkout': checkout})
  return latestCheckouts

def formatCheckoutHtml(checkouts, memberContext):
  """
  Format checkout info into html
  """
  today = datetime.datetime.today()

  doc = dominate.document(title='Fleet Checkout')
  with doc:
    h3("The following updates were made to the Fleet checkout")
    with div().add(ul()):
      for checkout in checkouts:
        equipment = checkout['equipment']
        duty = checkout['checkout']
        memberId = duty.memberIdFromEquipmentNote()
        comment = duty.commentFromEquipmentNote()
        endsAt = duty.endDate() + datetime.timedelta(-1)
        endStr = endsAt.strftime('%m/%d %H:%M')
        member = memberContext.memberWithIdent(memberId)
        name = ''
        if member:
          name = member['name']
        li('' + equipment['name'] + ' checkout by '+ name+ ' until ' + endStr + " note: " + comment)

    br()
  return doc
  
def emailMessage(doc):
  """
  Email when calltakers are needed
  """
  msg = EmailMessage()
  msg['Subject'] = "Fleet Checkout Update"
  msg['From'] = Address("Adam Fedor", "adam.fedor", "rockymountainrescue.org")
  msg['To'] = Address("Truck Drivers", "fleet", "rockymountainrescue.org")
  msg.set_content(" - plain content goes here - ")
  msg.add_alternative(str(doc), subtype='html')
  # Send the message via local SMTP server.
  with smtplib.SMTP('localhost') as s:
    s.send_message(msg)

def callMain():
  parser = argparse.ArgumentParser(description='Equipment Checkout', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("-l", "--live", dest='live', action='store_true', help='Run live and send email')
  args = parser.parse_args()

  print("Running Equipment Checkout Check")
  apiHelper.requestContext()
  context = EquipmentContext() 
  latestCheckouts = latestCheckoutList(context)
  saveLastCheckDate()

  if latestCheckouts:
    doc = formatCheckoutHtml(latestCheckouts, context.memberContext)
    if args.live:
      emailMessage(doc)
    else:
      print(doc)

callMain()
