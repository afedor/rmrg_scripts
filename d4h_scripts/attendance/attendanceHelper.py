#!/usr/bin/env python3
#
# Add Attendance
# Add responses from A911 page to the D4H incident
#
# Custom
import sys
sys.path.insert(1, '..')
import d4hcommon
from d4hcommon import apiHelper
from a911 import a911Context, deviceModel, alertModel

def runAddAttendance(pageId: int) -> str:
    # D4H Startup
    apiHelper.requestContext()
    activityContext = d4hcommon.ActivityContext()
    activityContext.initContext()
    memberContext = d4hcommon.MemberContext()
    memberContext.requestMembers()

    # Get the activity from D4H
    activity = activityContext.requestActivity('incidents', pageId)
    if not activity:
        return "Could not find incident"

    print(f'  got activity cad={activity.cadCode()}')
    if activity.published():
        return "Incident already published!"
    attendanceContext = d4hcommon.AttendanceContext(activity.identity())

    # A911 Startup
    a911 = a911Context.A911Context()
    a911.initContext()
    a911.requestPages()
    print("  got a911 pages")

    page = a911.pageWithCadCode(activity.cadCode())
    if not page:
        return "Could not find a911 page"

    print("  got a11 page with cad code")
    map = {"endsAt": activity.endDateStr(), 
        "startsAt": activity.startDateStr(),
        "status": "ATTENDING"}
    responses = a911.allRespondingDevices(page)
    allAttending = attendanceContext.attendanceList()
    print("Responding:")
    for response in responses:
        print(f"  {response.memberName()}  resp: {response.response()}")
        member = memberContext.memberContainsLastShortName(response.memberName())
        if "Cancel" in response.response():
            print("    Skipping - cancelled")
            continue
        if not member:
            print("    Could not match with D4H member")
            continue

        attendance = attendanceContext.memberAttendance(member.identifier())
        if attendance:
            try:
                allAttending.remove(attendance)
            except Exception as e:
                print(f"  Could not remove {attendance.memberId()}: {e}")
            if attendance.status() == "ATTENDING":
                print("    Attendance already contains member")
                continue
            print("    Updating attendance for member")
            attendanceContext.updateAttending(attendance.identifier(), map)
        else:
            print("    Adding member")
            attend = map
            attend["memberId"] = member.identifier()
            attend["activityId"] = activity.identity()
            attendanceContext.putAttending(attend)

    for attendance in allAttending:
        print(f"  Remove attendance {attendance.memberId()} status {attendance.status()}")
        attendanceContext.deleteAttending(attendance.identifier())
    return ""