import vk
import sys
import time
import datetime

interval = 5
groupId = "creativestudioleonidromanychev"
accessToken = '9af0e676dbcdef9e972ef57ad602d91c582afe98bb82b4671b1765a5dcc296a82dc5a02f7f27a641f4aea'
sendTo = [172338740]

session = vk.Session(accessToken)
vk_api = vk.API(session)

groupName = vk_api.groups.getById(group_id=groupId, fields='name', version='5.74')[0]['name']

print('OK, \'' + groupName + '\' is found')

print('Initializing members list...')
members = set(vk_api.groups.getMembers(group_id = groupId, version='5.74')['users'])
print('OK, ' + str(len(members)) + ' members are initialized')

while 1:
    message = datetime.datetime.today().strftime('%d %b %H:%M:%S') + ': '
    lastMembers = set(vk_api.groups.getMembers(group_id = groupId, version='5.74')['users'])
    message += str(len(lastMembers)) + ' subscribers, '
    if members == lastMembers:
        message += 'no changes'
    else:
        newMembers = set()
        unsubscribed = set()
        for user in members:
            if not user in lastMembers:
                unsubscribed.add(user)
        for user in lastMembers:
            if not user in members:
                newMembers.add(user)
        if len(newMembers)>0:
            message += str(len(newMembers)) + ' people subscribed'
        if len(unsubscribed)>0:
            if len(newMembers)>0:
                message += ', '
            message += str(len(unsubscribed)) + ' people unsibscribed'
        newUsers = vk_api.users.get(user_ids = newMembers, version='5.74')
        for user in newUsers:
            message += '\n+ ' + str(user['uid']) + ' ' + user['first_name'] + ' ' + user['last_name']
            for msgTo in sendTo:
                vk_api.messages.send(user_id = msgTo, message=groupName+': *id' + str(user['uid']) + ' ('+ user['first_name'] + ' ' + user['last_name'] +') subscribed', version='5.74')
        unUsers = vk_api.users.get(user_ids = unsubscribed, version='5.74')
        for user in unUsers:
            message += '\n- ' + str(user['uid']) + ' ' + user['first_name'] + ' ' + user['last_name']
            for msgTo in sendTo:
                vk_api.messages.send(user_id = msgTo, message=groupName+': *id' + str(user['uid']) + ' ('+ user['first_name'] + ' ' + user['last_name'] +') unsubscribed', version='5.74')
    print(message)
    members = lastMembers
    time.sleep(interval)
