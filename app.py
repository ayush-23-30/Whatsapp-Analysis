import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt

# Sidebar Title
st.sidebar.title("WhatsApp Chat Analyzer")

# File uploader
uploaded_file = st.sidebar.file_uploader("Choose a file...")

if uploaded_file is None:
    st.title("Please Upload a WhatsApp Chat Export Txt file")

if uploaded_file is not None:
    with st.spinner("Processing file... Please wait ⏳"):
        # Read file as bytes and decode to text
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode("utf-8")

        # Process data
        df = preprocessor.preprocess(data)
        df["user"] = df['user'].str.strip(']')

    st.success("File uploaded and processed successfully! ✅")
    st.dataframe(df)

    # Fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.selectbox("Show chat for:", user_list)  # Moved selection to main page

    # Show Analysis Button (Now Below DataFrame)
    if st.button("Show Analysis"):
        with st.spinner("Generating analysis... ⏳"):
            num_msg, words, num_media_files, links = helper.fetch_stats(selected_user, df)

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.header("Total Messages")
                st.title(num_msg)
            with col2:
                st.header("Total Words")
                st.title(words)
            with col3:
                st.header("Total Media")
                st.title(num_media_files)
            with col4:
                st.header("Total URLs")
                st.title(links)

            # Most Busy Users
            if selected_user == 'Overall':
                st.title('Most Busy Users')
                x, new_df = helper.fetch_most_busy_users(df)

                fig, ax = plt.subplots()
                col1, col2 = st.columns(2)
                with col1:
                    ax.bar(x.index, x.values)
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)
                with col2:
                    st.header('Most Messages By:')
                    st.dataframe(new_df)

            # Word Cloud
            st.title("Word Cloud")
            df_wc = helper.create_wordcloud(selected_user, df)
            fig, ax = plt.subplots()
            ax.imshow(df_wc)
            st.pyplot(fig)

            # Most Common Words
            mst_cmn = helper.most_used_words(selected_user,df)
            st.title("Most Common Words")
            fig,ax = plt.subplots()
            ax.bar(mst_cmn[0],mst_cmn[1])
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)

            # Emoji Analysis
            emoji_df = helper.emoji_helper(selected_user, df)
            if not emoji_df.empty:
                st.title("Emoji Analysis")
                col1, col2 = st.columns(2)
                with col1:
                    st.dataframe(emoji_df)
                with col2:
                    fig, ax = plt.subplots()
                    ax.pie(emoji_df['count'].head(), labels=emoji_df['emoji'].head(), autopct='%0.2f')
                    st.pyplot(fig)