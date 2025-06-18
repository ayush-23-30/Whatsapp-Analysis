# import emoji.unicode_codes
from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd 
from collections import Counter
import emoji 

extrator = URLExtract()

def fetch_stats (selected_user,df):

  if selected_user != "Overall":
    df = df[df['user'] == selected_user] ## df change karr diya hai 

    # fetch number of messages 

  num_msg =  df.shape[0]

  # number of words 

  words = []
  for msg in df['message']:
    words.extend(msg.split())

## Media files 
  num_media_files = df[df['message'].str.contains("omitted")].shape[0]

  ## URL  Extract
  links = []
  for msg in df['message']:
    links.extend(extrator.find_urls(msg))

  return num_msg, len(words), num_media_files, len(links)

def fetch_most_busy_users (df):
  x = df['user'].value_counts().head()
  new_df = round((df['user'].value_counts() / df.shape[0]) * 100 ,2 ).reset_index().rename(columns = {'index' : 'name', 'user' : 'percent'})
  return x , new_df

def create_wordcloud(selected_user, df):
  if selected_user != 'Overall':
    df = df[df['user'] == selected_user]
  
  wc = WordCloud(width=500, height= 500, min_font_size=10, background_color='white')
  df_wc = wc.generate(df['message'].str.cat(sep = " "))  
  return df_wc


def most_used_words (selected_user,df):
  f = open('stop_hinglish.txt','r')
  stop_words = f.read()
  if selected_user != 'Overall':
      df = df[df['user'] == selected_user]

  temp = df[df['user'] != 'group_notification']
  temp = temp[~temp['message'].str.contains("omitted")]
  temp['message'] = temp['message'].str.replace(r'[\[\]]', '', regex=True)
  

  words =[]
  for msg in temp['message']:
    for word in msg.lower().split():
      if word not in stop_words:
        words.append(word)
  
 
  
  most_common_df = pd.DataFrame(Counter(words).most_common(20))

  return most_common_df

# import emoji
# from collections import Counter
# import pandas as pd

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for msg in df['message']:
        emojis.extend([c for c in msg if c in emoji.EMOJI_DATA])  # Correct method

    emoji_df = pd.DataFrame(Counter(emojis).most_common(), columns=['emoji', 'count'])
    return emoji_df


