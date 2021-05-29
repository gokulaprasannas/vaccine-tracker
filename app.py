import datetime
import json
import requests
import pandas as pd
from fake_useragent import UserAgent
import sys
from copy import deepcopy
import config
import time
import pyttsx3


def main(argv):
    try:
        print('Starting the Tracker')

        DATE_RANGE = config.DATE_RANGE
        MIN_AGE_LIMIT = config.MIN_AGE_LIMIT
        VACCINE_TYPE = config.VACCINE_TYPE
        PAYMENT = config.PAYMENT
        DISTRICT_ID = config.DISTRICT_ID
        AVAILABLE_CAPACITY = config.AVAILABLE_CAPACITY
        TIME_INTERVAL = config.TIME_INTERVAL

        browser_header = {'User-Agent': UserAgent().random}

        base = datetime.datetime.today()
        date_list = [base + datetime.timedelta(days=x)
                     for x in range(DATE_RANGE)]
        date_str = [x.strftime("%d-%m-%Y") for x in date_list]

        while True:
            final_df = None
            for INP_DATE in date_str:
                URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}".format(
                    DISTRICT_ID, INP_DATE)
                response = requests.get(URL, headers=browser_header)
                if (response.ok) and ('centers' in json.loads(response.text)):
                    resp_json = json.loads(response.text)['centers']
                    if resp_json is not None:
                        df = pd.DataFrame(resp_json)
                        if len(df):
                            df = df.explode("sessions")
                            df['min_age_limit'] = df.sessions.apply(
                                lambda x: x['min_age_limit'])
                            df['vaccine'] = df.sessions.apply(
                                lambda x: x['vaccine'])
                            df['available_capacity'] = df.sessions.apply(
                                lambda x: x['available_capacity'])
                            df['date'] = df.sessions.apply(lambda x: x['date'])
                            df = df[["date", "available_capacity", "vaccine", "min_age_limit", "pincode",
                                     "name", "state_name", "district_name", "block_name", "fee_type"]]
                            if final_df is not None:
                                final_df = pd.concat([final_df, df])
                            else:
                                final_df = deepcopy(df)

                            if MIN_AGE_LIMIT != None:
                                final_df = filter_column(
                                    final_df, "min_age_limit", MIN_AGE_LIMIT)

                            if PAYMENT != None:
                                final_df = filter_column(
                                    final_df, "fee_type", PAYMENT)

                            if VACCINE_TYPE != None:
                                final_df = filter_column(
                                    final_df, "vaccine", VACCINE_TYPE)

                            final_df = filter_capacity(
                                final_df, "available_capacity", AVAILABLE_CAPACITY)

                            if(len(final_df) > 0):
                                print("Vaccine available for the date - ", INP_DATE)
                                beep()
                            else:
                                print(
                                    "No vaccine available for the date - ", INP_DATE)
                        else:
                            print("No vaccine available for the date - ", INP_DATE)
                    else:
                        print("No rows in the data Extracted from the API")
            time.sleep(TIME_INTERVAL)
    except Exception as e:
        print('Exception occurred', e)
        sys.exit(2)


def filter_column(df, col, value):
    df_temp = deepcopy(df.loc[df[col] == value, :])
    return df_temp


def filter_capacity(df, col, value):
    df_temp = deepcopy(df.loc[df[col] >= value, :])
    return df_temp


def beep():
    engine = pyttsx3.init()
    engine.say("Vaccine Available, Vaccine Available")
    engine.runAndWait()


if __name__ == "__main__":
    main(sys.argv[1:])
