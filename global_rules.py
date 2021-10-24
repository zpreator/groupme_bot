import random

def run(data, bot_info, send):
    message = data['text']

    sender = data['sender_id']
    sender_name = data['name']

    # Check if bot is sender, do exit if so (to avoid feedback loops)
    if sender == '861991':
        print('From bot')
        return True

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
        # msg = get_response()
        send('Sorry, this is still in development', bot_info[0])

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


if __name__ == '__main__':
    print(check_responses('responses.txt', 'mckensie'))