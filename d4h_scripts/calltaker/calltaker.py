#!/usr/bin/env python3
#
# CalltakerReminder
# Downloads current calltaker calendar from D4H and mails out a summary to the calltakers
# See: https://github.com/Knio/dominate
#
import argparse
import datetime
import requests
import calendar
# HTML
import dominate
from dominate.tags import *
# Custom
import apiHelper
import commonDates
from ordinalCallSignup import OrdinalCallSignup
from dutyModel import DutyModel
from calltakerContext import CalltakerContext
from calltakerCalendar import CalltakerCalendar
from memberContext import MemberContext
# Email
import smtplib
from email.message import EmailMessage
from email.headerregistry import Address

def calltakerEmailList() -> list:
  memberContext = MemberContext()
  memberContext.initContext()
  gid = memberContext.groupIdentWithName("Calltaker")
  memberList = memberContext.membersInGroup(gid)
  return memberContext.memberGroupEmails(memberList)

def formatCallTakerHtml():
  """
  Format calltaker info into html
  """
  context = CalltakerContext()
  context.getCalltakerDuties()
  callCalendar = CalltakerCalendar(context, calendar.MONDAY)
  tomorrow = datetime.datetime.today() + datetime.timedelta(1)
  fstyle = open("calendar.css", "r")
  lstyle = fstyle.readlines()
  tomorrowSignups = context.getSignupsForDay(tomorrow)

  doc = dominate.document(title='Calltaker Daily')
  with doc.head:
    style(''.join(lstyle))
  with doc:
    h3('TEST TEST TEST')
    p('Note this is a test of D4H scheduling for calltakers. This is not live yet.')
    h3('Calltakers for tomorrow:')
    with div().add(ul()):
      for signup in tomorrowSignups:
        startStr = str(signup.startDate().strftime('%H%M'))
        endStr = str(signup.endDate().strftime('%H%M'))
        if endStr == '0000':
          endStr = '2400'
        li(' '+ signup.dutyModel.memberName()+ ': '+ startStr+ ' -> '+ endStr)

    if context.isDayComplete(tomorrow) == False:
      p("Still need signup for tomorrow!")
      
    today = datetime.datetime.today()
    with div():
      h3("Upcoming Calltakers:")
      dominate.util.raw(callCalendar.formatmonth(today.year, today.month))

    if today.day > 12:
      nextMonth = datetime.datetime.today() + datetime.timedelta(21)
      callCalendar.setCurrentMonthDate(nextMonth)
      dominate.util.raw(callCalendar.formatmonth(nextMonth.year, nextMonth.month))
  return doc
  
def emailMessage(doc):
  emailList = calltakerEmailList()
  msg = EmailMessage()
  msg['Subject'] = "Calltaker Daily Summary"
  msg['From'] = Address("Adam Fedor", "adam.fedor", "rockymountainrescue.org")
  msg['To'] = (Address("Adam Fedor", "adam.fedor", "rockymountainrescue.org"))
  #msg['Bcc'] = ", ".join(emailList)
  msg.set_content(" - plain content goes here - ")
  msg.add_alternative(str(doc), subtype='html')
  # Send the message via local SMTP server.
  with smtplib.SMTP('localhost') as s:
    s.send_message(msg)

def callMain():
  parser = argparse.ArgumentParser(description='Calltaker Daily', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("-l", "--live", dest='live', action='store_true', help='Run live and send email')
  args = parser.parse_args()

  apiHelper.requestContext()
  doc = formatCallTakerHtml()
  if args.live:
    emailMessage(doc)
  else:
    print(doc)

callMain()
