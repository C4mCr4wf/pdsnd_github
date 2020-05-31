import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = {'january': 1,
          'february': 2,
          'march': 3,
          'april': 4,
          'may': 5,
          'june': 6,
          'all': None}

DAYS = {'monday': 0,
        'tuesday': 1,
        'wednesday': 2,
        'thursday': 3,
        'friday': 4,
        'saturday': 5,
        'sunday': 6,
        'all': None}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    # Gets user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("\nTo get started, please select the city data you would like to expore. \n (please type 'chicago', 'new york city', or 'washington') : ").lower()
        if city not in CITY_DATA:
            print("\nSorry. That is not a valid city option. Please try again.")
            continue
        else:
            print("\nExcellent!\n")
            break
    # Gets user input for month (all, january, february, ... , june)
    while True:
        month = input("Please select the month you would like to explore. \n (please enter a month from 'january' to 'june', OR 'all') : ").lower()
        if month not in MONTHS:
            print("\nSorry. That is not a valid month option. Please try again.")
            continue
        else:
            print("\nWonderful!\n")
            break
    # Gets user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Finally, please select a particular day of the week you'd like to explore. \n (please enter a day from 'monday' to 'sunday', OR 'all') : ").lower()
        if day not in DAYS:
            print("\nSorry. That is not a valid day option. Please try again.")
            continue
        else:
            print("\nThanks! Now computing statistics: {}: {}: {} ...".format(city, month, day))
            break

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.weekday
    df['Hour Start'] = df['Start Time'].dt.hour

    imonth = MONTHS.get(str(month))
    iday = DAYS.get(str(day))
    #print(imonth, iday) #CHECKPOINT

    if month != 'all':
        df = df[df['Month'] == imonth]

    if day != 'all':
        df = df[df['Day of Week'] == iday]

    #print(df.head(20)) #CHECKPOINT
    return df



def time_stats(df, city, month, day):
    """Displays statistics on the most frequent times of travel.

    Args:
        df - Pandas DataFrame containing city data (filtered by month and day)
        (str) city - name of the user-selected city to analyze
        (str) month - name of the user-selected month to filter by, or "all" to apply no month filter
        (str) day - name of the user-selected day of week to filter by, or "all" to apply no day filter
    Returns:
        First value: (str) Confirmation of chosen city.
        Second value: (str) Most popular month - or confirmation of chosen month.
        Third value: (str) Most popular day of week - or confirmation of chosen day.
        Fourth value: (str) Most popular hour in which travel began.
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    print("In the city of " + city.title() + ":\n")

    # Displays the most common month, if not specifically selected

    if month == 'all':
        pop_month = df['Month'].mode()[0]
        print("The most popular month of travel was {}.\n".format(str(list(MONTHS.keys())[list(MONTHS.values()).index(pop_month)]).title())) #MESSY?
    else:
        print("For the month of {}: \n".format(month.title()))

    # Displays the most common day of week, if not specifically selected
    if day == 'all':
        pop_day = df['Day of Week'].mode()[0]
        print("The most popular day of travel was {}.\n".format(str(list(DAYS.keys())[list(DAYS.values()).index(pop_day)]).title())) # ... it works.
    else:
        print("On the day of {}: \n".format(day.title()))

    # Displays the most common start hour
    pop_start = df['Hour Start'].mode()[0]
    print('The most popular hour for travel to begin was {}:00.\n'.format(pop_start))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.

    Args:
        df - Pandas DataFrame containing city data (filtered by month and day).

    Returns:
        First value: (str) Most common start station.
        Second value: (str) Most common end station.
        Third value: (str) Most common combination of start and end.
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Displays most commonly used Start station
    common_start = df['Start Station'].mode()[0]
    print("Most trips began at: {}. \n".format(common_start))

    # Displays most commonly used End station
    common_end = df['End Station'].mode()[0]
    print("Most trips ended at: {}. \n".format(common_end))

    # Displays most frequent combination of Start station and End station trip
    df['start_end'] = "began at " + df['Start Station'] + ", and ended at " + df['End Station']
    common_trip = df['start_end'].mode()[0]
    print("Most common route: {}. \n".format(common_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Displays total travel time
    total_travel = df['Trip Duration'].sum().astype(int)
    total_hr_min = "{}:{}".format(*divmod(total_travel, 60))
    print("The total duration of all trips was {} hours:minutes.\n".format(total_hr_min))   # WOULD CONVERT TO DD:hh:mm if could figure out clean method

    # Displays mean travel time
    mean_travel = df['Trip Duration'].mean().astype(int)
    mean_hr_min = "{}:{}".format(*divmod(mean_travel, 60))
    print("The average trip duration was {} hours:minutes.\n".format(mean_hr_min))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Displays counts of user types
    user_type = df['User Type'].value_counts().to_frame()
    print("User totals by:\n\n{} \n".format(user_type))

    # Displays counts of gender, if column available
    if 'Gender' in df:
        gender = df['Gender'].value_counts().to_frame()
        print("User totals by:\n\n{} \n".format(gender))
    else:
        print("\nWashington has no gender data.\n")

    # Displays earliest, most recent, and most common year of birth, if data available
    if 'Birth Year' in df:
        oldest = df['Birth Year'].min()
        print("The oldest user was born in {}. \n".format(int(oldest)))
        youngest = df['Birth Year'].max()
        print("The youngest user was born in {}. \n".format(int(youngest)))
        common_born = df['Birth Year'].mode()
        print("The most common user birth year was {}. \n".format(int(common_born)))
    else:
        print("Washington has no birth year data.\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """ Allows user to request 5 rows of the raw dataframe data at a time. """

    # Removes custom column, sets 5 row index values
    df = df.drop(['Start Time', 'Month', 'Day of Week', 'Hour Start', 'start_end'], axis = 1)
    start_index = 0
    end_index = 5

    # Gets user input as to whether thet wish raw data to be displayed
    raw = input("\nWould you like to see 5 lines of the raw data used in this inquiry? Enter yes or no: ").lower()

    # Displays 5 rows of raw data, and gets user input as to whether they would like another 5
    while True:
        if raw == "yes":
            print('\n', df.iloc[start_index : end_index])
            start_index += end_index
            end_index += end_index
            raw = input('\nWould you like to see 5 more rows? Enter yes or no: ').lower()
            continue
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, city, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no:\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
