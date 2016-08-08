#!/usr/bin/python
import re
import subprocess
import time

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
        else:
            time.sleep(10)
            check_services(logger)

def report_day(logger):
    print "hola"


