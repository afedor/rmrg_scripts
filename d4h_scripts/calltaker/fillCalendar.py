#!/usr/bin/env python3
#
# FillCalendar
# Updates the calltaker calendar
#
import os
import sys
import argparse
import datetime
from config_private import *
# Custom
sys.path.insert(1, '..')
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
# Coordinator
from coordinatorCalendar import CoordinatorCalendar

parser = argparse.ArgumentParser(description='Calltaker Calendar', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-n", "--name", dest='name', type=str, help='Calltaker name')
parser.add_argument("-l", "--list", dest='list', type=str, help='List of names')
parser.add_argument("-d", "--date", dest='date', type=str, help='Start Date')
args = parser.parse_args()

lines=[]
if args.list:
  with open(args.list, 'r') as file:
      lines = file.readlines()
elif args.name:
  lines = [args.name]

startTime = datetime.datetime.strptime(args.date, '%Y-%m-%d')

coordinatorCalendar = CoordinatorCalendar()
coordinatorCalendar.setupCalendar(readwrite=True)
for name in lines:
  name = name.rstrip()
  print(f"Insert <{name}>")
  coordinatorCalendar.insertEvent(name, startTime)
  startTime = startTime + datetime.timedelta(days=7)
