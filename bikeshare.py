import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters_city():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    # Welcome message
    print('*'*108)
    print("* In this version of the program you can select between the cities: chicago, new york city and washington, *")
    print("* and in addition you can select all of them (by writing 'All' or 'all') to obtain more wide information   *")
    print("* that include these three cities.                                                                         *")
    print("* You can also filter by month or weekday using the names or numbers to identify them; In months you can   *")
    print("* write '1' for January and '6' for June, and for weekdays '1' for Monday and '7' for Sunday.              *")
    print('*'*108, "\n")
    
    print('Welcome! Use this program to obtain some relevant information about the US bikeshare system')
    # Get user input for city (chicago, new york city, washington). 
    
    city = input("Enter the name of the city you want to see: ")
    # Format the input arguments (correct capitalized letters)
    city = city.lower()
    options = list(CITY_DATA.keys())
    options.extend(['all', 'exit'])
    while not city in options:
        city = input("Please write a valid name (chicago, new york city, washington or all) or write 'exit' to terminate the program: ")
        
    #return city, month, day
    return city

def get_filters_time():
    # Get user input for month (all, january, february, ... , june)
    month = input("Enter the month: ")
    # Format the input arguments (correct capitalized letters)
    month = month.lower()
    while not month in ('january', 'february', 'march', 'april', 'may', 'june', 'all', '1', '2', '3', '4', '5', '6'):
        month = input("Please write a valid month from january to june (numeric format is also permitted): ")

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Enter the day of the week: ")
    # Format the input arguments (correct capitalized letters)
    day = day.lower()
    while not day in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all', '1', '2', '3', '4', '5', '6', '7'):
        day = input("Please write a valid weekday from monday to sunday (numeric format is also permitted): ")
    print('-'*40)
    return month, day

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
    # load data file into a dataframe
    
    # If the user selected 'all' the cities, concatenate all the dataframes
    if city == 'all':
        
        cities = list(CITY_DATA.values())
        df = pd.DataFrame([])
        for i in cities:
            if df.empty:
                df = pd.read_csv(i)
            else:
                df = pd.concat([df,pd.read_csv(i)], sort = True)
    # If the user has just selected one city load it from the csv to df dataframe
    else:
        df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday + 1


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        months_dictionary = dict(zip(months, list(range(1, 7))))
        
        # If the user has selected the month in numeric format
        if month in ['1', '2', '3', '4', '5', '6']:
            selected_month = month
        # If the user has selected the month with its name
        else:
            selected_month = months_dictionary[month]
            
        # filter by month to create the new dataframe
        df = df[df['month'] == int(selected_month)]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        weekday_dictionary = dict(zip(days, list(range(1, 7))))
        
        # If the user has selected the weekday in numeric format
        if day in ['1', '2', '3', '4', '5', '6', '7']:
            selected_weekday = int(month)
        
        # If the user has selected the weekday with its name
        else:
            selected_weekday = weekday_dictionary[day]
            
        df = df[df['day_of_week'] == selected_weekday]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    most_common_month = df['month'].mode()[0]
    print("The most common month is: {}".format(most_common_month))
    
    # Display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print("The most common day of the week is: {}".format(most_common_day))

    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print("The most common start hour is: {}".format(most_common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    most_common_Start_Station = df['Start Station'].mode()[0]
    print("The most commonly used start station is: {}".format(most_common_Start_Station))
    # Display most commonly used end station
    most_common_End_Station = df['End Station'].mode()[0]
    print("The most commonly used end station is: {}".format(most_common_End_Station))


    # Display most frequent combination of start station and end station trip
    df['Station_Comb'] = df['Start Station'] + ' -> ' + df['End Station']
    most_common_Station_Comb = df['Station_Comb'].mode()[0]
    print("The most frequent combination of Start station and End station trip is: {}".format(most_common_Station_Comb))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    df['End Time'] = pd.to_datetime(df['End Time'])
    
    total_time = [(df['End Time'] - df['Start Time']).sum()]
    print ("The total of travel time considering all the trips is: {}".format(total_time[0]))

    # Display mean travel time
    mean_time = [(df['End Time'] - df['Start Time']).mean()]
    print ("The mean travel time is: {}".format(mean_time[0]))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    # Display counts of user types
    print("User types:")
    user_types = df['User Type'].value_counts()
    for i in range(user_types.size):
        print(user_types.index[i], user_types.values[i])

    # Considering that some of our files are missing important columns 
    # ("Gender") we'll handle the errors this may cause in this section below.
    # 
    print("\nNumber of users separated by gender:")
    try:
        # Display counts of gender
        gender_count = df['Gender'].value_counts()
        for i in range(gender_count.size):
            print("Number of {} users: {}".format(gender_count.index[i], gender_count.values[i]))
    
    except KeyError as e:
        print("Exception: The dataframe of the city selected doesn't include 'Gender' information.")
        #print("Error: {}".format(e))

    try:
        # Display earliest, most recent, and most common year of birth
        earliest_date = int(df['Birth Year'].min())
        most_recent_date = int(df['Birth Year'].max())
        most_common_year = int(df['Birth Year'].mode()[0])
        print("\nThe earliest date of year of birth is: {}\nThe most recent one: {}\nAnd the most common one: {}".format(earliest_date, most_recent_date, most_common_year))
    
    except KeyError as e:
        print("\nException: The dataframe of the city selected doesn't include 'Birth Year' information.")
        #print("Error: {}".format(e))
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    answer = input("Do you wish to see raw data of the dataframe? ")
    if answer == 'yes':
        start = 0
        end = 5
        while answer == 'yes':
            print(df.iloc[start:end])
            start += 5
            end += 5
            answer = input("Do you wish to see 5 more lines of raw data?\n")
    
def main():
    while True:
        #Divided get_filters() function to allow the option 'exit' in the program
        city = get_filters_city()
        if(city == 'exit'):
            break
        month, day = get_filters_time()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
