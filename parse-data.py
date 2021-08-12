import pandas as pd
import datetime
import os

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


mostCommon = df.Message.value_counts().head(10)
mostCommon = pd.DataFrame(mostCommon)

print(mostCommon)
