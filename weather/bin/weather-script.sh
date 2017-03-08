#!/bin/sh

cd "$(dirname "$0")"

#input is weather-script-preprocess.svg
#output is weather-script-output.svg
python weather-script.py

mv weather-script-output.svg template-agenda.svg

#input is template-agenda.svg
#output is almost_done.svg
python2 parse_ical.py

mv almost_done.svg weather-script-output.svg

./rsvg-convert --background-color=white -o weather-script-output.png weather-script-output.svg
./pngcrush -qf -c 0 weather-script-output.png weather.png
#cp -f weather-script-output.png /var/www/kindle/weather.png

