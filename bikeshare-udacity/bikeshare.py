import time
import calendar
from csv import DictReader as dict_reader
from collections import Counter as counter
from datetime import datetime
from functools import reduce

## Filenames
chicago = 'chicago.csv'
new_york_city = 'new_york_city.csv'
washington = 'washington.csv'

CITY_TO_FILENAME_DICT = {
    "chicago": chicago,
    "new york": new_york_city,
    "washington": washington
}

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

start_time_name = "Start Time"
end_time_name = "End Time"
trip_duration_name = "Trip Duration"
start_station_name = "Start Station"
end_station_name = "End Station"
user_type_name = "User Type"
gender_name = "Gender"
birth_year_name = "Birth Year"

def read_city_csv(city):
    '''Reads the csv file of the desired city

    Args:
        city: The name of the city, of which the csv file is desired to be read.
    Returns:
        (list) List of each bike ride info of the selected city as a dict.
    '''

    with open(CITY_TO_FILENAME_DICT.get(city)) as f:
        data = [{k: str(v) for k, v in row.items()}
            for row in dict_reader(f, skipinitialspace=True)]
    
    return data

def readable_row(rides):
    '''Turns a list of raw bike ride data into a readable string.

    Args:
        rides: List of a raw bike ride info.
    Returns:
        (str) Readable string of the bike ride info list provided.
    '''

    readable = "Here is the next " + str(len(rides)) + " rides:\n"
    for i, ride in enumerate(rides):
        readable += "**********\n"
        for key, value in ride.items():
            if value == None or value == '':
                value = 'N/A'
            readable += "\t" + key + ": " + value + "\n"
    
    readable += "**********\n"    
    return readable

def get_five_rows(city_file, range):
    '''Generator function that give readable bike ride entries.

    Args:
        city_file: The data that is read from the csv file.
        range: number of entries wanted
    Returns:
        (iterator) Iterator for the desired amount of bike rides.
    '''

    i = 0

    while i < len(city_file):
        yield readable_row(city_file[i:i+5])
        i += 5

def get_city():
    '''Asks the user for a city and returns the filename for that city's bike share data.

    Args:
        none.
    Returns:
        (str) Filename for a city's bikeshare data.
    '''

    city = input('\nHello! Let\'s explore some US bikeshare data!\n'
                 'Would you like to see data for Chicago, New York, or Washington?\n').lower()
    
    while 1:
        if city == "chicago" or city == "new york" or city == "washington":
            return city
        else:
            city = input('\nYou\'ve entered invalid city, please enter one of these:\n'
                 'Chicago, New York, Washington.\n')
    
def get_time_period():
    '''Asks the user for a time period and returns the specified filter.

    Args:
        none.
    Returns:
        (str) Time period filter for the desired bikeshare data, or 'none' if not specified.
    '''
    time_period = input('\nWould you like to filter the data by month, day, or not at'
                        ' all? Type "none" for no time filter.\n').lower()
    
    while 1:
        if time_period == "month" or time_period == "day" or time_period == "none":
            return time_period
        else:
            time_period = input('\nYou\'ve entered invalid filter, please enter one of these:\n'
                 'month, day, none.\n').lower()

def get_month():
    '''Asks the user for a month and returns the specified month.

    Args:
        none.
    Returns:
        (str) The month name that the user inputs.
    '''
    month = input('\nWhich month? January, February, March, April, May, or June?\n').title()
    
    while 1:
        if month in calendar.month_name[1:7]:
            return month
        else:
            month = input('\nPlease enter one of these months:\n'
                 'January, February, March, April, May, June.\n').title()


def get_day():
    '''Asks the user for a day and returns the specified day.

    Args:
        none.
    Returns:
        (str) The day name that the user inputs.
    '''
    day_number = int(input('\nWhich day? Please type your response as an integer.\n'))

    while 1:
        if day_number in range(7):
            return calendar.day_name[day_number]
        else:
            day_number = int(input('\nYou\'ve entered invalid day, please enter one of these:\n'
                 '0, 1, 2, 3, 4, 5, 6.\n'))


def popular_month(city_file):
    '''Gets the most popular month from the specified csv file data

    Args:
        city_file: The data that is read from the csv file.
    Returns:
        (str) The most popular month of the data file.
    '''

    data_months = [datetime.strptime(ride.get(start_time_name), DATE_FORMAT).month for ride in city_file]
    popular_month_number = counter(data_months).most_common(1)[0][0]
    return calendar.month_name[popular_month_number]


def popular_day(city_file, month_name = 'none'):
    '''Gets the most popular day from the specified csv file data.
        If the month is specified, it finds the most popular day of that month.

    Args:
        city_file: The data that is read from the csv file.
        month_name: The month filter for the most popular day. It searches through the days of all months if 'none' is given as input.
    Returns:
        (str) The most popular day of the specified time period for the city data.
    '''
    
    if month_name == 'none':
        data_days = [datetime.strptime(ride.get(start_time_name), DATE_FORMAT).weekday() for ride in city_file]
    else:
        month_to_number = {v: k for k,v in enumerate(calendar.month_name)}
        data_days = [datetime.strptime(ride.get(start_time_name), DATE_FORMAT).weekday() 
                    for ride in city_file 
                    if datetime.strptime(ride.get(start_time_name), DATE_FORMAT).month == month_to_number.get(month_name.title())]

    popular_day_number = counter(data_days).most_common(1)[0][0]
    return calendar.day_name[popular_day_number]


def popular_hour(city_file, month_or_day = 'none'):
    '''Gets the most popular hour from the specified csv file data.
        If the month is specified, it finds the most popular hour of that month.
        If the day is specified, it finds the most popular hour of that day.

    Args:
        city_file: The data that is read from the csv file.
        month_or_day: The month/day filter for the most popular hour. Both month and day names are accepted. It searches through all hours if 'none' is given as input.
    Returns:
        (int) The most popular hour of the data file for the specified time period from 1 to 24.
    '''

    if month_or_day == 'none':
        data_hours = [datetime.strptime(ride.get(start_time_name), DATE_FORMAT).hour for ride in city_file]
    elif month_or_day in calendar.month_name[1:7]:
        month_to_number = {v: k for k,v in enumerate(calendar.month_name)}
        data_hours = [datetime.strptime(ride.get(start_time_name), DATE_FORMAT).hour 
                        for ride in city_file 
                        if datetime.strptime(ride.get(start_time_name), DATE_FORMAT).month == month_to_number.get(month_or_day.title())]
    elif month_or_day in calendar.day_name:
        day_to_number = {v: k for k,v in enumerate(calendar.day_name)}
        data_hours = [datetime.strptime(ride.get(start_time_name), DATE_FORMAT).hour 
                        for ride in city_file
                        if datetime.strptime(ride.get(start_time_name), DATE_FORMAT).weekday() == day_to_number.get(month_or_day.title())]

    popular_hour = counter(data_hours).most_common(1)[0][0]
    return popular_hour


def trip_duration(city_file, month_or_day = 'none'):
    '''Gets the total and average trip durations from the specified csv file data.
        If the month is specified, it calculates for that month.
        If the day is specified, it calculates for that day.

    Args:
        city_file: The data that is read from the csv file.
        month_or_day: The month/day filter. Both month and day names are accepted. It searches calculates over all data if 'none' is given as input.
    Returns:
        (tuple) The total trip duration and the average trip duration in string with notation "X hours, Y minutes, Z seconds", respectively.
    '''

    if month_or_day == 'none':
        trip_durations = [float(ride.get(trip_duration_name)) for ride in city_file]
    elif month_or_day in calendar.month_name[1:7]:
        month_to_number = {v: k for k,v in enumerate(calendar.month_name)}
        trip_durations = [float(ride.get(trip_duration_name))
                        for ride in city_file 
                        if datetime.strptime(ride.get(start_time_name), DATE_FORMAT).month == month_to_number.get(month_or_day.title())]
    elif month_or_day in calendar.day_name:
        day_to_number = {v: k for k,v in enumerate(calendar.day_name)}
        trip_durations = [float(ride.get(trip_duration_name))
                        for ride in city_file
                        if datetime.strptime(ride.get(start_time_name), DATE_FORMAT).weekday() == day_to_number.get(month_or_day.title())]

    total_trip_duration = reduce((lambda x, y: x + y), trip_durations)
    average_trip_duration = total_trip_duration / len(trip_durations)

    m, s = divmod(total_trip_duration, 60)
    h, m = divmod(m, 60)
    total_trip_duration_str = "%d hours, %02d minutes, %02d seconds" % (h, m, s)

    m, s = divmod(average_trip_duration, 60)
    h, m = divmod(m, 60)
    average_trip_duration_str = "%d hours, %02d minutes, %02d seconds" % (h, m, s)

    return (total_trip_duration_str, average_trip_duration_str)

def popular_stations(city_file, month_or_day = 'none'):
    '''Gets the most popular start and end stations from the specified csv file data.
        If the month is specified, it finds the most popular stations for that month.
        If the day is specified, it finds the most popular stations for that day.

    Args:
        city_file: The data that is read from the csv file.
        month_or_day: The month/day filter. Both month and day names are accepted. It searches over all data if 'none' is given as input.
    Returns:
        (tuple) The ((most popular start station, number of usage), (most popular end station, number of usage)) tuple.
    '''
    
    if month_or_day == 'none':
        stations = [(ride.get(start_station_name), ride.get(end_station_name)) for ride in city_file]
    elif month_or_day in calendar.month_name[1:7]:
        month_to_number = {v: k for k,v in enumerate(calendar.month_name)}
        stations = [(ride.get(start_station_name), ride.get(end_station_name))
                        for ride in city_file 
                        if datetime.strptime(ride.get(start_time_name), DATE_FORMAT).month == month_to_number.get(month_or_day.title())]
    elif month_or_day in calendar.day_name:
        day_to_number = {v: k for k,v in enumerate(calendar.day_name)}
        stations = [(ride.get(start_station_name), ride.get(end_station_name))
                        for ride in city_file
                        if datetime.strptime(ride.get(start_time_name), DATE_FORMAT).weekday() == day_to_number.get(month_or_day.title())]

    start_stations, end_stations = zip(*stations)

    popular_start_station = counter(start_stations).most_common(1)[0]
    popular_end_station = counter(end_stations).most_common(1)[0]

    return (popular_start_station, popular_end_station)


def popular_trip(city_file, month_or_day = 'none'):
    '''Gets the most popular trip from the specified csv file data.
        If the month is specified, it finds the most popular trip for that month.
        If the day is specified, it finds the most popular trip for that day.

    Args:
        city_file: The data that is read from the csv file.
        month_or_day: The month/day filter. Both month and day names are accepted. It searches over all data if 'none' is given as input.
    Returns:
        (tuple) The ((start station, end station), number of usage) of the most popular trip.
    '''

    if month_or_day == 'none':
        stations = [(ride.get(start_station_name), ride.get(end_station_name)) for ride in city_file]
    elif month_or_day in calendar.month_name[1:7]:
        month_to_number = {v: k for k,v in enumerate(calendar.month_name)}
        stations = [(ride.get(start_station_name), ride.get(end_station_name))
                        for ride in city_file 
                        if datetime.strptime(ride.get(start_time_name), DATE_FORMAT).month == month_to_number.get(month_or_day.title())]
    elif month_or_day in calendar.day_name:
        day_to_number = {v: k for k,v in enumerate(calendar.day_name)}
        stations = [(ride.get(start_station_name), ride.get(end_station_name))
                        for ride in city_file
                        if datetime.strptime(ride.get(start_time_name), DATE_FORMAT).weekday() == day_to_number.get(month_or_day.title())]

    popular_trip = counter(stations).most_common(1)[0]

    return popular_trip


def users(city_file, month_or_day = 'none'):
    '''Counts the users of each user type from the specified csv file data.
        If the month is specified, it counts the users for that month.
        If the day is specified, it counts the users for that day.

    Args:
        city_file: The data that is read from the csv file.
        month_or_day: The month/day filter. Both month and day names are accepted. It counts over all data if 'none' is given as input.
    Returns:
        (dict) A dictionary having user types as keys and user counts as values.
    '''

    if month_or_day == 'none':
        data_users = [ride.get(user_type_name) for ride in city_file]
    elif month_or_day in calendar.month_name[1:7]:
        month_to_number = {v: k for k,v in enumerate(calendar.month_name)}
        data_users = [ride.get(user_type_name)
                        for ride in city_file 
                        if datetime.strptime(ride.get(start_time_name), DATE_FORMAT).month == month_to_number.get(month_or_day.title())]
    elif month_or_day in calendar.day_name:
        day_to_number = {v: k for k,v in enumerate(calendar.day_name)}
        data_users = [ride.get(user_type_name)
                        for ride in city_file
                        if datetime.strptime(ride.get(start_time_name), DATE_FORMAT).weekday() == day_to_number.get(month_or_day.title())]

    user_counts = counter(data_users).most_common()

    user_counts_dict = {}
    for user_type, user_count in user_counts:
        user_counts_dict[user_type] = user_count

    return user_counts_dict


def gender(city_file, month_or_day = 'none'):
    '''Counts the genders from the specified csv file data.
        If the month is specified, it counts the genders for that month.
        If the day is specified, it counts the genders for that day.

    Args:
        city_file: The data that is read from the csv file.
        month_or_day: The month/day filter. Both month and day names are accepted. It counts over all data if 'none' is given as input.
    Returns:
        (dict) A dictionary having gender names as keys and gender counts as values.
    '''

    if month_or_day == 'none':
        data_genders = [ride.get(gender_name) for ride in city_file]
    elif month_or_day in calendar.month_name[1:7]:
        month_to_number = {v: k for k,v in enumerate(calendar.month_name)}
        data_genders = [ride.get(gender_name)
                        for ride in city_file 
                        if datetime.strptime(ride.get(start_time_name), DATE_FORMAT).month == month_to_number.get(month_or_day.title())]
    elif month_or_day in calendar.day_name:
        day_to_number = {v: k for k,v in enumerate(calendar.day_name)}
        data_genders = [ride.get(gender_name)
                        for ride in city_file
                        if datetime.strptime(ride.get(start_time_name), DATE_FORMAT).weekday() == day_to_number.get(month_or_day.title())]

    gender_counts = counter(data_genders).most_common()

    gender_counts_dict = {}
    for gender_type, gender_count in gender_counts:
        if gender_type == '':
            # Gender unspecified
            gender_counts_dict['gender unspecified'] = gender_count
        else:
            gender_counts_dict[gender_type.lower()] = gender_count

    return gender_counts_dict

def birth_years(city_file, month_or_day = 'none'):
    '''TODO: fill out docstring with description, arguments, and return values.
    Question: What are the earliest (i.e. oldest user), most recent (i.e. youngest user),
    and most popular birth years?
    '''
    '''Gets the earliest (i.e. oldest user), most recent (i.e. youngest user), and most popular birth years.
        If the month is specified, it finds these information for that month.
        If the day is specified, it finds these information for that day.

    Args:
        city_file: The data that is read from the csv file.
        month_or_day: The month/day filter. Both month and day names are accepted. It searches over all data if 'none' is given as input.
    Returns:
        (dict) A dictionary having "most popular birth year", "oldest user", "youngest user" as keys.
    '''
    
    if month_or_day == 'none':
        data_birth_years = [int(float(ride.get(birth_year_name))) for ride in city_file if ride.get(birth_year_name) != '']
    elif month_or_day in calendar.month_name[1:7]:
        month_to_number = {v: k for k,v in enumerate(calendar.month_name)}
        data_birth_years = [int(float(ride.get(birth_year_name)))
                        for ride in city_file if ride.get(birth_year_name) != ''
                        if datetime.strptime(ride.get(start_time_name), DATE_FORMAT).month == month_to_number.get(month_or_day.title())]
    elif month_or_day in calendar.day_name:
        day_to_number = {v: k for k,v in enumerate(calendar.day_name)}
        data_birth_years = [int(float(ride.get(birth_year_name)))
                        for ride in city_file if ride.get(birth_year_name) != ''
                        if datetime.strptime(ride.get(start_time_name), DATE_FORMAT).weekday() == day_to_number.get(month_or_day.title())]

    birth_years_dict = {}

    birth_years_dict["most popular birth year"] = str(counter(data_birth_years).most_common(1)[0][0])
    current_year = datetime.now().year
    lowest_birth_year = min(data_birth_years)
    highest_birth_year = max(data_birth_years)
    birth_years_dict["oldest user"] = str(current_year - lowest_birth_year) + " (birth year: " + str(lowest_birth_year) + ")"
    birth_years_dict["youngest user"] = str(current_year - highest_birth_year) + " (birth year: " + str(highest_birth_year) + ")"
    
    return birth_years_dict

def display_data(city_file):
    '''Displays five lines of data if the user specifies that they would like to.
    After displaying five lines, ask the user if they would like to see five more,
    continuing asking until they say stop.

    Args:
        city_file: The data that is read from the csv file.
    Returns:
        none.
    '''
    
    display = input('Would you like to view individual trip data?'
                    'Type \'yes\' or \'no\'.\n').lower()

    for five_rows in get_five_rows(city_file, 5):
                        
        if display in ["no", "n"]:
            return
        elif display in ["yes", "y"]:
            print(five_rows)
        else:
            display = input('\nYou\'ve entered invalid answer, please enter one of these:\n'
                '\'yes\', \'no\'.\n').lower()
            continue
        
        display = input('\nWould you like to view individual trip data?'
                        'Type \'yes\' or \'no\'.\n').lower()


def statistics():
    '''Calculates and prints out the descriptive statistics about a city and time period
    specified by the user via raw input.

    Args:
        none.
    Returns:
        none.
    '''
    # Filter by city (Chicago, New York, Washington)
    city = get_city()

    print('Reading city csv file...')
    city_data = read_city_csv(city)

    # Filter by time period (month, day, none)
    time_period = get_time_period()

    if time_period == 'month':
        month = get_month()
    elif time_period == 'day':
        day = get_day()

    print('\nCalculating the first statistic...')
    print('\n-----------------------------------')

    if len(city_data) > 0:

        if city_data[0].get(start_time_name) != None:
            # Most popular month for start time.
            if time_period == 'none':
                start_time = time.time()
                
                print("The most popular month for {} is {}.".format(city.title(), popular_month(city_data).title()))
                
                print("\nThat took %s seconds." % (time.time() - start_time))
                print("Calculating the next statistic...")
                print('-----------------------------------\n')
                print('-----------------------------------')

            # Most popular day of week (Monday, Tuesday, etc.) for start time.
            if time_period == 'none' or time_period == 'month':
                start_time = time.time()
                
                if time_period == 'none':
                    print("The most popular day for {} is {}.".format(city.title(), popular_day(city_data).title()))
                elif time_period == 'month':
                    print("The most popular day for {} in {} is {}.".format(city.title(), month.title(), popular_day(city_data, month).title()))
                
                print("\nThat took %s seconds." % (time.time() - start_time))
                print("Calculating the next statistic...")    
                print('-----------------------------------\n')
                print('-----------------------------------')
                
            start_time = time.time()

            # Most popular hour of day (1-24) for start time.
            if time_period == 'none':
                print("The most popular hour for {} is {}.".format(city.title(), popular_hour(city_data)))
            elif time_period == 'month':
                print("The most popular hour for {} in {} is {}.".format(city.title(), month.title(), popular_hour(city_data, month)))
            elif time_period == 'day':
                print("The most popular hour for {} in {} is {}.".format(city.title(), day.title(), popular_hour(city_data, day)))

            print("\nThat took %s seconds." % (time.time() - start_time))
            print("Calculating the next statistic...")
            print('-----------------------------------\n')
            print('-----------------------------------')
            start_time = time.time()

        if city_data[0].get(trip_duration_name) != None:
            # Total and average trip durations.
            if time_period == 'none':
                total_trip_duration, average_trip_duration = trip_duration(city_data)
                print("The total trip duration is {} and average trip duration is {} for {}.".format(total_trip_duration, average_trip_duration, city.title()))
            elif time_period == 'month':
                total_trip_duration, average_trip_duration = trip_duration(city_data, month)
                print("The total trip duration is {} and average trip duration is {} for {} in {}.".format(total_trip_duration, average_trip_duration, city.title(), month.title()))
            elif time_period == 'day':
                total_trip_duration, average_trip_duration = trip_duration(city_data, day)
                print("The total trip duration is {} and average trip duration is {} for {} in {}.".format(total_trip_duration, average_trip_duration, city.title(), day.title()))

            print("\nThat took %s seconds." % (time.time() - start_time))
            print("Calculating the next statistic...")
            print('-----------------------------------\n')
            print('-----------------------------------')
            start_time = time.time()


        if city_data[0].get(start_station_name) != None and city_data[0].get(end_station_name) != None:
            # Most popular start and end stations.
            if time_period == 'none':
                (popular_start_station, no_of_start), (popular_end_station, no_of_end) = popular_stations(city_data)
                print("The most popular start station is {} (no. of usage: {}) and the most popular end station is {} (no. of usage: {}) for {}.".format(popular_start_station, str(no_of_start), popular_end_station, str(no_of_end), city.title()))
            elif time_period == 'month':
                (popular_start_station, no_of_start), (popular_end_station, no_of_end) = popular_stations(city_data, month)
                print("The most popular start station is {} (no. of usage: {}) and the most popular end station is {} (no. of usage: {}) for {} in {}.".format(popular_start_station, str(no_of_start), popular_end_station, str(no_of_end), city.title(), month.title()))
            elif time_period == 'day':
                (popular_start_station, no_of_start), (popular_end_station, no_of_end) = popular_stations(city_data, day)
                print("The most popular start station is {} (no. of usage: {}) and the most popular end station is {} (no. of usage: {}) for {} in {}.".format(popular_start_station, str(no_of_start), popular_end_station, str(no_of_end), city.title(), day.title()))

            print("\nThat took %s seconds." % (time.time() - start_time))
            print("Calculating the next statistic...")
            print('-----------------------------------\n')
            print('-----------------------------------')
            start_time = time.time()

            # Most popular trip routes.
            if time_period == 'none':
                (popular_trip_start, popular_trip_end), no_of_trip = popular_trip(city_data)
                print("The most popular trip is from {}, to {} (no. of usage: {}) for {}.".format(popular_trip_start, popular_trip_end, str(no_of_trip), city.title()))
            elif time_period == 'month':
                (popular_trip_start, popular_trip_end), no_of_trip = popular_trip(city_data, month)
                print("The most popular trip is from {}, to {} (no. of usage: {}) for {} in {}.".format(popular_trip_start, popular_trip_end, str(no_of_trip), city.title(), month.title()))
            elif time_period == 'day':
                (popular_trip_start, popular_trip_end), no_of_trip = popular_trip(city_data, day)
                print("The most popular trip is from {}, to {} (no. of usage: {}) for {} in {}.".format(popular_trip_start, popular_trip_end, str(no_of_trip), city.title(), day.title()))

            print("\nThat took %s seconds." % (time.time() - start_time))
            print("Calculating the next statistic...")
            print('-----------------------------------\n')
            print('-----------------------------------')
            start_time = time.time()

        if city_data[0].get(user_type_name) != None:
            # Number of user counts for each user type.
            if time_period == 'none':
                user_counts_dict = users(city_data)
                print("There are: ", end='')
                for user_type, user_count in user_counts_dict.items():
                    print("{} {} users, ".format(str(user_count), user_type), end='')
                print("for {}.".format(city.title()))
            elif time_period == 'month':
                user_counts_dict = users(city_data, month)
                print("There are: ", end='')
                for user_type, user_count in user_counts_dict.items():
                    print("{} {} users, ".format(str(user_count), user_type), end='')
                print("for {} in {}.".format(city.title(), month.title()))
            elif time_period == 'day':
                user_counts_dict = users(city_data, day)
                print("There are: ", end='')
                for user_type, user_count in user_counts_dict.items():
                    print("{} {} users, ".format(str(user_count), user_type), end='')
                print("for {} in {}.".format(city.title(), day.title()))

            print("\nThat took %s seconds." % (time.time() - start_time))
            print("Calculating the next statistic...")
            print('-----------------------------------\n')
            print('-----------------------------------')
            start_time = time.time()

        if city_data[0].get(gender_name) != None:
            # Number of each genders (includes count of unspecified).
            if time_period == 'none':
                gender_counts_dict = gender(city_data)
                print("There are: ", end='')
                for gender_type, gender_count in gender_counts_dict.items():
                    print("{} {} users, ".format(str(gender_count), gender_type), end='')
                print("for {}.".format(city.title()))
            elif time_period == 'month':
                gender_counts_dict = gender(city_data, month)
                print("There are: ", end='')
                for gender_type, gender_count in gender_counts_dict.items():
                    print("{} {} users, ".format(str(gender_count), gender_type), end='')
                print("for {} in {}.".format(city.title(), month.title()))
            elif time_period == 'day':
                gender_counts_dict = gender(city_data, day)
                print("There are: ", end='')
                for gender_type, gender_count in gender_counts_dict.items():
                    print("{} {} users, ".format(str(gender_count), gender_type), end='')
                print("for {} in {}.".format(city.title(), day.title()))

            print("\nThat took %s seconds." % (time.time() - start_time))
            print("Calculating the next statistic...")
            print('-----------------------------------\n')
            print('-----------------------------------')
            start_time = time.time()

        if city_data[0].get(birth_year_name) != None:
            # Youngest and oldest users and most popular birth year.
            if time_period == 'none':
                birth_years_dict = birth_years(city_data)
                print("The ", end='')
                for key_name, key_value in birth_years_dict.items():
                    print("{} is {}, ".format(key_name, key_value), end='')
                print("for {}.".format(city.title()))
            elif time_period == 'month':
                birth_years_dict = birth_years(city_data)
                print("The ", end='')
                for key_name, key_value in birth_years_dict.items():
                    print("{} is {}, ".format(key_name, key_value), end='')
                print("for {} in {}.".format(city.title(), month.title()))
            elif time_period == 'day':
                birth_years_dict = birth_years(city_data)
                print("The ", end='')
                for key_name, key_value in birth_years_dict.items():
                    print("{} is {}, ".format(key_name, key_value), end='')
                print("for {} in {}.".format(city.title(), day.title()))

            print("\nThat took %s seconds." % (time.time() - start_time))
            print('-----------------------------------\n')

    else:
        print('\nEmpty city bike ride data!\n')
        return

    # Display five lines of data at a time if user specifies that they would like to
    display_data(city_data)
    print('-----------------------------------\n')

    # Restart?
    restart = input('\nWould you like to restart? Type \'yes\' or \'no\'.\n').lower()
    if restart in ['yes', 'y']:
        statistics()
    
    return


if __name__ == "__main__":
    try:
	    statistics()
    except KeyboardInterrupt:
        print("Keyboard interrupt detected, leaving shortly...")
    except:
        print("There is something went wrong, terminating...")
    finally:
        print("See you later, take care!")
    