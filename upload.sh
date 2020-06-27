#!/bin/bash
#
# Linux
#
set_term_title() {
   echo -en "\033]0;$1\a"
}

# inotify does not work on WSL so using STAT and SLEEP...

#while [ "1" == "1" ];
#do
#	set_term_title "Monitoring changes"
#	inotifywait -e modify -e create -r app.py
#	set_term_title "Synching ..."
#
#	scp app.py pi@192.168.1.70:
#
#	set_term_title "Up-to-date"
#	sleep 1
#done



### Set initial time of file
export FILE="app.py"
LTIME=`stat -c %Z ${FILE}`

set_term_title "Monitoring changes"

while true
do
   ATIME=`stat -c %Z ${FILE}`
   if [[ "$ATIME" != "$LTIME" ]]
   then
       set_term_title "Synching ..."
       scp app.py pi@192.168.1.70:
       set_term_title "Up-to-date"
       LTIME=$ATIME
   fi
   sleep 5
done