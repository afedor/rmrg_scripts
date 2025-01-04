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

context=0

def formatCallStatus(doc):
  map = context.calltakerStatusMap()
  todaydate = datetime.datetime.now(datetime.timezone.utc)
  availClass = {AvailStatus.NoStatus: 'snone', AvailStatus.Available: 'savail', AvailStatus.Work: 'swork', AvailStatus.Marginal: 'smarg', AvailStatus.Unavailable: 'sunav'}
  with doc:
    h3('Calltakers Availability:')
    with table(border=1).add(tbody()):
      with tr():
        td('        ')
        td(todaydate.strftime('%B'), colspan="20")
      with tr():
        td('    ')
        for i in range(0, 20):
          thedate = todaydate + datetime.timedelta(days=i)
          weekday = thedate.strftime('%a')
          td(weekday[0])
      with tr():
        td('Name')
        for i in range(0, 20):
          thedate = todaydate + datetime.timedelta(days=i)
          td(thedate.day)
      for key, value in map.items():
        with tr():
          td(key)
          for i in range(0, 20):
            stat = value[i]
            td(cls=availClass[stat])
    with table().add(tbody()):
      with tr():
        td(cls='savail', width='40px')
        td('Available')
      with tr():
        td(cls='swork', width='40px')
        td('Marginal (During work hours)')
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
  global temp_email_list
  global context
  emailList = context.calltakerEmailList()
  msg = EmailMessage()
  msg['Subject'] = "D4H Calltaker Daily Summary"
  msg['From'] = Address("Adam Fedor", "adam.fedor", "rockymountainrescue.org")
  msg['To'] = (Address("Adam Fedor", "adam.fedor", "rockymountainrescue.org"))
  #msg['Bcc'] = ", ".join(emailList)
  msg['Bcc'] = ", ".join(temp_email_list)
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
  if args.live:
    emailMessage(doc)
  else:
    print(doc)

callMain()
