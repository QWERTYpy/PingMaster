import configparser
import shutil


def save_ini(dict_object):
    # Сохраняем созданные объекты в файл
    config = configparser.ConfigParser()
    for _ in dict_object.keys():
        ip_adr = dict_object[_].ip_adr
        descr = dict_object[_].descr
        ping_status = dict_object[_].ping_status
        ping_off = dict_object[_].ping_off
        x = dict_object[_].x
        y = dict_object[_].y
        work_status = dict_object[_].work_status
        config[f"{ip_adr}"] = {'descr': descr,
                               'x': x,
                               'y': y,
                               'ping_status': ping_status,
                               'ping_off': ping_off,
                               'work_status': work_status}
    shutil.copy('example.ini', 'example_tmp.ini')
    with open('example.ini', 'w') as configfile:
        config.write(configfile)


def load_ini():
    # Загружаем объекты из файла
    config = configparser.ConfigParser()
    config.read('example.ini', encoding='cp1251')
    list_obj = []

    for ip_adr in config.sections():

        list_obj.append([ip_adr,
                         config[ip_adr]['x'],
                         config[ip_adr]['y'],
                         config[ip_adr]['descr'],
                         (True, False)[config[ip_adr]['ping_status'] == 'False'],
                         float(config[ip_adr]['ping_off']),
                         ((True, False)[config.get(ip_adr, 'work_status', fallback='True') == 'False'])])
    print(list_obj)
    return list_obj


if __name__ == '__main__':
    load_ini()
