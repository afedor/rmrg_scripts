# RMRG Scripts

This is a repo of scripts used for RMRG scheduling and other applications.  Note the private information
such as passwords and tokens have been redacted from the repos, so you need to get that info separately to actually run
any of the scripts.

## RMRGury scripts

Contains php scripts for responding to RMRGury database requests. These scripts need to be placed in the
web server script dir (Currently /home/www-data/production-area/int/miscdb)

## D4H Scripts

Contains scripts for sending out calltaker reminders gathered from the D4H database. These should be run from
a crontab.

To authorize usage of D4H, you need to get a D4H personal token (The same
kind you get for RMRAccess) and place it in the d4hcommon/config_private.py file

To get access to the Google calendar containing the calltaker schedule, you need to run the calltaker.py script
manually once, which will open a browser window and complete an OAuth verification to get a token.

To get access to a911, you need to get a refresh token (See README in a911 directory) and put it in the
config_private.py file in the a911 directory

### Calltaker

The calltaker script checks the calltaker schedule everyday, and sends out an email on days where there is lack
of coverage for the current or next day.

### Overdue Activities

The overdue activities script sends an email out to the responsible person (calltaker or ops) who has not
finished filling out and approving an incident report after more than a week.

### Equipment Checkout

The equipment checkout script checks the RMRAccess equipment spreadsheet and sends an email if a
truck or other vehicle has been checked out recently.

### Add Attendance

This script grabs the attendance from the A911 page and inserts it into the matching d4H incident

Example crontab:
# Calltaker coverage
4 7 * * * /usr/bin/python3.8 /home/fedor/rmrg_scripts/d4h_scripts/calltaker/calltaker.py --live
# Draft activities
5 18 * * 1 /usr/bin/python3.8 /home/fedor/rmrg_scripts/d4h_scripts/calltaker/overdueActivities.py --live
# Equipment checkout
*/15 * * * * flock -n /home/fedor/equip-lock.txt /usr/bin/python3.8 /home/fedor/rmrg_scripts/d4h_scripts/equipment/equipmentCheckout.py --live > /dev/null 2>&1

