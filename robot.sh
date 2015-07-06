#!/bin/bash
# ========================================================
# Bash script for controlling PiBot-A
# Version 1.1 - by Thomas Schoch - www.retas.de
# ========================================================

function die # Print an error message and terminate
{
    echo "$@" >&2
    exit 1
}

function start # Start robot
{
    local mode lmode robot

    # Select appropriate robot script
    read x mode lmode <<<$(grep "^1 " $config)
    [[ -n $mode ]] || die "Syntax error in $config"
    robot=$path/robot-$mode.py
    [[ -x $robot ]] ||
         die "Mode not yet implemented: $lmode"

    # Check whether robot is running already
    if [[ -z $pid ]]
    then
        # Start robot as daemon
        $robot <&- >/dev/null 2>&1 &
        echo $! >$pidfile
        $led0 1900 100
    else
        die "Robot already running: $pid"
    fi
}

function stop # Stop robot
{
    # Check whether robot is running
    if [[ -n $pid ]]
    then
        # Kill robot daemon
        kill $pid
        rm -f $pidfile
        $led0 100 1900
    else
        echo "Robot not running." >&2
    fi
}

# Location of scripts and files
path=${0%/*}             # path of this script
config=$path/robot.cfg   # config file with modes of robot
pidfile=$path/robot.pid  # file with PID of running robot
led0=/home/pi/io/led0    # script controlling status led

# Determine modes defined in config
modes=$(awk '{ printf "%s|", $2 }' $config)

# Check command line arguments. (Somewhat tricky: zero
# argument is allowed, awk above provides "|" at the end,
# the regex ^($args)$ will be evaluated to ^(xx|yy|zz|)$,
# which means: $1 may be NULL. For the usage message
# $args is expanded to "xx | yy | zz | ".)
args="start|stop|toggle|reset|shutdown|down|$modes"
[[ $1 =~ ^($args)$ ]] ||
    die "Usage: robot.sh [ ${args//|/ | } ]"

# Get pid of running robot process (if any) from pidfile
[[ -f $pidfile ]] && pid=$(<$pidfile)

# Perform the desired action
case $1
 in "")
    # No arguments given: show robot's pid and mode
    echo "${pid:--} $(sed -n "/^1/s/..//p" $config)"

 ;; ??)
    # Activate mode given in $1
    sed "s/./0/;/^. $1/s/./1/" $config >$config.new
    mv -f $config.new $config

    # Robot operations:
 ;; start)  start
 ;; stop)   stop
 ;; toggle) [[ -n $pid ]] && stop || start

 ;; reset)
    echo "00:00 0" >/home/pi/sys/runtime

 ;; shutdown|down)
    stop
    $led0 50 50
    shutdown -h now
esac
