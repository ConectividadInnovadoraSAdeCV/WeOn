#!/usr/bin/python
import re
import subprocess
import time
import datetime

from FtpMod import ftp_transfer

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
    return datetime.datetime.strftime( datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')

def reporter( weon_connection, logger):
    REPORT_FILE = "/home/rock/WeOn/logs/report.txt"
    date = datetime.date.today()
    logger.info(date)
    if check_date( REPORT_FILE, date ):
        return 1

    logger.info("Weon report day")
    __defaulf_reports = [ "gps", "connects",  "url" ]
    ftpObj = ftp_transfer.transfer_ftp( weon_connection )

    for report in  __defaulf_reports:
        logger.info( report  )
        ftpObj.connect()
        ftpObj.write_report( report )
        ftpObj.close()
    write_file( REPORT_FILE, "%s" %date )
    return 1

def check_date( REPORT_FILE, date ):
    fd = open(REPORT_FILE, 'r')
    value = fd.read()
    if "%s" % date in value:
        return 1
    return 0

def write_file(filename,data):
      f = open(filename, 'w')
      f.write(data)
      f.close()

def clean_url_file(  log_path, _url_file ):
    try:
         subprocess.check_output("sh /home/rock/WeOn/src/sysadmin/clean_url.sh %s %s" % ( log_path, _url_file) , shell=True)
    except subprocess.CalledProcessError:
        pass
