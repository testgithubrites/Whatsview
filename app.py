import streamlit as st # type: ignore
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns # type: ignore
st.sidebar.title("Whatsview")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)

    st.dataframe(df)
    user_list = df['user'].unique().tolist()  #Accesses the 'user' column in the DataFrame df#unique(): This method returns the unique values present in the 'user' column. It returns a NumPy array containing only the distinct values (no duplicates).#tolist(): Converts the NumPy array returned by .unique() into a Python list.
    user_list.remove('group_notification') #removed group notification as working on users only.
    user_list.sort()
    user_list.insert(0,"Overall")  # For group analysis

    selected_user = st.sidebar.selectbox("Show analysis w.r.t", user_list)

    if st.sidebar.button("Show Analysis"):
        num_messages,words,num_media_messages,num_links = helper.fetch_stats(selected_user,df)
        
        st.title("Top Statistics")
        
        col1,col2,col3,col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links shared")
            st.title(num_links)
            
        #Timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'],color='red')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        #Daily Timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        
        # activity map
        st.title('Activity Map')
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

    #Finding the most busy users
        if selected_user == 'Overall':
            st.title("Most Busy Users")
            x,new_df= helper.fetch_most_busy_users(df)
            fig,ax = plt.subplots()
            col1 , col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x.values,color='purple')
                plt.xticks(rotation='vertical')
                plt.show()
                st.pyplot(fig)
                st.set_option('deprecation.showPyplotGlobalUse', False)
            with col2:
                st.dataframe(new_df, height=400, width=400, use_container_width=True)
        st.title('Wordcloud')
        df_wc=helper.word_cloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
        
    #Emoji Analysis
        emoji_df = helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")
        col1,col2 = st.columns(2)
        # Create explode array
        explode = [0.1] * len(emoji_df)  # Adjust the value to move each slice outward
        with col1:
            st.table(emoji_df.T)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df['count'], labels=emoji_df['emoji'], autopct='%.2f')
            ax.axis('equal')  # Equal aspect ratio ensures that pie chart is a circle.
            plt.title("Emoji Distribution")
            st.pyplot(fig)  # Display the plot in Streamlit
        
       