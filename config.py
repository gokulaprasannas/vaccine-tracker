# Required, Range of the date to check, base date will be the current date.
DATE_RANGE = 3

# Required, Supported values [18,45], Leave it as `MIN_AGE_LIMIT = None` if no filter required
MIN_AGE_LIMIT = 18

# Required, Supported values ['COVAXIN','COVISHIELD'], Leave it as `VACCINE_TYPE = None` if no filter required
VACCINE_TYPE = 'COVAXIN'

# Required, Supported values ['Free', 'Paid'], Leave it as `PAYMENT = None` if no filter required
PAYMENT = None

# Required, Check the district_mapping.csv to find the relevant district_id
DISTRICT_ID = 540  # defaults to Madurai

# Required, minimum available capacity to match the criteria and trigger buzzer
AVAILABLE_CAPACITY = 0

# Required, time interval to check for the availability in seconds. Recommended 30s.
TIME_INTERVAL = 30
