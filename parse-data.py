import pandas as pd
import datetime
import os
import matplotlib.pyplot as plt
import string

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

# sumj_df.to_csv('Him.csv')
# sumg_df.to_csv('Her.csv')

# Get all punctuation marks
februari = []
mart = []
april = []
mai = []
juni = []

gfebruari = []
gmart = []
gapril = []
gmai = []
gjuni = []

clean_df_j = clean_df[clean_df['Name'].isin(['Hardonk Jomme'])]
clean_df_g = clean_df[clean_df['Name'].isin(['Guillermina'])]

for i in range(len(clean_df_j)):
    if clean_df_j.iloc[i, 0].month == 2:
        for j in clean_df_j.iloc[i, 2]:
            if j in string.punctuation:
                februari.append(j)

    if clean_df_j.iloc[i, 0].month == 3:
        for j in clean_df_j.iloc[i, 2]:
            if j in string.punctuation:
                mart.append(j)

    if clean_df_j.iloc[i, 0].month == 4:
        for j in clean_df_j.iloc[i, 2]:
            if j in string.punctuation:
                april.append(j)

    if clean_df_j.iloc[i, 0].month == 5:
        for j in clean_df_j.iloc[i, 2]:
            if j in string.punctuation:
                mai.append(j)

    if clean_df_j.iloc[i, 0].month == 6:
        for j in clean_df_j.iloc[i, 2]:
            if j in string.punctuation:
                juni.append(j)

for i in range(len(clean_df_g)):
    if clean_df_g.iloc[i, 0].month == 2:
        for j in clean_df_g.iloc[i, 2]:
            if j in string.punctuation:
                gfebruari.append(j)

    if clean_df_g.iloc[i, 0].month == 3:
        for j in clean_df_g.iloc[i, 2]:
            if j in string.punctuation:
                gmart.append(j)

    if clean_df_g.iloc[i, 0].month == 4:
        for j in clean_df_g.iloc[i, 2]:
            if j in string.punctuation:
                gapril.append(j)

    if clean_df_g.iloc[i, 0].month == 5:
        for j in clean_df_g.iloc[i, 2]:
            if j in string.punctuation:
                gmai.append(j)

    if clean_df_g.iloc[i, 0].month == 6:
        for j in clean_df_g.iloc[i, 2]:
            if j in string.punctuation:
                gjuni.append(j)


# Turn month lists into string
def tostring(s):
    str1 = " "  # initialize an empty string
    return str1.join(s)


feb, mar, apr, may, jun = tostring(februari), tostring(mart), tostring(april), tostring(mai), tostring(juni)
gfeb, gmar, gapr, gmay, gjun = tostring(gfebruari), tostring(gmart), tostring(gapril), tostring(gmai), tostring(gjuni)

# print(gfeb, '\n', gmar, '\n', gapr, '\n', gmay, '\n', gjun)


# View activity per month
month = [2, 3, 4, 5, 6]

for i in month:
    g = date_df.loc[(date_df['Date'].dt.month == i) & (date_df['Name'] == "Guillermina")]
    j = date_df.loc[(date_df['Date'].dt.month == i) & (date_df['Name'] == "Hardonk Jomme")]

    g = g.groupby(pd.Grouper(key='Date', axis=0,
                             freq='T')).sum()
    j = j.groupby(pd.Grouper(key='Date', axis=0,
                             freq='T')).sum()

    g = g.reset_index()
    j = j.reset_index()

    g.plot(x='Date', y='Characters')
    plt.savefig('g_month{}.svg'.format(i))

