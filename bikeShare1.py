import time
import pandas as pd
import numpy as np
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """ 
    Asks user to specify a city, month, and day to analyze. 

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of the week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # Get user input for city (chicago, new york city, washington)
    # HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            # Ask the user to choose a city
            city = input('Please choose a city from these (chicago, new york city, washington): ').strip().lower()
            # Check if the input city is valid
            if city in ['chicago', 'new york city', 'washington']:
                print(f"You selected: {city}")
                break  # Exit loop if valid city is selected
            else:
                print("Invalid city, please choose from chicago, new york city, washington.")
        except Exception as e:
            print(f"An error occurred: {e}. Please try again.")

    # Get user input for month (all, january, february, ... , june)
    while True:
        try:
            # Ask the user to choose a month
            month = input('Please enter a month (All, January, February, ... June): ').strip().lower()
            # Check if the input month is valid
            if month in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
                print(f"You selected: {month.capitalize()}")
                break  # Exit loop if valid month is selected
            else:
                print("Invalid month, please enter a valid month.")
        except Exception as e:
            print(f"An error occurred: {e}. Please try again.")

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            # Ask the user to choose a day of the week
            day = input('Please enter a day of the week (All, Monday, Tuesday, ... Sunday): ').strip().lower()
            # Check if the input day is valid
            if day in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                print(f"You selected: {day.capitalize()}")
                break  # Exit loop if valid day is selected
            else:
                print("Invalid day, please enter a valid day of the week (All, Monday, Tuesday, ... Sunday).")
        except Exception as e:
            print(f"An error occurred: {e}. Please try again.")

    # Print a separator line to improve readability
    print('-'*40)

    # Return the user's selections (city, month, day)
    return city, month, day

#-------------------------------------------------------------
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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df
#--------------------------------------------------------------------
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    try:
        # Convert 'Start Time' to datetime format
        df['Start Time'] = pd.to_datetime(df['Start Time'])

        # Extract month from 'Start Time' and create a new column for it
        df['month'] = df['Start Time'].dt.month

        # Display the most common month
        try:
            popular_month = df['month'].mode()[0]
            print('Most Popular Month is:', popular_month)
        except IndexError:
            print("No data available for the month.")

        # Extract day of the week from 'Start Time' and create a new column for it
        df['day'] = df['Start Time'].dt.day_name()

        # Display the most common day of the week
        try:
            popular_day = df['day'].mode()[0]
            print('Most Popular Day is:', popular_day)
        except IndexError:
            print("No data available for the day.")

        # Extract hour from 'Start Time' and create a new column for it
        df['hour'] = df['Start Time'].dt.hour

        # Display the most common start hour
        try:
            popular_hour = df['hour'].mode()[0]
            print('Most Popular Start Hour:', popular_hour)
        except IndexError:
            print("No data available for the hour.")

    except KeyError:
        print("The 'Start Time' column is missing from the dataset.")
    
    # Print the time it took to run the calculations
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
#--------------------------------------------------------------------
def station_stats(df): 
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    try:
        if not df['Start Station'].empty:
            start_station = df['Start Station'].value_counts().idxmax()
            print(f"Most Commonly Used Start Station: {start_station}")
        else:
            print("No data available for Start Station.")
    except KeyError:
        print("The 'Start Station' column is missing from the dataset.")

    try:
        if not df['End Station'].empty:
            end_station = df['End Station'].value_counts().idxmax()
            print(f"Most Commonly Used End Station: {end_station}")
        else:
            print("No data available for End Station.")
    except KeyError:
        print("The 'End Station' column is missing from the dataset.")

    try:
        if not df[['Start Station', 'End Station']].empty:
            most_common_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
            print(f"Most Frequent Trip: {most_common_trip[0]} -> {most_common_trip[1]}")
        else:
            print("No data available for the most frequent trip.")
    except KeyError:
        print("The 'Start Station' or 'End Station' columns are missing from the dataset.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
#-----------------------------------------------------------------------------------
def trip_duration_stats(df): #3
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # display total travel time
    print('Total travel time is:', df['Trip Duration'].sum())

    # display mean travel time
    print('Mean travel time is:', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
#------------------------------------------------------------------------------------
def user_stats(df): #4
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

     # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)
    

    # Display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print(gender)
    except KeyError:
        print("Error: 'Gender' column is not found.")
    
    # Display earliest, most recent, and most common year of birth
    try:
        earliest_birth_year = df['Birth Year'].min()
        most_recent_birth_year = df['Birth Year'].max()
        most_common_birth_year = df['Birth Year'].mode()
    
        print("\nEarliest Birth Year:", earliest_birth_year)
        print("Most Recent Birth Year:", most_recent_birth_year)
        print("Most Common Birth Year:", most_common_birth_year)
    
    except KeyError:
        print("Error: 'Birth Year' column is not found.")
    
    # Print the time taken
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
#-------------------------------------------------------------------------------
def display_data(df):
    start_row = 0

    while True:
        print(df.iloc[start_row:start_row + 5])  
        
        start_row += 5

        restart = input('\nWould you like to show another 5 rows? Enter yes or no: ').lower()
        
        if restart != 'yes':
            break
#-------------------------------------------------------------------------------
def main():
    while True:
        city, month, day = get_filters()
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