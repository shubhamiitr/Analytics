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

out = open('Invites.csv', 'w')
out.write('{:s}, {:s}'.format('Username', 'Invites'))

out.write('\n')

def getUserInfoById(parseId, invites):
  endpoint = '/1/users/' + parseId;
  connection.request('GET', endpoint, '', {
    "X-Parse-Application-Id": "jrumkUT2jzvbFn7czsC5fQmFG5JIYSE4P7GJrlOG",
    "X-Parse-REST-API-Key": "nJKpGXJMp6Y6RCzRAR6VtdI1A8BN1IdI4g7KJILU",
  })
  user = json.loads(connection.getresponse().read())
  if user.has_key("username"):
    out.write('{:s}, {:s}'.format(user["username"], invites))
    out.write('\n')
  return

fp = open('download.csv', 'r')
userinvites = fp.read().split('\n')
for userinvite in userinvites:
  parseId = userinvite.split(',')[0]
  invites = userinvite.split(',')[1]
  getUserInfoById(parseId, invites)
fp.close()