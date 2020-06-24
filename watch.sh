#!/bin/bash
#
# Linux
#
set_term_title() {
   echo -en "\033]0;$1\a"
}

while [ "1" == "1" ]; 
do
	set_term_title "Monitoring changes"
	inotifywait -e modify -e create -r app.py
	set_term_title "Synching ..."

	sudo service lightdm restart

	set_term_title "Up-to-date"
	sleep 1
done


