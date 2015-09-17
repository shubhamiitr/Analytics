import json,httplib,urllib,time
connection = httplib.HTTPSConnection('api.parse.com', 443)
connection.connect()

current_milli_time = lambda: int(round(time.time() * 1000))
sleep_time = 1

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

def dropParseFile(filename):
  endpoint = '/1/files/' + filename
  connection.request('DELETE', endpoint, '', {
    "X-Parse-Application-Id": "jrumkUT2jzvbFn7czsC5fQmFG5JIYSE4P7GJrlOG",
    "X-Parse-Master-Key": "uh9Vt7UoQUcsUDheZgoOuaBzbPFzUDoxkhSFPEXk"
  })
  response = connection.getresponse().read()
  time.sleep(sleep_time)
  return

def dropParseUser(id):
  print "Deleting ParseUser: " + id + " ..."
  endpoint = '/1/users/' + id
  connection.request('DELETE', endpoint, '', {
    "X-Parse-Application-Id": "jrumkUT2jzvbFn7czsC5fQmFG5JIYSE4P7GJrlOG",
    "X-Parse-REST-API-Key": "nJKpGXJMp6Y6RCzRAR6VtdI1A8BN1IdI4g7KJILU",
    "X-Parse-Master-Key": "uh9Vt7UoQUcsUDheZgoOuaBzbPFzUDoxkhSFPEXk"
  })
  result = json.loads(connection.getresponse().read())
  time.sleep(sleep_time)
  return

def dropParseSession(id):
  print "Deleting ParseSession: " + id + " ..."
  endpoint = '/1/sessions/' + id
  connection.request('DELETE', endpoint, '', {
    "X-Parse-Application-Id": "jrumkUT2jzvbFn7czsC5fQmFG5JIYSE4P7GJrlOG",
    "X-Parse-REST-API-Key": "nJKpGXJMp6Y6RCzRAR6VtdI1A8BN1IdI4g7KJILU",
    "X-Parse-Master-Key": "uh9Vt7UoQUcsUDheZgoOuaBzbPFzUDoxkhSFPEXk"
  })
  result = json.loads(connection.getresponse().read())
  time.sleep(sleep_time)
  return

def dropParseObject(ParseClass, id):
  print "Deleting " + ParseClass + ": " + id + " ..."
  endpoint = '/1/classes/' + ParseClass + '/' + id
  connection.request('DELETE', endpoint, '', {
    "X-Parse-Application-Id": "jrumkUT2jzvbFn7czsC5fQmFG5JIYSE4P7GJrlOG",
    "X-Parse-REST-API-Key": "nJKpGXJMp6Y6RCzRAR6VtdI1A8BN1IdI4g7KJILU"
  })
  result = json.loads(connection.getresponse().read())
  time.sleep(sleep_time)
  return

def clearSessions(start_date, end_date):
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
        "keys": "user",
        "limit": 100,
        "skip": skip,
        "order": "createdAt",
        "include": "user"
      })
    else:
      params = urllib.urlencode({
        "where": json.dumps({
          "createdAt": {
            "$gt": last_date,
            "lte": end_date
          }
        }),
        "keys": "user",
        "limit": 100,
        "skip": skip,
        "order": "createdAt",
        "include": "user"
      })
    skip += 100
    endpoint = '/1/sessions?%s' % params
    connection.request('GET', endpoint, '', {
      "X-Parse-Application-Id": "jrumkUT2jzvbFn7czsC5fQmFG5JIYSE4P7GJrlOG",
      "X-Parse-REST-API-Key": "nJKpGXJMp6Y6RCzRAR6VtdI1A8BN1IdI4g7KJILU",
      "X-Parse-Master-Key": "uh9Vt7UoQUcsUDheZgoOuaBzbPFzUDoxkhSFPEXk"
    })
    sessions = json.loads(connection.getresponse().read())["results"]
    if len(sessions) == 0:
      break
    for session in sessions:
      if session.has_key("user") == False:
        dropParseSession(session["objectId"])
    if skip == 10000:
      skip = 0
      first_run = False
      last_date = sessions[len(sessions)-1]["createdAt"]
  return

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
        "keys":"username",
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
        "keys":"username",
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
      appUsers[user["username"]] = True
    if skip == 10000:
      skip = 0
      first_run = False
      last_date = users[len(users)-1]["createdAt"]
  return

def getCodegroups(start_date, end_date):  
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
        "keys": "senderId,code,senderPic",
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
        "keys": "senderId,code,senderPic",
        "limit": 100,
        "skip": skip,
        "order": "createdAt"
      })
    skip += 100
    endpoint = '/1/classes/Codegroup?%s' % params
    connection.request('GET', endpoint, '', {
      "X-Parse-Application-Id": "jrumkUT2jzvbFn7czsC5fQmFG5JIYSE4P7GJrlOG",
      "X-Parse-REST-API-Key": "nJKpGXJMp6Y6RCzRAR6VtdI1A8BN1IdI4g7KJILU",
    })
    codegroups = json.loads(connection.getresponse().read())["results"]
    if len(codegroups) == 0:
      break
    for codegroup in codegroups:
      if appUsers.has_key(codegroup["senderId"]) == False:
        print codegroup["objectId"]
        # if "senderPic" in codegroup:
        #   dropParseFile(codegroup["senderPic"]["name"])
        # dropParseObject("Codegroup", codegroup["objectId"])
      else:
        Codegroups[codegroup["code"].encode('utf-8', 'ignore')] = True 
    if skip == 10000:
      skip = 0
      first_run = False
      last_date = codegroups[len(codegroups)-1]["createdAt"]
  return  

def clearGroupDetails(start_date, end_date):  
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
        "keys": "senderId,code,attachment",
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
        "keys": "senderId,code,attachment",
        "limit": 100,
        "skip": skip,
        "order": "createdAt"
      })
    skip += 100
    endpoint = '/1/classes/GroupDetails?%s' % params
    connection.request('GET', endpoint, '', {
      "X-Parse-Application-Id": "jrumkUT2jzvbFn7czsC5fQmFG5JIYSE4P7GJrlOG",
      "X-Parse-REST-API-Key": "nJKpGXJMp6Y6RCzRAR6VtdI1A8BN1IdI4g7KJILU",
    })
    groupdetails = json.loads(connection.getresponse().read())["results"]
    if len(groupdetails) == 0:
      break
    for groupdetail in groupdetails:
      if (appUsers.has_key(groupdetail["senderId"]) == False) or (Codegroups.has_key(groupdetail["code"].encode('utf-8', 'ignore')) == False):
        if "attachment" in groupdetail:
          dropParseFile(groupdetail["attachment"]["name"])
        dropParseObject("GroupDetails", groupdetail["objectId"])
    if skip == 10000:
      skip = 0
      first_run = False
      last_date = groupdetails[len(groupdetails)-1]["createdAt"]
  return  

def clearGroupMembers(start_date, end_date):  
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
        "keys": "emailId,code",
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
        "keys": "emailId,code",
        "limit": 100,
        "skip": skip,
        "order": "createdAt"
      })
    skip += 100
    endpoint = '/1/classes/GroupMembers?%s' % params
    connection.request('GET', endpoint, '', {
      "X-Parse-Application-Id": "jrumkUT2jzvbFn7czsC5fQmFG5JIYSE4P7GJrlOG",
      "X-Parse-REST-API-Key": "nJKpGXJMp6Y6RCzRAR6VtdI1A8BN1IdI4g7KJILU",
    })
    groupmembers = json.loads(connection.getresponse().read())["results"]
    if len(groupmembers) == 0:
      break
    for groupmember in groupmembers:
      if (appUsers.has_key(groupmember["emailId"]) == False) or (Codegroups.has_key(groupmember["code"].encode('utf-8', 'ignore')) == False):
        dropParseObject("GroupMembers", groupmember["objectId"])
    if skip == 10000:
      skip = 0
      first_run = False
      last_date = groupmembers[len(groupmembers)-1]["createdAt"]
  return  

def clearMessageneeders(start_date, end_date):  
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
        "keys": "cod",
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
        "keys": "cod",
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
      if Codegroups.has_key(msgnd["cod"].encode('utf-8', 'ignore')) == False:
        dropParseObject("Messageneeders", msgnd["objectId"])
    if skip == 10000:
      skip = 0
      first_run = False
      last_date = msgnds[len(msgnds)-1]["createdAt"]
  return  

start_date = convertUTCDateToParseDate(datetime(2014,1,1,0,0))
end_date = convertUTCDateToParseDate(datetime(2015,9,16,0,0))

# clearSessions(start_date, end_date)

appUsers = {}
fp = open('appUsers.json', 'r')
appUsers = json.loads(fp.read())
fp.close()
# getAppUsers(start_date, end_date)
# fp = open('appUsers.json', 'w')
# fp.write(json.dumps(appUsers))
# fp.close()

Codegroups = {}
fp = open('Codegroups.json', 'r')
Codegroups = json.loads(fp.read())
fp.close()
# getCodegroups(start_date, end_date)
# fp = open('Codegroups.json', 'w')
# fp.write(json.dumps(Codegroups))
# fp.close()

# clearGroupDetails(start_date, end_date)
clearGroupMembers(start_date, end_date)
# clearMessageneeders(start_date, end_date)

