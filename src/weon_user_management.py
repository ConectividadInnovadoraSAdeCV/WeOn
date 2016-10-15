#!/usr/bin/python

import socket
import threading
import subprocess
import urllib2
import datetime
import os
import time

import weon_utils
from GpsMod import gps_service

target_host = ''
target_port = 7000

CONNECTION_FILE = "/home/rock/WeOn/logs/started_sections.txt"
STATE = "/home/rock/WeOn/logs/state_connections"
OUTPUT_FILE = "/home/rock/WeOn/logs/%s-GPS.txt" % datetime.date.today()

class user_thread(threading.Thread):
    iptables_set=1
    def __init__(self, threadID, mac,logger):
        self.threadLock = threading.Lock()
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.mac_address = mac
        self.ip_device = ""
        self.start_connection = weon_utils.get_time()
        self.start_position = gps_service.readgps(logger)
        self.log = logger

    def run(self):
        self.threadLock.acquire()
        self._define_iptable_rules()
        if user_thread.iptables_set == 0:
            self.threadLock.release()
        else:
            self._wait_user()
            self.end_position = gps_service.readgps( self.log )
            self.end_connection = weon_utils.get_time()
            self._append_data()
            if self.ip_device:
                self._remove_tcp_data()
            self.threadLock.release()

    def _define_iptable_rules(self):
        try:
            self.log.info("iptables for device: " )
            subprocess.check_output("sh /home/rock/WeOn/src/sysadmin/iptable_mac.sh " + self.mac_address, shell=True )
        except subprocess.CalledProcessError:
            logger.info("Unable to assign iptable rule to mac address: %s " % self.mac_address )
            user_thread.iptables_set = 0


    def _wait_user(self):
        try:
            ip_device = subprocess.check_output('arp -a | grep %s' % self.mac_address, shell=True).split(" ")
            ip_device = ip_device[1]
            self.ip_device = ip_device[1:-1]
            self.log.info( "%s -> %s" % ( self.ip_device, self.mac_address) )
            time.sleep(10)

            while not subprocess.Popen(["/bin/ping", "-n","-w5","-c1",self.ip_device],stdout=subprocess.PIPE).wait():
                time.sleep(5)
        except subprocess.CalledProcessError:
            self.log.info("failed")

    def _append_data(self):
        with open(OUTPUT_FILE, "a") as _file:
            _file.write("%s | %s | ( %s  ) | %s | ( %s )\n" % (self.mac_address, self.start_connection,
                                                            self.start_position, self.end_connection,
                                                            self.end_position))

    def _remove_tcp_data(self):
        self.log.info( "%s device disconneted " % self.ip_device)
        try:
            subprocess.check_output("sh /home/rock/WeOn/src/sysadmin/clean_ip.sh %s %s" % (self.mac_address, self.ip_device) , shell=True)
        except subprocess.CalledProcessError:
            pass

def start_service(logger):
    logger.info("USER MANAGEMENT")
    modified_date = ""
    count = 0
    threads = dict()
    socket.setdefaulttimeout(1)
    server =  socket.socket( socket.AF_INET, socket.SOCK_STREAM, 0 )
    server.bind( ( target_host , target_port  )  )
    server.listen( 5 )

    while True:
        check_threads(threads,logger)
        try:
            client_connection, addr = server.accept()
        except:
            continue
        client_mac_address = client_connection.recv( 128 )
        if client_mac_address:
            thread = user_thread(count, client_mac_address, logger)
            logger.info("Client device connected: " + client_mac_address)
            thread.start()
            time.sleep(1)
            client_connection.close()
            threads[ "%s" % count ] = thread
            count+=1


def check_threads(threads,logger):
    logger.info("%r" % threads)
    for count in threads.keys():
        print(threads[count].isAlive())
        if threads[count].isAlive():
            pass
        else:
            threads[count].join()
            threads.pop(count, None)


