from groupy.client import Client
import pandas as pd
import os


def create_groupme_api():
    keys = readKeys()
    groupme_key = keys['access_token']
    client = Client.from_token(groupme_key)
    groups = list(client.groups.list_all())
    for group in groups:
        print(group.name)
        if group.name == 'Large Fry Larrys':
            lfl = group
    return lfl


def getAllMessages(group):
    print('Getting all messages, this will take a minute...')
    messageData = []
    for message in group.messages.list_all():
        messageData.append(message.data)

    messages_df = pd.DataFrame.from_dict(messageData, orient='columns')
    messages_df = messages_df[messages_df['sender_type'] == 'user']  # Filters out groupme stuff
    list_to_delete = ['GroupMe', 'Zach  Preator', 'Zach Preator 2', 'Donald J. Trump', 'John Cena',
                      'Shad Karlson, a liberal']
    df_to_delete = messages_df[messages_df['name'].isin(list_to_delete)].index
    messages_df = messages_df.drop(df_to_delete)
    # setFavNum(messages_df)
    messages_df.to_csv('data.csv')
    return messages_df
    
def getRandomMeme(messages_df, min_likes=0):
    if min_likes == None:
        min_likes = 0
    attach_df = messages_df[messages_df['attachments'].map(len) > 0]
    attach_df = attach_df[attach_df['fav_num'] >= min_likes]
    loop = True
    while loop:
        rand = attach_df.sample()
        row = rand.iloc[0]
        attachments = row['attachments'][0]
        try:
            url = attachments['url']
            loop = False
        except:
            loop = True
    if pd.isna(row['text']):
        text = ''
    else:
        text = '"' + str(row['text']) + '"'
    user = row['name']
    avatar = row['avatar_url']
    return url, user, avatar, text

def readKeys():
    keys = {}
    vars = os.getenv('KEYS').split(',')
    keys['access_token'] = vars[0]
    return keys

