#!/bin/bash

# Activate the python virtual environment
    . /path_to_virtualenv/activate

case "$1" in
  start)
    echo "Starting server"
    # Start the daemon 
    python /home/rock/WeOn/src/ClientMod/ftp_daemon.py start
    ;;
  stop)
    echo "Stopping server"
    # Stop the daemon
    python /home/rock/WeOn/src/ClientMod/ftp_daemon.py stop
    ;;
  restart)
    echo "Restarting server"
    python /home/rock/WeOn/src/ClientMod/ftp_daemon.py restart
    ;;
  *)
    # Refuse to do other stuff
    echo "Usage: /etc/init.d/ftp_daemon_service.sh {start|stop|restart}"
    exit 1
    ;;
esac

exit 0

