import json,httplib,urllib

connection = httplib.HTTPSConnection('api.parse.com', 443)
connection.connect()

from datetime import datetime, timedelta

def convertUTCDateToParseDate(utcdate):
  date = {
    "__type": "Date", 
    "iso": utcdate.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
  }
  return date

def convertParseDateToUTCDate(date):
  utcdate = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
  return utcdate

def convertParseDateToDisplayDate(date):
  utcdate = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
  return utcdate.strftime("%Y/%m/%d")

out = open('Knit Users.csv', 'w')
out.write('{:s}, {:s}, {:s}, {:s}'.format('Username', 'Role', 'Login', 'Created Date'))
out.write('\n')

def getLoginType(username):
  if username.isdigit() == False:
    return "Email"
  else:
    length = len(username)
    if length == 10:
      return "Mobile"
    elif length == 12:
      return "SMS"
    elif length == 21:
      return "Google"
    else:
      return "Facebook"

def getAppUsers(start_date, end_date):
  first_run = True
  skip = 0
  while True:
    if first_run:
      params = urllib.urlencode({
        "where": json.dumps({
          "createdAt": {
            "$gt": start_date,
            "$lte": end_date
          }
        }),
        "keys": "username,role",
        "limit": 100,
        "skip": skip,
        "order": "createdAt"
      })
    else:
      params = urllib.urlencode({
        "where": json.dumps({
          "createdAt": {
            "$gt": last_date,
            "$lte": end_date
          }
        }),
        "keys": "username,role",
        "limit": 100,
        "skip": skip,
        "order": "createdAt"
      })
    skip += 100
    endpoint = '/1/users?%s' % params
    connection.request('GET', endpoint, '', {
      "X-Parse-Application-Id": "jrumkUT2jzvbFn7czsC5fQmFG5JIYSE4P7GJrlOG",
      "X-Parse-REST-API-Key": "nJKpGXJMp6Y6RCzRAR6VtdI1A8BN1IdI4g7KJILU",
    })
    users = json.loads(connection.getresponse().read())["results"]
    if len(users) == 0:
      break
    for user in users:
      login = getLoginType(user["username"])
      out.write('{:s}, {:s}, {:s}, {:s}'.format(user["username"], user["role"], login, convertParseDateToDisplayDate(user["createdAt"])))
      out.write('\n')
    if skip == 10000:
      skip = 0
      first_run = False
      last_date = users[len(users)-1]["createdAt"]
  return

def getSMSUsers(start_date, end_date):
  skip = 0
  first_run = True
  while True:
    if first_run:
      params = urllib.urlencode({
        "where": json.dumps({
          "createdAt": {
            "$gt": start_date,
            "$lte": end_date
          }
        }),
        "keys": "number",
        "limit": 100,
        "skip": skip,
        "order": "createdAt"
      })
    else:
      params = urllib.urlencode({
        "where": json.dumps({
          "createdAt": {
            "$gt": last_date,
            "$lte": end_date
          }
        }),
        "keys": "number",
        "limit": 100,
        "skip": skip,
        "order": "createdAt"
      })
    skip += 100
    endpoint = '/1/classes/Messageneeders?%s' % params
    connection.request('GET', endpoint, '', {
      "X-Parse-Application-Id": "jrumkUT2jzvbFn7czsC5fQmFG5JIYSE4P7GJrlOG",
      "X-Parse-REST-API-Key": "nJKpGXJMp6Y6RCzRAR6VtdI1A8BN1IdI4g7KJILU",
    })
    msgnds = json.loads(connection.getresponse().read())["results"]
    if len(msgnds) == 0:
      break
    for msgnd in msgnds:
      if smsUsers.has_key(msgnd["number"]) == False:
        smsUsers[msgnd["number"]] = msgnd["createdAt"]
        out.write('{:s}, {:s}, {:s}, {:s}'.format(msgnd["number"], "parent", "SMS", convertParseDateToDisplayDate(msgnd["createdAt"])))
        out.write('\n')
    if skip == 10000:
      skip = 0
      first_run = False
      last_date = msgnds[len(msgnds)-1]["createdAt"]
  return      

start_date = datetime(2015,9,7,0,0)
end_date = datetime(2015,9,14,0,0)

getAppUsers(convertUTCDateToParseDate(start_date), convertUTCDateToParseDate(end_date))

smsUsers = {}
fp = open('smsUsers.json', 'r')
smsUsers = json.loads(fp.read())
fp.close()
getSMSUsers(convertUTCDateToParseDate(start_date), convertUTCDateToParseDate(end_date))
fp = open('smsUsers.json', 'w')
fp.write(json.dumps(smsUsers))
fp.close()