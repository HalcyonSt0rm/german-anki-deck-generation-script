import requests
from bs4 import BeautifulSoup
import genanki
import os
from gtts import gTTS
from time import sleep

# requests

URL = 'https://1000mostcommonwords.com/1000-most-common-german-words/'
page = requests.get(URL)

# beautifulsoup

soup = BeautifulSoup(page.content, "html.parser")
wordslist = soup.find_all('td')

# lists for scraped words

english = []
deutsch = []
doNotInclude = ['Number', 'German', 'in English']

# indices

i = 1
noteIndex = 0

# ANKI ID #'s

MODEL_ID = 1886936494
DECK_ID = 1978128349

# card formatting

CARD_CSS = """.card {
 font-family: Roboto, sans-serif;
 font-size: 20px;
 text-align: center;
}
"""
            
# initialize the model for our note cards 

basic = genanki.Model(
  MODEL_ID,
  'Simple Model',
  fields=[
    {'name': 'Question'},
    {'name': 'Answer'},
    {'name': 'MyMedia'},
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': '{{Question}}<br>{{MyMedia}}',
      'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
    },
  ],
  css=CARD_CSS
  )

# initialize the deck that the note cards will be in.

deutschDeck = genanki.Deck(
  DECK_ID,
  'Deutsch 1k most frequent')

de_package = genanki.Package(deutschDeck)
de_package.media_files = list()

# parse english and german words into respective lists

for entry in wordslist:
    word = entry.text
    isInt = word.isnumeric()
    isViable = True
    for string in doNotInclude:
      if word == string or isInt == True:
        print('bypassing incompatible word \"' + word + '\"')
        isViable = False
        break
      
    if i % 2 == 0 and isViable == True:
      try:
        english.append(word)
        print('added word \"' + word + '\" to english list')
        i+=1
      except:
        print('could not add word to deutsch list')
    elif isViable == True:
      try:
        deutsch.append(word)
        print('added word \"' + word + '\" to deutsch list')
        i+=1
      except:
        print('could not add word to english list')
    else:
      continue
    



# create a card for each word pair and add it to the deck

for word in deutsch:
    media = str(word) + str(noteIndex) + '.mp3'
    try:
      print('creating tts file ' + media)
      tts = gTTS(word, lang='de')
      tts.save(media)
      print('created!')
    except:
      print('could not create TTS file')

    card = genanki.Note(
    model=basic,
    fields=[deutsch[noteIndex], english[noteIndex], '[sound:' + media + ']'])
    
    print('creating card number ' + str(noteIndex+1))
    noteIndex+=1
    try:
      de_package.media_files.append(media)
      deutschDeck.add_note(card)
      print('card ' + str(noteIndex) + ' created')
    except:
      print('could not create card')

# create an apkg file and export our deck to it.
print('creating package file...')
try:
  genanki.Package(deutschDeck).write_to_file('deutsch-1K-most-frequent.apkg')
  print('File created!')
except:
  print('could not create package file')