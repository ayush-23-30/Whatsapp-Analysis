import re 
import pandas as pd

def preprocess (data):
  pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}:\d{2}\s(?:AM|PM)?'

  messages = re.split(pattern, data)
  dates = re.findall(pattern, data)

  while len(messages) > len(dates):
    messages.pop()


  df = pd.DataFrame({'user_message':messages, 'message_date':dates})
  df['message_date'] = df['message_date'].str.replace('\u202f', ' ')

  df['date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %I:%M:%S %p', errors='coerce')

  df.rename(columns={'message_date':'date'}, inplace=True)
  df = df.loc[:,~df.columns.duplicated()]

  user = []
  messages = []
  for msg in df['user_message']:
    entry = re.split('([\w\W]+?):\s', msg)
    if entry[1:]: # user Name
      user.append(entry[1])
      messages.append(entry[2])
    else:
      user.append('group_notification')
      messages.append(entry[0])

  df['user'] = user
  df['message'] = messages
  df.drop(columns=['user_message'], inplace=True)
  # Replace non-breaking space with a regular space
  df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y, %I:%M:%S %p', errors='coerce')

  df['only_date'] = df['date'].dt.date
  df['year'] = df['date'].dt.year
  df['month_num'] = df['date'].dt.month
  df['month'] = df['date'].dt.month_name()
  df['day'] = df['date'].dt.day
  df['day_name'] = df['date'].dt.day_name()
  df['hour'] = df['date'].dt.hour
  df['minute'] = df['date'].dt.minute

  period = []
  for hour in df[['day_name', 'hour']]['hour']:
      if hour == 23:
          period.append(str(hour) + "-" + str('00'))
      elif hour == 0:
          period.append(str('00') + "-" + str(hour + 1))
      else:
          period.append(str(hour) + "-" + str(hour + 1))
  df['period'] = period
  
  return df 



# preprocess("[07/02/25, 8:52:51 PM] Aditya Gym Trainer : Messages and calls are end-to-end encrypted. Only people in this chat can read, listen to, or share them. [07/02/25, 8:52:51 PM] Ayush💖: video omitted [17/04/25, 2:19:58 PM]")