from pytg import Telegram
from pytg.exceptions import NoResponse
from database import database

import configs
import time


db = database()

class Checker:
     def __init__(self):
         tg = Telegram(
         telegram="./tg/bin/telegram-cli",
         pubkey_file="./tg/tg-server.pub")
         self.sender = tg.sender

     def check_a_number(self, phonenumber):
        result = {
            'phone' : phonenumber,
            'registered' : "NULL",
            'chat_id' : "NULL",
            'username' : "NULL",
            'check_time' : "NULL",
            'error_on_get' : "NULL"}
        try:
            res = self.sender.contact_add(phonenumber, "check", "contact")
            result['check_time'] = time.ctime() # save the time that number checked
            if res == []: # not registered
                result['registered'] =  "False"

            elif len(res)>= 1: # user registered on telegram
                print((res))
                r = res[0]
                result['registered'] = "True"
                result['chat_id'] = r.peer_id
                if hasattr(r, 'username'):
                    result['username'] = r.username
        except NoResponse:
            print("CLI did not responded in time")
            result['error_on_get'] = "No respond error"

        return result
     def check_range(self, area_code, start_range, end_range):
        start = start_range
        end   = end_range + 1
        for x in range(start, end):
            phone = area_code + str(x)[1:7]
            time.sleep(configs.timout_to_next) # time out
            result = self.check_a_number(phone)
            if result['error_on_get'] == "NULL": # there is no error
                db.save(
                    result['phone'],
                    result['registered'],
                    result['chat_id'],
                    result['username'],
                    result['check_time']
                )
                print("the " + result['phone'] + " checked and saved to database");
            else:
                # guess telegram banned us
                # so sleep for a while
                print("Warning: it seems we are banned from telegram server!")
                print("wait for a moments...")
                time.sleep(configs.timeout_on_no_res)


        print("checking loop ended.")
