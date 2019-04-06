import pandas as pd

import numpy as np

import os

import re

from datetime import datetime

def getWhatsAppData():

        df = pd.read_csv('pulak2.csv')

        responseDictionary = dict()

        receivedMessages = df[df['name'] != personName]

        sentMessages = df[df['name'] == personName]

        combined = pd.concat([sentMessages, receivedMessages])

        otherPersonsMessage, myMessage = "",""

        firstMessage = True

        for index, row in combined.iterrows():

            if (row['name'] != personName):

                if myMessage and otherPersonsMessage:

                    otherPersonsMessage = cleanMessage(otherPersonsMessage)

                    myMessage = cleanMessage(myMessage)

                    responseDictionary[otherPersonsMessage.rstrip()] = myMessage.rstrip()

                    otherPersonsMessage, myMessage = "",""

                otherPersonsMessage = otherPersonsMessage + str(row['text']) + " "

            else:

                if (firstMessage):

                    firstMessage = False

                    # Don't include if I am the person initiating the convo

                    continue

                myMessage = myMessage + str(row['text']) + " "

        return responseDictionary


   ###############################################
def cleanMessage(message):

  # Remove new lines within message

  cleanedMessage = message.replace('\x8f',' ').lower()

  # Deal with some weird tokens

  cleanedMessage = cleanedMessage.replace("\xc2\xa0", "")

  # Remove punctuation

  cleanedMessage = re.sub('([.,!?])','', cleanedMessage)

  # Remove multiple spaces in message

  cleanedMessage = re.sub('ðÿ˜',' ', cleanedMessage)
    
  return cleanedMessage


combinedDictionary = {}





combinedDictionary.update(getWhatsAppData())

print ('Total len of dictionary', len(combinedDictionary))



print ('Saving conversation data dictionary')

np.save('conversationDictionary.npy', combinedDictionary)
np.load("conversationDictionary.npy")


conversationFile = open('conversationData.txt', 'w')

for key,value in combinedDictionary.items():

  if (not key.strip() or not value.strip()):

    # If there are empty strings

    continue

  conversationFile.write(key.strip() + value.strip())

