import configparser
from object import Object


def save_ini(dict_object):
    config = configparser.ConfigParser()
    for _ in dict_object.keys():
        ip_adr = dict_object[_].ip_adr
        descr = dict_object[_].descr
        x = dict_object[_].x
        y = dict_object[_].y
        config[f"{ip_adr}"] = {'descr': descr,
                               'x': x,
                               'y': y}
    with open('example.ini', 'w') as configfile:
        config.write(configfile)


def load_ini():
    config = configparser.ConfigParser()
    config.read('example.ini')
    list_obj = []
    for ip_adr in config.sections():
        list_obj.append([ip_adr, config[ip_adr]['x'], config[ip_adr]['y'], config[ip_adr]['descr']])
    return list_obj
    print(list_obj)


if __name__ == '__main__':
    load_ini()
