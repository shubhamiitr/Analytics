import json,httplib,urllib,time

connection = httplib.HTTPSConnection('api.parse.com', 443)
connection.connect()

from datetime import datetime, timedelta

def convertUTCDateToParseDate(utcdate):
  date = {
    "__type": "Date", 
    "iso": utcdate.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
  }
  return date

def convertParseDateToDisplayDate(date):
  utcdate = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
  return utcdate.strftime("%Y/%m/%d")

out = open('App Subscibers First Class Info.csv', 'w')
out.write('{:s}, {:s}'.format('Subscriber Id', 'Class code'))
out.write('\n')

def getAppSubscribersFirstClassInfo(start_date, end_date):
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
        "keys": "code,emailId",
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
        "keys": "code,emailId",
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
      if appSubscribers.has_key(groupmember["emailId"]) == False:
        appSubscribers[groupmember["emailId"]] = groupmember["code"]    
        out.write('{:s}, {:s}\n'.format(groupmember["emailId"], groupmember["code"]))
    if skip == 10000:
      skip = 0
      first_run = False
      last_date = groupmembers[len(groupmembers)-1]["createdAt"]  
  return

start_date = datetime(2014,1,1,0,0)
end_date = datetime(2015,9,14,0,0)

appSubscribers = {}
# fp = open('appSubscribers.json', 'r')
# appSubscribers = json.loads(fp.read())
# fp.close()
getAppSubscribersFirstClassInfo(convertUTCDateToParseDate(start_date), convertUTCDateToParseDate(end_date))
fp = open('appSubscribers.json', 'w')
fp.write(json.dumps(appSubscribers))
fp.close()