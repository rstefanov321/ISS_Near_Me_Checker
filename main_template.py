import time
import requests
from datetime import datetime
import smtplib

MY_LAT = float()
MY_LNG = float()
MY_EMAIL = "test_sender@gmail.com"
MY_PASS = "password"
TO_EMAIL = "test_recipient@gmail.com"


def is_dark():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LNG,
        "formatted": 0,
    }

    # Get sunrise and sunset times
    # response = requests.get(f"https://api.sunrise-sunset.org/json?lat={parameters['lat']}&lng={parameters['lng']}")
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()

    # split and extract the hour as an integer
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()
    hour_now = time_now.hour
    print(f"Current hour is {hour_now}")

    if hour_now < sunrise or hour_now > sunset:
        return True
    else:
        return False


def send_email():
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs=TO_EMAIL,
                            msg="Subject: Look up! The ISS is above your head!! \n\n Hi,\nThis is your email reminder "
                                "when the ISS is over your location. Have fun watching it.")


def is_iss_near_me():
    # ISS - location API
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()

    latitude = float(response.json()['iss_position']["latitude"])
    longitude = float(response.json()['iss_position']["longitude"])
    iss_position = (latitude, longitude)
    my_position = (MY_LAT, MY_LNG)

    print(f"my position: {my_position}")
    print(f"iss position:  {iss_position}")

    lat_diff = abs(MY_LAT - latitude)
    lng_diff = abs(MY_LNG - longitude)

    print(f"lat diff: {lat_diff}")
    print(f"lang diff: {lng_diff}")

    if abs(lat_diff) < 5 and abs(lng_diff) < 5:
        return True


# If the ISS is close to my current position, and it is currently dark
# then email me to tell me to look up.
# Run the code every 60 seconds or any other timeframe
while True:
    print("checking...")
    if is_dark() is True and is_iss_near_me() is True:
        send_email()
        print("email sent")
        time.sleep(120)  # set the timer to 2 minutes, so that you don't get an email every 5 seconds

    time.sleep(5)


