import requests
from datetime import datetime
import smtplib
import time
import os
from dotenv import load_dotenv

load_dotenv()

MY_LAT = 46.204391
MY_LONG = 6.143158

MY_MAIL = os.environ.get('MAIL')
MY_PASS = os.environ.get('PASS')
MAIL_TO = os.environ['MAILTO']


def is_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= MY_LONG <= MY_LONG + 5:
        return True


def is_dark():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get(
        "https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()
    if time_now.hour >= sunset or time_now.hour <= sunrise:
        return True


def send_mail():
    if is_overhead() and is_dark():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(MY_MAIL, MY_PASS)
            connection.sendmail(MY_MAIL, MAIL_TO,
                                msg="Subject: Look Up \n\n Look up ISS is near!")


# If you want to run the code every 60 seconds, uncomment this section instead.
# while True:
#     send_mail()
#     time.sleep(60)

send_mail()
