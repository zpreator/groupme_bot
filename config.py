from groupy.client import Client
import pandas as pd


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
    setFavNum(messages_df)
    messages_df.to_csv('data.csv')
    return messages_df
    

def readKeys():
    vars = os.getenv('KEYS').split(',')
    keys['access_token'] = vars[0]
    return keys

