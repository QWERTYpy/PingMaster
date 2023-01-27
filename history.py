import os
import datetime

def folder_exist():
    # Если папка отсутствует, то создаем её
    if not os.path.isdir("history"):
        os.mkdir("history")


def add_in_log(str_add):
    now_date = datetime.datetime.now()
    now_date = now_date.strftime("%Y-%m-%d")
    file_log = open(f"history/{now_date}.txt", 'a+')
    file_log.write(str_add+"\n")
    file_log.close()



if __name__ == '__main__':
    folder_exist()
    add_in_log("222222")