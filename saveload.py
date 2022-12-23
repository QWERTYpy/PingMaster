import configparser
from object import Object


def save_ini(dict_object):
    # Сохраняем созданные объекты в файл
    config = configparser.ConfigParser()
    for _ in dict_object.keys():
        ip_adr = dict_object[_].ip_adr
        descr = dict_object[_].descr
        ping_status = dict_object[_].ping_status
        x = dict_object[_].x
        y = dict_object[_].y
        config[f"{ip_adr}"] = {'descr': descr,
                               'x': x,
                               'y': y,
                               'ping_status': ping_status}
    with open('example.ini', 'w') as configfile:
        config.write(configfile)


def load_ini():
    # Загружаем объекты из файла
    config = configparser.ConfigParser()
    config.read('example.ini', encoding='cp1251')
    list_obj = []
    for ip_adr in config.sections():
        list_obj.append([ip_adr, config[ip_adr]['x'], config[ip_adr]['y'], config[ip_adr]['descr'],
                         (True, False)[config[ip_adr]['ping_status'] == 'False']])
    return list_obj
    # print(list_obj)


if __name__ == '__main__':
    load_ini()
