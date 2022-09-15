#!/usr/bin/env bash

# turn on sh's job control
set -m

# debug: turn on echoing of all commands
set -x

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

if [ -z "$1" ] || [ -z "$2" ]
then
	printf "${RED} ERROR, quiting${NC}\n"
	echo usage: docker-entrypoint.sh [transmission-daemon-DIR] [libgen-seedtool-FILE]
	exit
fi

printf "${GREEN}[+] starting transmission-daemon:\n"
printf "[===] cd $1 && /usr/bin/transmission-daemon --foreground --config-dir $1 ${NC}\n"
cd $1 && /usr/bin/transmission-daemon --foreground --config-dir $1 &

printf "${GREEN}[+] starting libgen-seedtools:\n"
printf "[===] cd $2 && /usr/local/bin/libgen-seedtools --config $2/config.json fetch${NC}\n"
cd $2 && /usr/local/bin/libgen-seedtools --config $2/config.json fetch
printf "${GREEN}[+] done running libgen-seedtools${NC}\n"

printf "${GREEN}[+] transmssion-daemon's webinterface is available at http://$(hostname -i):9091${NC}\n"

### run untill background prcess exits
fg %1