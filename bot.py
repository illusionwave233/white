from pytg.sender import Sender
from pytg.receiver import Receiver  # get messages
from pytg.exceptions import NoResponse
from pytg.utils import coroutine
import re
import time
from database import database
sender = Sender("127.0.0.1", 4458)
receiver = Receiver("127.0.0.1", 4458)

db = database()

@coroutine
def checker(t,sender):
    quit = False
    try:
        while not quit:  # loop for messages
            msg = (yield)  # it waits until the generator has a has message here.
            sender.status_online()
            print(msg)
            if msg.event != "message":
                continue  # is not a message.
            if msg.own:   # the bot has send this message.
                continue  # we don't want to process this message.
            if msg.text is None:  # we have media instead.
                continue  # and again, because we want to process only text message.
            phone = re.match("^[+](?=\d)\d{12}",msg.text)
            if phone is not None:
                r = t.check_number(phone.group(0))
                if (r == None) or (r == False) :
                    sender.send_msg(msg.sender.cmd, str(phone.group(0)) + " no telegram")
                    db.save(str(phone.group(0)), "False", "NULL", "NULL")
                else:
                    reply_msg =  "phone: " + str(r.phone) + "\n"
                    phonenumber = str(r.phone)
                    if (hasattr(r, 'peer_id')):
                        reply_msg += "chat_id: " + str(r.peer_id) + "\n"
                        chat_id = str(r.peer_id)
                    else:
                        reply_msg += "chat_id: no chat id\n"
                        chat_id = "NULL"
                    if(hasattr(r, 'username')):
                        reply_msg += "username: @" + str(r.username) + "\n"
                        username = str(r.username)
                    else:
                        reply_msg += "username: no username \n"
                        username = "NULL"
                    sender.send_msg(msg.sender.cmd, reply_msg )
                    db.save(phonenumber,"True", chat_id, username)
    except GeneratorExit:
        # the generator (pytg) exited (got a KeyboardIterrupt).
        pass
    except KeyboardInterrupt:
        # we got a KeyboardIterrupt(Ctrl+C)
        pass
    else:
        # the loop exited without exception, becaues _quit was set True
        pass

class Teleg:
    def check_number(self,phone):
        fname = "checking"
        lname = "bot"
        result = []
        try:
            result = sender.contact_add(phone, fname, lname)
        except NoResponse:  # from pytg.exceptions import NoResponse
            print("CLI did not responded in time")
            return None

        if result == [] :
            # not registered
            return False
        elif len(result) >= 1: # user exist
            return result[0]
        else:
            return None
    def startBot(self):
        receiver.start()
        receiver.message(checker(self,sender))
