# Required, Date to start checking, 0 means today, 1 means tommorrow.. etc.
BASE_DATE = 1

# Required, Range of the date to check, base date will be BASE_DATE.
DATE_RANGE = 5

# Required, Supported values [18,45], Leave it as `MIN_AGE_LIMIT = None` if no filter required
MIN_AGE_LIMIT = 18

# Required, Supported values ['COVAXIN','COVISHIELD'], Leave it as `VACCINE_TYPE = None` if no filter required
VACCINE_TYPE = None

# Required, Supported values ['Free', 'Paid'], Leave it as `PAYMENT = None` if no filter required
PAYMENT = None

# Required, Check the district_mapping.csv to find the relevant district_id
DISTRICT_ID = 294  # defaults to Madurai

# Required, minimum available capacity to match the criteria and trigger buzzer
AVAILABLE_CAPACITY = 1

# Required, Supported values ['Dose 1', 'Dose 2'], Leave it as `DOSAGE_TYPE = None` if no filter required
DOSAGE_TYPE = 'Dose 1'

# Optional, Copy and paste the exact preferred hospital name from cowin app
HOSPITAL_NAME = None

# Required, time interval to check for the availability in seconds. Recommended 30s.
TIME_INTERVAL = 30
