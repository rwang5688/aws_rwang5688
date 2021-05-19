import json
import sqsutil


def receive_task_message(queue_name):
    # get queue url
    queue_url = sqsutil.get_queue_url(queue_name)
    if queue_url is None:
        print('receive_task_message: %s does not exist.' % queue_name)
        return None

    # receive message
    message = sqsutil.receive_message(queue_url)
    if message is None:
        print('receive_task_message: cannot retrieve message.')
        return None

    # success
    return message


def get_task_from_message(message):
    # get message body
    message_body = eval(message['Body'])
    if message_body is None:
        print('receive_task_message: message body is missing.')
        return None

    # get task
    task = message_body['task']
    if task is None:
        print('receive_task_message: task is missing.')
        return None

    # success
    return task


def delete_task_message(queue_name, message):
    # get queue url
    queue_url = sqsutil.get_queue_url(queue_name)
    if queue_url is None:
        print('delete_task_message: %s does not exist.' % queue_name)
        return False

    # delete message
    sqsutil.delete_message(queue_url, message)
    return True


def send_task_message(queue_name, action, task):
    # get queue url
    queue_url = sqsutil.get_queue_url(queue_name)
    if queue_url is None:
        print('send_task_message: Queue %s does not exist.' % queue_name)
        return False

    # assume user_id and task_id are set
    message_body = {}
    message_body['action'] = action
    message_body['task'] = task

    # send message as json
    message_body_json = json.dumps(message_body)
    message_id = sqsutil.send_message(queue_url, message_body_json)
    print('MessageId: %s' % message_id)
    print('MessageBodyJSON: %s' % message_body_json)

    # # debug: receive message
    # message = sqsutil.receive_message(queue_url)
    # if message is None:
    #     print('send_task_message: cannot retrieve sent message.')
    #     print('(When downstream Lambda function is running, missing message is expected.)')
    # else:
    #     print('Received message:')
    #     print(message)

    # success
    return True

