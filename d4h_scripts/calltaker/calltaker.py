#!/usr/bin/env python3
#
# CalltakerReminder
# Downloads current calltaker calendar from D4H and mails out a summary to the calltakers
# See: https://github.com/Knio/dominate
#
import sys
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
from dutyModel import AvailStatus
from calltakerContext import CalltakerContext
from calltakerCalendar import CalltakerCalendar
from config import *
# Email
import smtplib
from email.message import EmailMessage
from email.headerregistry import Address
# Coordinator
from coordinatorCalendar import CoordinatorCalendar

context=0

def formatCallStatus(doc):
  maxdays = 20
  map = context.calltakerStatusMap()
  todaydate = datetime.datetime.now(datetime.timezone.utc)
  nextmonth = commonDates.firstDayOfNextMonth(todaydate)
  colspan = commonDates.differenceInDays(todaydate, nextmonth)
  if colspan > maxdays:
    colspan = maxdays
  availClass = {AvailStatus.NoStatus: 'snone', AvailStatus.Available: 'savail', AvailStatus.Work: 'swork', AvailStatus.Marginal: 'smarg', AvailStatus.Unavailable: 'sunav'}
  with doc:
    h3('Calltakers Availability:')
    with table(border=1).add(tbody()):
      with tr():
        td('        ')
        td(todaydate.strftime('%b'), colspan=str(colspan))
        if colspan < maxdays:
          td(nextmonth.strftime('%b'), colspan=str(maxdays-colspan))
      with tr():
        td('    ')
        for i in range(0, maxdays):
          thedate = todaydate + datetime.timedelta(days=i)
          weekday = thedate.strftime('%a')
          td(weekday[0])
      with tr():
        td('Name')
        for i in range(0, maxdays):
          thedate = todaydate + datetime.timedelta(days=i)
          td(thedate.day)
      for key, value in map.items():
        with tr():
          td(key)
          for i in range(0, maxdays):
            stat = value[i]
            td(cls=availClass[stat])
    with table().add(tbody()):
      with tr():
        td(cls='savail', width='40px')
        td('Available')
      with tr():
        td(cls='swork', width='40px')
        td('Marginal (From 9am-5pm)')
      with tr():
        td(cls='smarg', width='40px')
        td('Marginal (All day)')
      with tr():
        td(cls='sunav', width='40px')
        td('Unavailable')
    br()

def formatCallTakerHtml():
  """
  Format calltaker info into html
  """
  global context
  context.getCalltakerDuties()
  callCalendar = CalltakerCalendar(context, calendar.MONDAY)
  tomorrow = datetime.datetime.today() + datetime.timedelta(1)
  fstyle = open(sys.path[0] + "/calendar.css", "r")
  lstyle = fstyle.readlines()
  tomorrowSignups = context.getSignupsForDay(tomorrow)
  coordinatorCalendar = CoordinatorCalendar()
  coordinator = coordinatorCalendar.getCoordinatorForDate(tomorrow)

  doc = dominate.document(title='Calltaker Coverage')
  with doc.head:
    style(''.join(lstyle))
  with doc:
    if context.isDayComplete(tomorrow) == False:
      total = context.dayCoverageHours(tomorrow)
      p("Still need calltaker signup for tomorrow! ", (48-total)/2, " hours not covered")

    h3('Calltakers for tomorrow: (Coordinator is ', coordinator, ')')
    with div().add(ul()):
      for signup in tomorrowSignups:
        startStr = str(signup.startDate().strftime('%H%M'))
        endStr = str(signup.endDate().strftime('%H%M'))
        if endStr == '0000':
          endStr = '2400'
        li(' '+ signup.dutyModel.memberName()+ ': '+ startStr+ ' -> '+ endStr)

    today = datetime.datetime.today()
    with div():
      h3("Upcoming Calltakers:")
      dominate.util.raw(callCalendar.formatmonth(today.year, today.month))

    if today.day > 12:
      nextMonth = datetime.datetime.today() + datetime.timedelta(21)
      callCalendar.setCurrentMonthDate(nextMonth)
      dominate.util.raw(callCalendar.formatmonth(nextMonth.year, nextMonth.month))
    with table().add(tbody()):
      with tr():
        td(cls='daypart', width='40px')
        td('Not covered (Any day)')
      with tr():
        td(cls='daycomp', width='40px')
        td('Covered (Any day)')
      with tr():
        td(cls='todpart', width='40px')
        td('Not Covered for today')
      with tr():
        td(cls='todcomp', width='40px')
        td('Covered for today')
    br()

  return doc
  
def emailMessage(doc):
  """
  Email when calltakers are needed
  """
  global context
  emailList = context.calltakerEmailList()
  msg = EmailMessage()
  msg['Subject'] = "Calltaker Coverage Needed"
  msg['From'] = Address("Adam Fedor", "adam.fedor", "rockymountainrescue.org")
  msg['To'] = Address("Calltakers", "calltakernotify", "rockymountainrescue.org")
  msg.set_content(" - plain content goes here - ")
  msg.add_alternative(str(doc), subtype='html')
  # Send the message via local SMTP server.
  with smtplib.SMTP('localhost') as s:
    s.send_message(msg)

def emailSummaryMessage(doc):
  """
  Email daily summary, but only to people who want it
  """
  global context
  emailList = context.calltakerEmailList()
  msg = EmailMessage()
  msg['Subject'] = "Calltaker Coverage Summary"
  msg['From'] = Address("Adam Fedor", "adam.fedor", "rockymountainrescue.org")
  msg['Bcc'] = ", ".join(summary_email_list)
  msg.set_content(" - plain content goes here - ")
  msg.add_alternative(str(doc), subtype='html')
  # Send the message via local SMTP server.
  with smtplib.SMTP('localhost') as s:
    s.send_message(msg)

def callMain():
  global context
  parser = argparse.ArgumentParser(description='Calltaker Daily', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("-l", "--live", dest='live', action='store_true', help='Run live and send email')
  args = parser.parse_args()

  apiHelper.requestContext()
  context = CalltakerContext() 
  context.getDuties()
  doc = formatCallTakerHtml()
  formatCallStatus(doc)
  if 'summary_email_list' not in globals():
    print('Error: summary email list not set')
  tomorrow = datetime.datetime.today() + datetime.timedelta(1)
  if args.live:
    if context.isDayComplete(tomorrow) == False:
      emailMessage(doc)
    else:
      emailSummaryMessage(doc)
  else:
    print(doc)

callMain()
