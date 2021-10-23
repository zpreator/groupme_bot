def run(data, bot_info, send):

    help_message = "Help:\n.help  -->  This screen\n.test  -->  Try it!\nOtherwise, repeats your message."

    message = data['text']

    if message == '.help':
        send(help_message, bot_info[0])
        return True

    if message == '.test':
        send("Hi there! Your bot is working, you should start customizing it now.", bot_info[0])
        return True

    result = check_responses('responses.txt', message)
    if result is not None:
        send(result, bot_info[0])
    return True


def check_responses(path, msg):
    with open(path, 'r') as file:
        line = file.readline()
        trigger, response = line.split(':')
        if trigger.lower() in msg.lower():
            return response
    return None