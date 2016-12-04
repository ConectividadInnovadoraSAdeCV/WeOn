#!/usr/bin/python
import subprocess
from GpsMod import gps_service


def gps_testing(logger=None):
    output =gps_service.readgps(logger)
    if "unable to read gps 1" in  output:
        subprocess.check_output('reboot', shell=True)
    else:
        if logger:
            logger.info("GPS Device is working correctly!")
