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
        DOSAGE_TYPE = config.DOSAGE_TYPE
        HOSPITAL_NAME = config.HOSPITAL_NAME

        base = datetime.datetime.today()
        date_list = [base + datetime.timedelta(days=x)
                     for x in range(DATE_RANGE)]
        date_str = [x.strftime("%d-%m-%Y") for x in date_list]
        loop_count = 0

        while True:
            final_df = None
            loop_count += 1
            print(
                '-------------------------------Loop Count ' + str(loop_count) + '-------------------------------')
            for INP_DATE in date_str:
                URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}".format(
                    DISTRICT_ID, INP_DATE)
                response = requests.get(
                    URL, headers={'User-Agent': UserAgent().random})
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
                            df['available_capacity_dose1'] = df.sessions.apply(
                                lambda x: x['available_capacity_dose1'])
                            df['available_capacity_dose2'] = df.sessions.apply(
                                lambda x: x['available_capacity_dose2'])
                            df['date'] = df.sessions.apply(lambda x: x['date'])
                            df = df[["date", "available_capacity", "vaccine", "min_age_limit", "pincode",
                                     "name", "state_name", "district_name", "block_name", "fee_type", "available_capacity_dose1", "available_capacity_dose2"]]
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

                            if HOSPITAL_NAME != None:
                                final_df = filter_column(
                                    final_df, "name", HOSPITAL_NAME)

                            final_df = filter_capacity(
                                final_df, "available_capacity", AVAILABLE_CAPACITY)

                            if DOSAGE_TYPE != None:
                                if DOSAGE_TYPE == 'Dose 1':
                                    final_df = filter_capacity(
                                        final_df, "available_capacity_dose1", 1)
                                else:
                                    final_df = filter_capacity(
                                        final_df, "available_capacity_dose2", 1)

                            if(len(final_df) > 0):
                                print("------------Vaccine available for the date - ",
                                      INP_DATE, "----------------")
                                for (i, row) in final_df.iterrows():
                                    print(" Hospital -", row['name'], ", Age -", str(row['min_age_limit']), ", Vaccine", row['vaccine'], ', Payment -',
                                          row['fee_type'], ', Dose 1 -', str(row['available_capacity_dose1']), ', Dose 2 -', str(row['available_capacity_dose2']))
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
