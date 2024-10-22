import re
import pandas as pd

def preprocess(data):
    # Define pattern to split messages
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s*[AP]M\s*-\s'

    # Split messages and dates based on the pattern
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # Create DataFrame
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Convert message_date to datetime
    df['message_date'] = pd.to_datetime(df['message_date'], format="%m/%d/%y, %I:%M %p - ")

    users = []
    messages = []

    # Loop through user messages
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # If the message has a user
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:  # If it's a group notification
            users.append('group_notification')
            messages.append(entry[0])

    # Assign users and messages after processing all rows
    df['user'] = users
    df['message'] = messages

    # Drop the user_message column
    df.drop(columns=['user_message'], inplace=True)

    # Extract additional date information
    df['year'] = df['message_date'].dt.year
    df['month_num'] = df['message_date'].dt.month
    df['month'] = df['message_date'].dt.month_name()
    df['date'] = df['message_date'].dt.day
    df['hour'] = df['message_date'].dt.hour
    df['day_name'] = df['message_date'].dt.day_name()
    df['minute'] = df['message_date'].dt.minute
    df['only_date'] = df['message_date'].dt.date
    
    return df
