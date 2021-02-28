import re
import tkinter as tk
from tkinter import Button
from tkinter.messagebox import showinfo

import matplotlib.pyplot as plt
import pandas as pd
import tweepy
from textblob import TextBlob
from wordcloud import WordCloud


def getposts():
    # Twitter API credentials
    consumerKey = 'Your Credentials'
    consumerSecret = 'Your Credentials'
    accessToken = 'Your Credentials'
    accessTokenSecret = 'Your Credentials'

    # Create the authentication Object
    authenticate = tweepy.OAuthHandler(consumerKey, consumerSecret)

    # Set the access token and access token secret
    authenticate.set_access_token(accessToken, accessTokenSecret)

    # Create the API object while passing inthe auth information
    api = tweepy.API(authenticate, wait_on_rate_limit=True)

    # Exract 100 tweets from the twitter user
    posts = api.user_timeline(screen_name=entry.get(),
                              count=1000, Lang="en", tweet_mode="extended")
    return posts


def showrecentTweets():      # Print the recent 15 tweets from the account
    posts = getposts()
    i = 1
    s = ""
    for tweet in posts[0:15]:
        s += str(i) + ') ' + tweet.full_text + '\n'
        i = i + 1
    showinfo("Recent 15 Tweets:", s)


def cleanTxt(text):
    text = re.sub(r'@[A-Za-z0-9]+', '', text)  # Removed mentions
    text = re.sub(r'#', '', text)  # Removing the '#' Symbol
    text = re.sub(r'RT[\s]+', '', text)  # Removing RT
    text = re.sub(r'(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', '', text) # Remove the hyper link
    return text


# Create a function to get the subjectivity


def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity


# Create a function to get the polarity


def getPolarity(text):
    return TextBlob(text).sentiment.polarity


def getTweetDataFrame():
    posts = getposts()
    df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])
    df['Tweets'] = df['Tweets'].apply(cleanTxt)
    # Create two new columns
    df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
    df['Polarity'] = df['Tweets'].apply(getPolarity)
    df['Analysis'] = df['Polarity'].apply(getAnalysis)
    return df

def removeStoppers(text):
    text = re.sub(r'(ourselves | hers | between | yourself | but | again | there | about | once | during | out | very | having | with | they | own | an | be | some | for | do | its | yours | such | into | of | most | itself | other | off | is | s | d | am | or | who | as | from | him | each | the | themselves | until | below | are | we | these | your | his | through | don | nor | me | were | her | more | himself | this | down | should | our | their | while | above | both | up | to | ours | had | she | all | no | when | at | any | before | them | same | and | been | have | in | will | on | does | yourselves | then | that | because | what | over | why | so | can | did | not | now | under | he | you | herself | has | just | where | too | only | myself | which | those | i | after | few | whom | t | being | if | theirs | my | against | a | by | doing | it | how | further | was | here | than)','',text)
    return text

def getWordCloud():
    df = getTweetDataFrame()
    df['Tweets'] = df['Tweets'].apply(removeStoppers)
    allWords = ' '.join([twts for twts in df['Tweets']])
    wordCloud = WordCloud(width=500, height=300, random_state=21,
                          max_font_size=119).generate(allWords)
    plt.imshow(wordCloud, interpolation="bilinear")
    plt.axis('off')
    plt.show()


def getAnalysis(score):
    if score < 0:
        return 'Negative'
    elif score == 0:
        return 'Neutral'
    else:
        return 'Positive'


def plotPolaritySubjectivity():
    df = getTweetDataFrame()
    plt.figure(figsize=(8, 6))
    for i in range(0, df.shape[0]):
        plt.scatter(df['Polarity'][i], df['Subjectivity'][i], color='Blue')
    plt.title('Sentiment Analysis')
    plt.xlabel('Polarity')
    plt.ylabel('Subjectivity')
    plt.show()


def plotSentiments():
    df = getTweetDataFrame()
    # Get the percentage of positive tweets
    ptweets = df[df.Analysis == 'Positive']
    ptweets = ptweets['Tweets']

    round((ptweets.shape[0] / df.shape[0]) * 100, 1)

    # Get the percentage of negative tweets
    ntweets = df[df.Analysis == 'Negative']
    ntweets = ntweets['Tweets']

    round((ntweets.shape[0] / df.shape[0]) * 100, 1)

    # Show the value counts

    df['Analysis'].value_counts()

    # plot and visualize the counts
    plt.title('Sentiment Analysis')
    plt.xlabel('Sentiment')
    plt.ylabel('Counts')
    df['Analysis'].value_counts().plot(kind='bar')
    plt.show()

def plotPieChart():
    df = getTweetDataFrame()
    my_labels = 'Positive Tweets','Neutral Tweets','Negative Tweets'
    my_colors = ['green','yellow','red']
    my_explode = (0, 0.1, 0)
    plt.pie(df['Analysis'].value_counts(),labels=my_labels,autopct='%1.1f%%',startangle=15, shadow = True, colors=my_colors, explode=my_explode)
    plt.title('Analysis of Tweets')
    plt.axis('equal')
    plt.show()

def showPositiveTweets():
    df = getTweetDataFrame()
    j = 1
    s = ""
    sortedDF = df.sort_values(by=['Polarity'])
    for i in range(0, sortedDF.shape[0]):
        if sortedDF['Analysis'][i] == 'Positive':
            s += str(j) + ') ' + sortedDF['Tweets'][i] + '\n'
            j = j + 1
    showinfo("Showing all Positive tweets:", s)


def showNegativeTweets():
    df = getTweetDataFrame()
    j = 1
    s = ""
    sortedDF = df.sort_values(by=['Polarity'], ascending='False')
    for i in range(0, sortedDF.shape[0]):
        if sortedDF['Analysis'][i] == 'Negative':
            s += str(j) + ') ' + sortedDF['Tweets'][i] + '\n'
            j = j + 1
    showinfo("Showing all Negative tweets:", s)

def showNeutralTweets():
    df = getTweetDataFrame()
    k = 1
    s = ""
    sortedDF = df.sort_values(by=['Polarity'])
    for i in range(0, sortedDF.shape[0]):
        if sortedDF['Analysis'][i] == 'Neutral':
            s += str(k) + ') ' + sortedDF['Tweets'][i] + '\n'
            k = k + 1
    showinfo("Showing all Neutral tweets:", s)

def positivePercentage():
    df = getTweetDataFrame()
    ptweets = df[df.Analysis == 'Positive']
    ptweets = ptweets['Tweets']

    perc = round((ptweets.shape[0] / df.shape[0]) * 100, 1)
    showinfo("Percentage of Positive Tweets:", perc)


def negativePercentage():
    df = getTweetDataFrame()
    ntweets = df[df.Analysis == 'Negative']
    ntweets = ntweets['Tweets']

    neg = round((ntweets.shape[0] / df.shape[0]) * 100, 1)
    showinfo("Percentage of Negative Tweets:", neg)

def neutralPercentage():
    df = getTweetDataFrame()
    neutweets = df[df.Analysis == 'Neutral']
    neutweets = neutweets['Tweets']

    neutra = round(  (neutweets.shape[0] / df.shape[0]) *100 , 1)
    showinfo("Percentage of Neutral Tweets:", neutra)

w = tk.Tk()
w.configure(background="#000000")
w.title("Twitter Sentiment Analysis")
w.geometry("1000x1000")
tk.Label(w, text="Twitter Username (Handle):",bg='#ff8080',width = 30,height = 1, font=('Helvetica',15)).place(relx = 0.5, rely = 0.2, anchor = 'center')
entry = tk.Entry(w, width = 25, font=('Helvetica',17))

b1 = Button(w, text="Search", command=showrecentTweets,
            fg='black', bg='#ffff66',height=2, width=20,font=('Helvetica',12))
b1.place(x=700, y=300)

b2 = Button(w, text="Positive Percentage",
            command=positivePercentage, fg='black', bg='#ff9900',height=2,width=20,font=('Helvetica',12))
b2.place(x=100, y=400)

b3 = Button(w, text="Plot Sentiments",  
            command=plotSentiments, fg='black', bg='#ff66b3',height=2, width=20,font=('Helvetica',12))
b3.place(x=170, y=500)

b4 = Button(w, text="Negative Percentage",  
            command=negativePercentage, fg='black', bg='#ff1aff',height=2,width=20,font=('Helvetica',12))
b4.place(x=500, y=400)

b5 = Button(w, text="Negative Tweets",
            command=showNegativeTweets, fg='black', bg='#ff704d',height=2, width=20,font=('Helvetica',12))
b5.place(x=500, y=300)

b6 = Button(w, text="Positive Tweets", 
            command=showPositiveTweets, fg='black', bg='#00ff00',height=2, width=20,font=('Helvetica',12))
b6.place(x=100, y=300)

b7 = Button(w, text="Neutral Tweets", 
            command=showNeutralTweets, fg='black', bg='#66e0ff',height=2, width=20,font=('Helvetica',12))
b7.place(x=300, y=300)

b8 = Button(w, text="Word Cloud",
            command=getWordCloud, fg='black', bg='#00ccff',height=2, width=20,font=('Helvetica',12))
b8.place(x=700, y=400)

b9 = Button(w, text="Neutral Percentage", 
            command= neutralPercentage, fg='black', bg='#ffff00',height=2, width=20,font=('Helvetica',12))
b9.place(x=300, y=400)

b10 = Button(w, text="Plot Polarity Subjectivity", 
            command=plotPolaritySubjectivity, fg='black', bg='#ff471a',height=2, width=20,font=('Helvetica',12))
b10.place(x=650, y=500)

b11 = Button(w, text="Show Pie Chart",
            command=plotPieChart, fg='black', bg='#3333ff',height=2, width=22,font=('Helvetica',12))
b11.place(x=400, y=500)



entry.bind("<Return>", showrecentTweets)
entry.pack(padx=5, pady=200, side=tk.TOP)
w.mainloop()

