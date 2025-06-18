import streamlit as st 
import preprocessor,helper
import matplotlib.pyplot as plt

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file ...")

# f = open('D:\ml-Project\chat-analysis\_chat.txt', 'r', encoding = 'utf-8')

# data = f.read()
  
# if data:
# ----- uncomment this code 

if uploaded_file is None :
    st.title("Please Upload a Whatsapp Chat Export Txt files")

if uploaded_file is not None:
  # to read file as a bytes :
  bytes_data = uploaded_file.getvalue()
  data = bytes_data.decode("utf-8")

  df = preprocessor.preprocess(data)  
  df["user"] =  df['user'].str.strip(']')
  
  st.dataframe(df)
  ## Fetch unique Users 
  user_list  = df['user'].unique().tolist()
  user_list.remove("group_notification")
  user_list.sort()
  user_list.insert(0,"Overall")
  selected_user = st.sidebar.selectbox("Show Chats person ", user_list)

  if st.sidebar.button("Show Analysis"): 
    num_msg , words , num_media_files,links= helper.fetch_stats(selected_user,df)
    
    col1,col2,col3,col4 = st.columns(4)

    with col1 :
      st.header("Total Message")
      st.title(num_msg)
    with col2 :
      st.header("Total Words")
      st.title(words)
    with col3 :
      st.header("Total Media")
      st.title(num_media_files)
    with col3 :
      st.header("Total Urls")
      st.title(links)
    
    if selected_user == 'Overall':
      st.title('Most Busy Users')
      x,new_df = helper.fetch_most_busy_users(df)
      # print('hbjb',x)
      fig, ax = plt.subplots()
      
      col1, col2 = st.columns(2)
      with col1 :
        ax.bar(x.index, x.values)
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)
      with col2 :
        st.header('Most Messages By ')
        st.dataframe(new_df)
      
      st.title("Word Cloud")
      df_wc = helper.create_wordcloud(selected_user,df)
      fig,ax  = plt.subplots()
      ax.imshow(df_wc)
      st.pyplot(fig)

      ## Most Common words 
      mst_cmn = helper.most_used_words(selected_user,df)
      st.title("Most Common Words")
      fig,ax = plt.subplots()
      ax.bar(mst_cmn[0],mst_cmn[1])
      plt.xticks(rotation = 'vertical')
      st.pyplot(fig)
      # st.dataframe(mst_cmn) 

      ## Emoji Analysis 
      emoji_df = helper.emoji_helper(selected_user,df)
      if len(emoji_df) !=0:
        st.title("Emoji Analysis")

        col1,col2 = st.columns(2)
        with col1 :
          st.dataframe(emoji_df)
        with col2 : 
          fig, ax = plt.subplots()
          ax.pie(emoji_df['count'].head(), labels=emoji_df['emoji'].head(), autopct='%0.2f')
          st.pyplot(fig)
  



