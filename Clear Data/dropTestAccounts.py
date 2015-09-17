import json,httplib,urllib,time
connection = httplib.HTTPSConnection('api.parse.com', 443)
connection.connect()

current_milli_time = lambda: int(round(time.time() * 1000))
sleep_time = 1

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

def dropGroupMembers(code):
  params = urllib.urlencode({
    "where": json.dumps({
      "code": code
    }),
    "keys": "code"
  })
  endpoint = '/1/classes/GroupMembers?%s' % params
  while True:
    connection.request('GET', endpoint, '', {
      "X-Parse-Application-Id": "jrumkUT2jzvbFn7czsC5fQmFG5JIYSE4P7GJrlOG",
      "X-Parse-REST-API-Key": "nJKpGXJMp6Y6RCzRAR6VtdI1A8BN1IdI4g7KJILU",
    })
    groupmembers = json.loads(connection.getresponse().read())["results"]
    for groupmember in groupmembers:
      dropParseObject("GroupMembers", groupmember["objectId"])
    if len(groupmembers) == 0:
      break
  return

def dropMessageState(message_id):
  params = urllib.urlencode({
    "where": json.dumps({
      "message_id": message_id
    }),
    "keys": "message_id"
  })
  endpoint = '/1/classes/MessageState?%s' % params
  while True:
    connection.request('GET', endpoint, '', {
      "X-Parse-Application-Id": "jrumkUT2jzvbFn7czsC5fQmFG5JIYSE4P7GJrlOG",
      "X-Parse-REST-API-Key": "nJKpGXJMp6Y6RCzRAR6VtdI1A8BN1IdI4g7KJILU",
    })
    msgstates = json.loads(connection.getresponse().read())["results"]
    for msgstate in msgstates:
      dropParseObject("MessageState", msgstate["objectId"])
    if len(msgstates) == 0:
      break    
  return

def dropSMSReport(groupdetailId):
  params = urllib.urlencode({
    "where": json.dumps({
      "groupdetailId": groupdetailId
    }),
    "keys": "groupdetailId"
  })
  endpoint = '/1/classes/SMSReport?%s' % params
  while True:
    connection.request('GET', endpoint, '', {
      "X-Parse-Application-Id": "jrumkUT2jzvbFn7czsC5fQmFG5JIYSE4P7GJrlOG",
      "X-Parse-REST-API-Key": "nJKpGXJMp6Y6RCzRAR6VtdI1A8BN1IdI4g7KJILU",
    })
    smsreports = json.loads(connection.getresponse().read())["results"]
    for smsreport in smsreports:
      dropParseObject("SMSReport", smsreport["objectId"])
    if len(smsreports) == 0:
      break    
  return  

def dropGroupDetails(code):
  params = urllib.urlencode({
    "where": json.dumps({
      "code": code
    }),
    "keys": "code,attachment"
  })
  endpoint = '/1/classes/GroupDetails?%s' % params
  while True:
    connection.request('GET', endpoint, '', {
      "X-Parse-Application-Id": "jrumkUT2jzvbFn7czsC5fQmFG5JIYSE4P7GJrlOG",
      "X-Parse-REST-API-Key": "nJKpGXJMp6Y6RCzRAR6VtdI1A8BN1IdI4g7KJILU",
    })
    groupdetails = json.loads(connection.getresponse().read())["results"]
    for groupdetail in groupdetails:
      dropMessageState(groupdetail["objectId"])
      dropSMSReport(groupdetail["objectId"])
      if "attachment" in groupdetail:
        dropParseFile(groupdetail["attachment"]["name"])
      dropParseObject("GroupDetails", groupdetail["objectId"])
    if len(groupdetails) == 0:
      break    
  return

def dropMessageneeders(cod):
  params = urllib.urlencode({
    "where": json.dumps({
      "cod": cod
    }),
    "keys": "cod"
  })
  endpoint = '/1/classes/Messageneeders?%s' % params
  while True:
    connection.request('GET', endpoint, '', {
      "X-Parse-Application-Id": "jrumkUT2jzvbFn7czsC5fQmFG5JIYSE4P7GJrlOG",
      "X-Parse-REST-API-Key": "nJKpGXJMp6Y6RCzRAR6VtdI1A8BN1IdI4g7KJILU",
    })
    msgnds = json.loads(connection.getresponse().read())["results"]
    for msgnd in msgnds:
      dropParseObject("Messageneeders", msgnd["objectId"])  
    if len(msgnds) == 0:
      break
  return 

def dropCodegroups(senderId):
  params = urllib.urlencode({
    "where": json.dumps({
      "senderId": senderId
    }),
    "keys": "senderId,code,senderPic"
  })
  endpoint = '/1/classes/Codegroup?%s' % params
  while True:
    connection.request('GET', endpoint, '', {
      "X-Parse-Application-Id": "jrumkUT2jzvbFn7czsC5fQmFG5JIYSE4P7GJrlOG",
      "X-Parse-REST-API-Key": "nJKpGXJMp6Y6RCzRAR6VtdI1A8BN1IdI4g7KJILU",
    })
    codegroups = json.loads(connection.getresponse().read())["results"]
    for codegroup in codegroups:
      print "    < CLASSCODE: " + codegroup["code"] + " >"
      dropGroupMembers(codegroup["code"])
      dropGroupDetails(codegroup["code"])
      dropMessageneeders(codegroup["code"])
      if "senderPic" in codegroup:
        dropParseFile(codegroup["senderPic"]["name"])
      dropParseObject("Codegroup", codegroup["objectId"])
    if len(codegroups) == 0:
      break  
  return  

def dropTestAccounts():
  params = urllib.urlencode({
    "where": json.dumps({
      "username": {
        "$lte": "0000999999"
      }
    }),
    "keys":"username,pid"
  })
  endpoint = '/1/users?%s' % params
  while True:
    connection.request('GET', endpoint, '', {
      "X-Parse-Application-Id": "jrumkUT2jzvbFn7czsC5fQmFG5JIYSE4P7GJrlOG",
      "X-Parse-REST-API-Key": "nJKpGXJMp6Y6RCzRAR6VtdI1A8BN1IdI4g7KJILU",
    })
    users = json.loads(connection.getresponse().read())["results"]
    for user in users:
      dropCodegroups(user["username"])
      if "pid" in user:
        dropParseFile(user["pid"]["name"])
      dropParseUser(user["objectId"])
    if len(users) == 0:
      break
  return

def dropAccounts(usernames):
  for username in usernames:
    params = urllib.urlencode({
      "where": json.dumps({
        "username": username
      }),
      "keys":"username,pid"
    })
    endpoint = '/1/users?%s' % params
    connection.request('GET', endpoint, '', {
      "X-Parse-Application-Id": "jrumkUT2jzvbFn7czsC5fQmFG5JIYSE4P7GJrlOG",
      "X-Parse-REST-API-Key": "nJKpGXJMp6Y6RCzRAR6VtdI1A8BN1IdI4g7KJILU",
    })
    users = json.loads(connection.getresponse().read())["results"]
    for user in users:
      print "\n     < USER: " + user["username"] + " >" 
      dropCodegroups(user["username"])
      if "pid" in user:
        dropParseFile(user["pid"]["name"])
      dropParseUser(user["objectId"])
  return

dropAccounts([])