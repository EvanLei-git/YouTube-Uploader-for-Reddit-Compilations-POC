import datetime 
import time
import random
import os,sys
sys.dont_write_bytecode = True

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the configurations module
import configurations

def extract_month(utc_timestamp):
    # Convert the UTC timestamp to a datetime object
    datetime_obj = datetime.datetime.utcfromtimestamp(utc_timestamp)
    # Extract the month from the datetime object
    month = datetime_obj.month
    return month

def extract_year(utc_timestamp):
    # Convert the UTC timestamp to a datetime object
    datetime_obj = datetime.datetime.utcfromtimestamp(utc_timestamp)
    # Extract  year from the datetime object
    year = datetime_obj.year % 100
    return year

'''
def randomNearDay():
    start_date = datetime.date(2023, 1, 1)
    end_date = datetime.date.today()

    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    unixtime = time.mktime(random_date.timetuple())
    UT = str(unixtime)[:-2]
    #print(random_date)
    return(UT)
'''
def randomNearDay():
    # Define the start and end dates for the range of random dates
    end_date = datetime.date.today()
    start_date = end_date.replace(day=1) - datetime.timedelta(days=30)
    # Generate a random date within the range of the current or previous month
    random_date = start_date + datetime.timedelta(days=random.randint(0, (end_date - start_date).days))
    # Convert the random date to a Unix timestamp
    unixtime = time.mktime(random_date.timetuple())
    UT = str(unixtime)[:-2]
    return UT

def randomDay():
    start_date = configurations.SEARCH_DATE
    end_date = time.strftime('%Y-%m-%d')

    start_unixtime = int(time.mktime(time.strptime(start_date, '%Y-%m-%d')))
    end_unixtime = int(time.mktime(time.strptime(end_date, '%Y-%m-%d')))

    random_unixtime = random.randint(start_unixtime, end_unixtime)
    random_timestamp = str(random_unixtime)
    print (random_timestamp)
    return random_timestamp