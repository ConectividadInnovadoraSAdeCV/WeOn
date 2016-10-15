#!/usr/bin/python
import re
import subprocess
import time
import datetime

def read_conf_file():
    WEON_CONFIG_FILE="/etc/weon.conf"
    weon_dict = dict()
    with open(WEON_CONFIG_FILE, "r") as _file:
        for line in _file:
            if re.search("^(\w+)\ ?=\ ?([\w\d\.\/\_]+)",line):
                key, value = line.split("=")
                weon_dict[key]=value.rstrip()
    return weon_dict


def check_services(logger):
    fail_flag =  0
    count_limit = 10
    fail_count = 0

    logger.info("Check weon services")
    try:
        services_output=subprocess.check_output('sh /home/rock/WeOn/src/sysadmin/weon_service.sh', shell=True).split("\n")
        for service in services_output:
            if "Fail" in service:
                logger.info(service)
                fail_flag =  1
    except subprocess.CalledProcessError:
        pass

    if fail_flag:
        fail_count += 1
        if fail_count == count_limit:
            logger.info("Unable to restore services")
            return 0
        else:
            time.sleep(10)
            check_services(logger)
    return 1

def get_time():
    return datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')


def reporter(weon_connections,logger):
    logger.info("Weon report day")
    try:
        subprocess.check_output('sh /home/rock/WeOn/src/sysadmin/weon_reporter.sh %s %s %s %s %s' % (
                weon_connections['DEVICE_ID'],
                weon_connections['FTP_SERVER'],
                weon_connections['USER'],
                weon_connections['PASSWORD'],
                weon_connections['FTP_PATH']
            ), shell=True)
    except subprocess.CalledProcessError:
        logger.info("Weon report day failed")
        pass
    return 1
