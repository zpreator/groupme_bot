import random
import markovify
import pandas as pd
from groupme_config import getAllMessages, getRandomMeme


def run(data, bot_info, group, send, send_image):
    message = data['text']

    sender = data['sender_id']
    sender_name = data['name']

    # Check if bot is sender, do exit if so (to avoid feedback loops)
    if sender == '861991':
        print('From bot')
        return True

    with open('groupme_response.txt', 'a') as file:
        file.write('{0}\n'.format(message))

    if message == '.help':
        help_message = "Help:"\
                       "\n.help   -->  This screen"\
                       "\n.test   -->  For debugging"\
                       "\n.joke   -->  Gets a Dad joke"\
                       "\n.swerve -->  Compiles a response based on chat history"
        send(help_message, bot_info[0])
        return True

    if message == '.test':
        send("Hi there! Your bot is working, you should start customizing it now.", bot_info[0])
        return True

    if message == '.details':
        send('user_id: {0} .get_bot_id'.format(str(sender)), bot_info[0])
        return True

    if message.lower() == '.joke' or message.lower() == '.jokes':
        msg = get_random_joke()
        send(msg, bot_info[0])

    if message.lower() == '.swerve':
        print('Attempting to make markov chain')
        msg = make_markov_chain()
        print(msg)
        send(msg, bot_info[0])

    if message.lower() == '.meme':
        print('Retrieving a meme')
        image_url, user = get_random_meme(group)
        print('Sending meme')
        msg = 'Sent by {0}'.format(user)
        send_image(image_url, msg, bot_info[0])
        
    if '.get_bot_id' in message:
        send('bot_id: {0}'.format(str(sender)), bot_info[0])
        return True

    # Checks all the possible triggers from responses.txt
    result = check_responses('responses.txt', message)
    if result is not None:
        send(result, bot_info[0])
        return True
    return True


def check_responses(path, msg):
    with open(path, 'r') as file:
        for line in file:
            if line[0] != '#' and line != '\n' and line != '':
                trigger, response = line.split(':')
                if trigger.lower() in msg.lower():
                    return response
    return None


def get_random_joke():
    with open('jokes.txt', 'r') as file:
        lines = file.readlines()
        index = random.randint(0, len(lines) - 1)
        selected_line = lines[index]
        return selected_line


def get_response():
    with open('markov_responses.txt', 'r') as file:
        lines = file.readlines()
        index = random.randint(0, len(lines) - 1)
        selected_line = lines[index]
        return selected_line


def make_markov_chain():
    with open('groupme_response.txt', 'r') as file:
        text = file.read()
    print('Text preview: {0}'.format(text[:100]))
    text_model = markovify.NewlineText(text)
    response = text_model.make_short_sentence(280)
    return response
    

def get_random_meme(group):
    messages_df = getAllMessages(group)
    url, user, avatar, text = getRandomMeme(messages_df, 3)
    return url, user


if __name__ == '__main__':
    # print(check_responses('responses.txt', 'mckensie'))
    print(make_markov_chain())