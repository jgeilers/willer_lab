import requests
import json
import os
import sys

def updateSession(sessionId, surveyId, payload, apiToken, dataCenter):
    url = "https://" + dataCenter + ".qualtrics.com/jfe/form/" + surveyId

    headers = {'X-API-TOKEN': apiToken,
          'content-type': 'application/json',
          'Accept': 'text/plain'}


    response = requests.post(url, headers=headers, data=payload)
    print ("update response=", response.text)

def getSession(surveyId, apiToken, dataCenter):

    headers = {
        "Content-Type": "application/json",
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-API-TOKEN': apiToken
        }

    url = "https://env.qualtrics.com/API/v3/users"
    
    response = requests.get(url, headers=headers)
    print(response)
    print(response.text)
    res = response.json()
    print(res)

    sessionId = res['result']['sessionId']
    return sessionId


def main():

    try:
        surveyId = sys.argv[1]
    except IndexError:
        print ("usage: %s -i <surveyID> %s", sys.argv[0])
        sys.exit(2) 

    try:
        apiToken = ''
        dataCenter = 'stanforduniversity'
    except KeyError:
        print("set environment variables APIKEY and DATACENTER")
        sys.exit(2) 

    sessionId = getSession(surveyId, apiToken, dataCenter)
    print(sessionId)

    headers = {'X-API-TOKEN': apiToken,
    "content-type": "application/json"}

    url = "https://" + dataCenter + ".qualtrics.com/API/v3/surveys/" + surveyId

    response = requests.get(url, headers=headers)

    d = json.JSONDecoder()
    res = d.decode(response.text)

    r = res['result']

    questions = r['questions']

    for k, v in questions.items():
        print (k)
        print (v['questionText'])
        c = v['choices']
        for x, y in c.items():
            print (y['choiceText'])
            print (x)
        answer = input("enter your answer=")  
        payload = '{ \
        "advance": true \
        } \
        "responses": { \
        "%s": { \
            "%s": { \
                "selected": true \
                } \
            } \
        }' % (k, answer) 
        updateSession(sessionId, surveyId, payload, apiToken, dataCenter) 

if __name__ == "__main__":
    main()