import requests
from datetime import date, timedelta
import time
from twilio.rest import Client

def dateGenerator():
    today = date.today()
    today.strftime("%d-%m-%Y")
    day = 0
    dateList = []
    while day <= 7:
        nextDay = today + timedelta(days=day)
        dateList.append(nextDay.strftime("%d-%m-%Y"))
        day = day + 1
    return dateList


def runApi(centerId):
    dateList = dateGenerator()
    for apiDate in dateList:
        API = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=" + str(centerId) + "&date=" + apiDate
        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
        req = requests.get(API, headers=headers)
        obj = req.json()
        for centers in obj:
            for v in obj[centers]:
                if v["fee_type"] == "Free":
                    for session in v["sessions"]:
                        if session["available_capacity"] > 0 and session["min_age_limit"] == 18:
                            return True, v["name"], session["date"]

    return False, "Not yet", "Not yet"


def vaccineSlotDetector(account_sid,auth_token,centerId):
    MessageCounter = 5
    alertSentDate = date.today()
    while True:

        while True:
            flag, centerName, availableDate = runApi(centerId)
            if flag and MessageCounter > 0:


                #Need/can to implement a helper method for sending message.....
                client = Client(account_sid, auth_token)
                messageBody = "Hey it's your buddy Supriyo, Vaccine is available please check at" + availableDate + centerName
                message = client.messages.create(body=messageBody, from_='Put your twilio phone no.', to='put your twilio authorised phone no.')
                MessageCounter = MessageCounter - 1
                alertSentDate = date.today()

                if MessageCounter <= 0:
                    break

            time.sleep(300)

       #MessageReseter can be buggy need to think better alternative
        if MessageCounter == 0:
            while True:
                resetDay = alertSentDate + timedelta(days=1)
                if date.today() == resetDay:
                    MessageCounter = 5
                    break


if __name__ == '__main__':

    centerId = ""  # Put your center Id here
    account_sid = " " #put your twilio account_sid
    auth_token = " " #put your twilio auth_token

    try:
        vaccineSlotDetector(account_sid,auth_token,centerId)

    except:
        client = Client(account_sid, auth_token)
        messageBody = "Hey it's your buddy Supriyo, unfortunately your code is bombed please check"
        message = client.messages.create(body=messageBody, from_='Put your twilio phone no.', to='put your twilio authorised phone no.')

