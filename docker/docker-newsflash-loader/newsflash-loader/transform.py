# -*- coding: utf-8 -*-
import types
import json
import base64
import email
import time
import quopri
from datetime import datetime


def mboxToJsonList(mBoxData):
    """
    :param mBoxData: containing the mbox data
    :return: a list of jsons representing the data in the mbox
    """
    message_list = []
    for message in mBoxData:

        content = getMessageContent(message)

        if(content is not None):
            message_list.append(generateJSON(subject=message['subject'], formattedtimestamp=message['date'], unixtimestamp=dateToUnix(message['date']), fromsender=message['from'], content=content))


    return message_list


def getMessageContent(message):
    content = None
    if message.is_multipart():
        # get only first content and ignore html and binary attatchment

        payl = message.get_payload()

        while not isinstance(payl, types.StringType):

            if isinstance(payl, list):
                payl = payl[0].get_payload()
            else:
                print "type is not list nor String"
                print type(payl)
                return

        content = payl

    else:
        content = message.get_payload()


    return content

def generateJSON(subject, formattedtimestamp, unixtimestamp, content, fromsender):
    gjson = json.dumps({"subject": subject,
                        "formatted_timestamp": formattedtimestamp,
                        "unix_timestamp": unixtimestamp,
                        "from": fromsender,
                        "content": content},
                       separators=(",", ": "))

    return gjson

def dateToUnix(date):
    #convert date format 'Fri, 2 Nov 2007 17:46:37 +0100'
    date = date[:-6]
    datetime_object = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S')

    unixtimestamp = "" + str(time.mktime(datetime_object.timetuple()))
    unixtimestamp = unixtimestamp[:-2]
    return unixtimestamp




def gmailToJsonList(gmailData):
    """
    :param gmailData: data as it is returned by the gmail api in raw
    :return: a list of jsons representing this emails
    """

    message_list =[]

    historyIds = []

    for data in gmailData:

        if data['historyId'] in historyIds:
            #do not add same message again just because its history has changed
            continue

        #decode binary data
        decoded_data = base64.urlsafe_b64decode(data['raw'].encode('ASCII'))
        #data is not yet utf 8 encoded
        decoded_data = decoded_data.decode('iso-8859-1')


        #generate the message object
        message = email.message_from_string(decoded_data)

        if "inovex" not in message['subject'] or "newsflash" not in message['subject']:
            #filter for only inovex emails and ignore all the google mails and spam
            continue


        content = getMessageContent(message)
        #content is in print format



        if content is not None:

            content = quopri.decodestring(content)

            message_list.append(generateJSON(subject=message['subject'], formattedtimestamp=message['date'],
                                             unixtimestamp=data['internalDate'][:-3], fromsender=message['from'],
                                             content=content))

        else:
            print "content is None"
            print type(data)

        historyIds.append(data['historyId'])



    return message_list
