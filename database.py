import pymysql
import time
import configs

# database table schema is like below #
#######################################
#  `phonenumber` VARCHAR(20) NULL,
#  `isRegistered` TINYINT NULL,
#  `chat_id` VARCHAR(45) NULL,
#  `username` VARCHAR(45) NULL,
#  UNIQUE INDEX `id_UNIQUE` (`id` ASC));
db = pymysql.connect(host=configs.host,    # your host, usually localhost
                     user=configs.db_user,         # your username
                     passwd=configs.db_password,     # your password
                     db=configs.db_name)        # name of the data base
cursor = db.cursor()
class database:
    def save(self, phonenumber, isRegistered, chat_id, username, check_time):
        sql = "INSERT INTO " + configs.db_name + "." + configs.table_name + " (`phonenumber`, `registered`, `chat_id`, `username`, `time`) VALUES( %s, %s, %s, %s, %s);"
        cursor.execute(sql, (phonenumber, isRegistered, chat_id, username, check_time))
        db.commit()
