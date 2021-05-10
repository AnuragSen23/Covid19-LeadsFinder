import warnings
warnings.filterwarnings('ignore')
import tweepy
import pandas as pd
pd.set_option('display.max_colwidth', -1)
import streamlit as st
from PIL import Image
import os

consumer_key = "Enter consumer_key"
consumer_sec = "Enter consumer_sec"

access_token = "Enter access_token"
access_token_sec = "Enter access_token_sec"

auth=tweepy.OAuthHandler(consumer_key,consumer_sec)
auth.set_access_token(access_token,access_token_sec)

api=tweepy.API(auth)

image = Image.open(os.path.join('image_dem.jpg'))
st.image(image)
st.title('COVID19 - LeadsFinder')
st.write("LIVE! Twitter data based on location, requirement and availability of leads is scraped to provide instant assistance. Contact details (Phone Number) and location can be retrieved. Do redirect to the tweets using the links generated for more details.")
'-------------------------------------------------------------'
try:
    location = st.text_input("Enter your location (India): ")
    commodity, cause = st.beta_columns(2)
    commodity = commodity.selectbox("Your Requirement: ",("Oxygen","Plasma","Remdesivir","ICU","Tocilizumab","Ventilator","Hospital Beds"))
    cause = cause.selectbox("Available / in Need? ",("Available","Need"))
    st.write("If no record is retrieved from your exact location, try the nearest city from your location.")

    st.markdown("**➡ Searching Leads: **" + location + " " + commodity + " " + cause)

    verified = st.checkbox("Verified resource search ✅")
    if st.button('Search'):

        if (commodity == "Oxygen" or commodity == "Remdesivir" or commodity == "Ventilator" or commodity == "ICU" or commodity == "Hospital Beds" or commodity == "Plasma"):
            input_data = location + " " + commodity + " " + cause
        if commodity == "Tocilizumab":
            input_data = "Tocilizumab"

        if verified:
            input_data = location + " " + commodity + " " + cause + " " + "Verified" + " "  + "✅"


        data = tweepy.Cursor(api.search, q = input_data , tweet_mode = "extended").items(50)

        tweets = []
        time = []
        a = []
        name = []
        string = "https://twitter.com/twitter/statuses/"

        for i in data:
            tweets.append(i.full_text)
            time.append(i.created_at)
            a.append(i.id)
            name.append(i.user.name)
        a = map(str,a)

        list2 = ['https://twitter.com/twitter/statuses/%s' % (x,) for x in a]


        tweets = [t.replace('\n','. ') for t in tweets]


        df1 = pd.DataFrame({'Name':name,'Tweets':tweets,'Date':time})
        df2 = pd.DataFrame({'Date':time,'Tweets':tweets,'Name':name,'Link':list2})

        #Tweetdata1 = df1.set_index('Name')
        Tweetdata2 = df2.set_index('Date')

        Tweetdata2 = Tweetdata2.reset_index()
        st.table(df1.head(25))


        try:
            st.markdown("**Tweet Source:**")
            st.table(st.markdown(Tweetdata2['Link']))
        except TypeError:
            pass

        # res = Tweetdata.drop(['Date','Tweets'],axis=1)
        # res = res.reset_index()
        # try:
        #     st.markdown("**Tweet Source:**")
        #     st.table(st.markdown(res['Link']))
        # except TypeError:
        #     pass
    else:
        pass
    st.warning("This app scraps live twitter data by keyword search, thus I am not responsible for it's authenticity.✌️")
    st.info("For Feedbacks and suggestion, drop a message on my LinkedIn😃:  [Anurag Sen](https://www.linkedin.com/in/anurag-sen-aa36961b2/)")
    st.success("Stay Connected. Stay safe. [WHO-Covid19](https://www.who.int/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19) • [Ministry of health and family welfare](https://www.mohfw.gov.in/) • [GAVI](https://www.gavi.org/covid19?gclid=Cj0KCQjwppSEBhCGARIsANIs4p7U9Uf4QdGlKsTn1nPZjjYbwnMmFSshyqd64qbkHm0gQnoKeIR7GjEaApIhEALw_wcB)")
except KeyError:
     st.markdown("**Relevant records not found 👎**")
