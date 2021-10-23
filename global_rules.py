def run(data, bot_info, send):
    count = 0
    message = data['text']

    sender = data['sender_id']

    if message == '.help':
        help_message = "Help:\n.help  -->  This screen\n.test  -->  Try it!\nOtherwise, repeats your message."
        send(help_message, bot_info[0])
        return True

    if message == '.test':
        send("Hi there! Your bot is working, you should start customizing it now.", bot_info[0])
        return True

    if message == '.details':
        count += 1
        if count > 2:
            return True
        send(str(sender) + '.details', bot_info[0])
        return True

    # Checks all the possible triggers from responses.txt
    # result = check_responses('responses.txt', message)
    # if result is not None:
    #     send(result, bot_info[0])
        # return True
    return True


def check_responses(path, msg):
    with open(path, 'r') as file:
        for line in file:
            if line[0] != '#' and line != '\n' and line != '':
                trigger, response = line.split(':')
                if trigger.lower() in msg.lower():
                    return response
    return None

if __name__ == '__main__':
    print(check_responses('responses.txt', 'mckensie'))