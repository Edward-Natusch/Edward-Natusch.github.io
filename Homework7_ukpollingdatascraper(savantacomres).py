
# SavantaComres Polling Data Web Scraper

# Edward Natusch University of Bristol 2021

# Importing the required packages 

import certifi

import numpy as np

from urllib.request import Request, urlopen

import pandas as pd

import requests

from bs4 import BeautifulSoup

import os

# Using beautiful soup to read the html data from comresglobal

url = 'https://comresglobal.com/poll-category/voting-intention/'

request = Request(url , headers ={'User-Agent':'Mozilla/5.0'})

html = urlopen(request).read()

soup = BeautifulSoup(html, 'html.parser')

# Creating an array 'links' to store the links found in the html data 

links = []

for link in soup.find_all('a'):
   links.append(link.get('href'))

# Creating an array 'VotingIntentionLinks' to store all the links, which include Westminster Voting Intention data

VotingIntentionLinks= []

for i in range(0,len(links)):
  if '/westminster-voting-intention-' in links[i]:
    VotingIntentionLinks.append(links[i])
    print(links[i])

# Creating two arrays 'Polls' and 'Text' to hold 

Polls = []

Text = []

# Looping through all the Westminster Voting Intention links and storing the text data in the array 'Polls'

for i in range(0,len(VotingIntentionLinks)):
  url = (VotingIntentionLinks[i])
  request = Request(url , headers ={'User-Agent':'Mozilla/5.0'})
  html = urlopen(request).read()
  soup = BeautifulSoup(html, 'html.parser')
  soup_li = soup.find_all("div", {"class": "col-md-7"})
  Polls.append(soup_li[0].text)
  print(soup_li[0].text)

# Creating a variable a o store the length of the array 'Polls'

a = len(Polls)


# Extracting polling data for the conservative party 

count = 0
found = False

# Creating three arrays. The first stores the polling value, the second stores the date the poll was published and the third will store that these values are for the Conservatives.

Conservative_poll_values = []
Conservative_poll_dates = []
Conservative_Party = []

# For loop, loops through the text data, looking for a match for 'Con' and stores the value of the polling data in the array 'Conservative_poll_values'

# Additionally, looks for a match with 'Date Published' and stores the date in the array 'Conservative_poll_dates' 

for i in range(0,a):
  b=len(Polls[i])
  found = False
  for j in range(0,b):
    if((Polls[i][j] =='C' and Polls[i][j+1] == 'o'and Polls[i][j+2] == 'n' and Polls[i][j+3] == ' ' and Polls[i][j+4] != 'v') or (Polls[i][j] =='C' and Polls[i][j+1] == 'O'and Polls[i][j+2] == 'N' and Polls[i][j+3] != 'T')):
      print(Polls[i][j+4:j+8])
      Conservative_poll_values.append(Polls[i][j+4:j+8])
      Conservative_Party.append("Conservative")
      count = count + 1
      found = True
    
    # Following two lines commented out - Work in Progress 

    # if((found == True) and (Polls[i][j:j+11] == 'online from')):
       # print(Polls[i][j+12:j+34])
    
    # if((found == True) and (Polls[i][j:j+14] == 'online between')):
      # print(Polls[i][j+15:j+36])

    if((found == True) and (Polls[i][j:j+14] == 'Date Published')):
      Conservative_poll_dates.append(Polls[i][j+15:j+25])
  

# Doing the same for Labour 

count = 0
found = False

Labour_poll_values = []
Labour_poll_dates = []
Labour_Party = []

for i in range(0,a):
  b=len(Polls[i])
  found = False
  for j in range(0,b):
    if(Polls[i][j] == ('L') and (Polls[i][j+1] == 'A') and (Polls[i][j+2] == 'B')) or (Polls[i][j] == ('L') and (Polls[i][j+1] == 'a') and (Polls[i][j+2] == 'b') and Polls[i][j+3] == ' '):
      print(Polls[i][j+4:j+8])
      Labour_poll_values.append(Polls[i][j+4:j+8])
      Labour_Party.append("Labour")
      count = count + 1
      found = True

    if((found == True) and (Polls[i][j:j+14] == 'Date Published')):
      Labour_poll_dates.append(Polls[i][j+15:j+25])

# Inputting the scraped polling data into a table and cleaning

# Creating a data frame to store Conservative party data

df1 = pd.DataFrame([Conservative_Party,Conservative_poll_values,Conservative_poll_dates]).T
df1.columns = ['Party','Vote Percentage','Date']

# Cleaning the data

df1['Vote Percentage'] = df1['Vote Percentage'].str.replace('(',' ')
df1['Vote Percentage'] = df1['Vote Percentage'].str.replace('%',' ')
df1['Vote Percentage'] = df1['Vote Percentage'].str.replace('\n',' ')
df1['Vote Percentage'] = df1['Vote Percentage'].str.replace('-',' ')
df1['Date'] = df1['Date'].str.replace('\n',' ')

# Creating a data frame to store Labour party data

df2 = pd.DataFrame([Labour_Party,Labour_poll_values,Labour_poll_dates]).T
df2.columns = ['Party','Vote Percentage','Date']
df2['Vote Percentage'] = df2['Vote Percentage'].str.replace('(',' ')
df2['Vote Percentage'] = df2['Vote Percentage'].str.replace('%',' ')
df2['Vote Percentage'] = df2['Vote Percentage'].str.replace('\n',' ')
df2['Vote Percentage'] = df2['Vote Percentage'].str.replace('-',' ')
df2['Date'] = df2['Date'].str.replace('\n',' ')

# Sort by publishing date

df1["Date"] = pd.to_datetime(df1["Date"],dayfirst=True)
df2["Date"] = pd.to_datetime(df2["Date"],dayfirst=True)

df1.sort_values(by=['Date'], inplace=True)
df2.sort_values(by=['Date'], inplace=True)

df1.to_csv("Homework7_ConservativePartyPollingData.csv")
df2.to_csv("Homework7_LabourPartyPollingData.csv")



