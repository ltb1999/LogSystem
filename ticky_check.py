#!/usr/bin/env python3
import re
import operator
import csv

# Dictionary for ERROR:
error = {"Timeout while retrieving information": 0,
        "The ticket was modified while updating":0,
        "Connection to DB failed":0,
        "Tried to add information to closed ticket":0,
        "Permission denied while closing ticket":0,
        "Ticket doesn't exist":0}

# Dictionary for USER:
per_user = {}
with open("user_emails.csv") as f:
  for line in f:
   search = re.search(r"([\w.]*)@", line) # Parse the first part of the email
   if search:
    user_name = search.group(1) # Remove the @
    print(user_name)
    per_user.update({user_name:[0,0]}) # value of error and info of each user start at 0

# Parse Error File, which is created by "grep ERROR syslog.log >> error.txt" in the terminal
with open("error.txt") as f:
 for line in f:
  user_name = re.search(r"\(([\w.]*)",line)
  error_message = re.search(r"ERROR ([\w\s']*)", line)
  if error_message:
    error_m = error_message.group(1)[:-1]
    error[error_m] = error[error_m]+1
  if user_name:
    user_name = user_name.group(1)
    per_user[user_name][1] = per_user[user_name][1]+1

# Parse Info file, which is created by "grep INFO syslog.log >> info.txt" in the terminal
with open("info.txt") as f:
 for line in f:
  user_name = re.search(r"\(([\w.]*)",line)
  if user_name:
   user_name = user_name.group(1)
   per_user[user_name][0] = per_user[user_name][0]+1

# Rearrange error message in order
error = sorted(error.items(), key = operator.itemgetter(1), reverse = True)

# Print the error_message.csv file with the ordered list
csv_file = "error_message.csv"
try:
    with open(csv_file, 'w') as csvfile:
        csvfile.writelines("Error,Count\n")
        for name,count in error:
            csvfile.writelines(name+','+str(count)+'\n')
except IOError:
    print("I/O error")

# Rearrange per_user dict to an ordered list
per_user = sorted(per_user.items(), key = operator.itemgetter(0))

# Print the user_statistics.csv file with the ordered list
csv_file = "user_statistics.csv"
try:
    with open(csv_file, 'w') as csvfile:
        csvfile.writelines("Username,INFO,ERROR\n")
        for name,list in per_user:
            csvfile.writelines(name+','+str(list[0])+','+str(list[1])+'\n')
except IOError:
    print("I/O error")
