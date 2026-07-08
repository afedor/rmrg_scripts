#!/usr/bin/env python3
#
# Add Attendance
# Add responses from A911 page to the D4H incident
#
import sys
import argparse
import attendanceHelper

parser = argparse.ArgumentParser(description='Add Attendance', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-p", "--page", dest='page', type=int, help='Incident identifier of the page')
args = parser.parse_args()
if not args.page:
  print("Usage: addAttendance -p page")
  sys.exit(1)

result = attendanceHelper.runAddAttendance(args.page)
print(f"Result: {result}")