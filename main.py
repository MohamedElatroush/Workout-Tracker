import requests
from datetime import datetime
import os

NUTRITION_APP_ID = os.environ["NUTRITION_APP_ID"]
NUTRITION_API_KEY = os.environ["NUTRITION_API_KEY"]
NUTRITION_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheet_endpoint = os.environ["sheet_endpoint"]

sheet_username = os.environ["sheet_username"]
sheet_password = os.environ["sheet_password"]

GENDER = "male"
WEIGHT_KG = 88
HEIGHT_CM = 190
AGE = 25

active_dict = {}

headers = {
    "x-app-id": NUTRITION_APP_ID,
    "x-app-key": NUTRITION_API_KEY,
}

user_activity = input("Tell me which excercises you did: ")

parameters = {
    "query": user_activity,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

res = requests.post(NUTRITION_ENDPOINT, json=parameters, headers=headers)
res.raise_for_status()

# activity["Excercise"] = res.json()["name"]
# activity["duration"] = res.json()["duration_min"]

activity_list = res.json()['exercises']

for activity in activity_list:

    date = datetime.now()
    current_date = date.strftime("%d/%m/20%y")
    current_time = date.strftime("%H:%M:%S")
    sheet_input = {
        "workout":
            {
                "date": current_date,
                "time": current_time,
                "exercise": activity["name"].title(),
                "duration": activity["duration_min"],
                "calories": activity["nf_calories"]
            }
    }

    # Basic Authentication
    sheet_response = requests.post(
        sheet_endpoint,
        json=sheet_input,
        auth=(
            sheet_username,
            sheet_password,
        )
    )

    print(sheet_response.text)


