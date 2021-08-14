import pandas as pd
import datetime
import os
import matplotlib.pyplot as plt

cwd = os.getcwd()
print('cwd:', cwd)


# read chat
def read_file(file):
    """Reads Whatsapp text file into a list of strings"""
    x = open(file, 'r', encoding='utf-8')  # Opens the text file into variable x but the variable cannot be explored yet
    y = x.read()  # By now it becomes a huge chunk of string that we need to separate line by line
    content = y.splitlines()  # The splitline method converts the chunk of string into a list of strings
    return content


chat = read_file('_chat.txt')

names = []
messages = []
dates = []
times = []

for line in chat:
    try:
        splitLine, dateTime = line.split('] ')[1], line.split(']')[0]
        dateTime = dateTime.split('[')[1]
        date, time = dateTime.split(', ')  # date = '18/06/17'; time = '22:47'
        name, message = splitLine.split(': ')[0], splitLine.split(': ')[1]

        names.append(name)
        messages.append(message)
        dates.append(date)
        times.append(time)

    except:
        pass

df = pd.DataFrame(list(zip(dates, times, names, messages)),
                  columns=['Date', 'Time', 'Name', 'Message'])

# Create a column with length of messages (length by words)
df['Words'] = df['Message'].apply(lambda x: len(str(x).split(" ")))

# Create another column for the number of characters in messages
df['Characters'] = df['Message'].str.len()

# Drop the 'attached' rows
clean_df = df[~df['Message'].isin(['<attached', 'image omitted', 'Missed voice call'])]

mostCommon = clean_df.Message.value_counts().head(10)
mostCommon = pd.DataFrame(mostCommon)

print(mostCommon)

# Concatenate 'Date' and 'Time' columns
clean_df['Date'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])

# Convert the 'Date' column to datetime format
clean_df['Date'] = clean_df['Date'].astype('datetime64[ns]')
clean_df = clean_df.drop(columns=['Time'])

# Check the format of 'Date' column
print(clean_df.info())

# Keep only dates and word/character count
date_df = clean_df[['Date', 'Name', 'Words', 'Characters']]

# Create J & G frames
date_j = date_df[date_df['Name'].isin(['Hardonk Jomme'])]
date_g = date_df[date_df['Name'].isin(['Guillermina'])]

# Drop 'Name' columns
date_j = date_j.drop(columns=['Name'])
date_g = date_g.drop(columns=['Name'])

# Applying the groupby function on df
sumj_df = date_j.groupby(pd.Grouper(key='Date', axis=0,
                                    freq='D')).sum()

sumg_df = date_g.groupby(pd.Grouper(key='Date', axis=0,
                                    freq='D')).sum()


sumj_df.to_csv('Him.csv')
sumg_df.to_csv('Her.csv')

plot_g = pd.read_csv('Her.csv')
plot_g.plot()
plt.savefig("g.svg")
