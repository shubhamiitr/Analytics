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

out = open('Users Info.csv', 'w')
out.write('{:s}, {:s}, {:s}, {:s}'.format('Username', 'Name', 'Email', 'Mobile'))
out.write('\n')

def getUserInfoByName(username):
  params = urllib.urlencode({
    "where": json.dumps({
      "username": username
    }),
    "keys": "username,name,email,phone",
    "limit": 1    
  })
  endpoint = '/1/users?%s' % params
  connection.request('GET', endpoint, '', {
    "X-Parse-Application-Id": "jrumkUT2jzvbFn7czsC5fQmFG5JIYSE4P7GJrlOG",
    "X-Parse-REST-API-Key": "nJKpGXJMp6Y6RCzRAR6VtdI1A8BN1IdI4g7KJILU",
  })
  users = json.loads(connection.getresponse().read())["results"]
  if len(users) == 0:
    out.write('{:s}'.format(username))
  else:  
    user = users[0]
    out.write('{:s}, {:s}, {:s}, {:s}'.format(user["username"], user["name"].encode('utf-8', 'ignore'), user["email"] if user.has_key("email") else "", user["phone"] if user.has_key("phone") else ""))
  out.write('\n')
  return

fp = open('usernames.txt', 'r')
usernames = fp.read().split('\n')
for username in usernames:
  getUserInfoByName(username)
fp.close()