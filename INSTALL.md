
## Installing

Starting from a new Kindle 4NT -
1) Copy the 'weather' directory from this repository to the Kindle's USB drive's root
2) 'Jailbreak' the kindle by following https://wiki.mobileread.com/wiki/Kindle4NTHacking#Jailbreak
3) Install USBhacks and test ability to get ssh access to kindle by following http://www.shatteredhaven.com/2012/11/1337365-ssh-on-kindle-4-usbnetwork-hack.html. 
4) Install python from https://www.mobileread.com/forums/showthread.php?t=88004.
5) logon to kindle via ssh and install three python modules -
		python -m ensurepip
		/mnt/us/python/bin/pip install icalendar
		/mnt/us/python/bin/pip install tzdata
		/mnt/us/python/bin/pip install pyyaml
6) The weather app can be tested by running /mnt/us/weather/weather.sh. 
Configuration options are set in the files 'weather.conf' and 'weather.conf.new' in the 'weather' directory in the Kindle's USB drive's root.

To get the easy launcher from the kindle home screen
1) Copy the 'kite' directory from this repository to the Kindle's USB drive's root
2) Install kite from https://www.mobileread.com/forums/showthread.php?t=168270 using the 'installation of kite as a script' method
3) Restart the Kindle and a pdf 'book' called Weather will have been added which will launch the weather app

## Note

All scripts are compatible with the dash and bash shell on your host system.

So you can test your configuration on the host system.

To leave the launcher hit ENTER.

(I use the Ubuntu LTS 12.04.)

Good luck!


## Partial directory structure on your Kindle internal SD card

```
/mnt/us
│
├── kite
│   ├── onboot
│   ├── ondrop
│   └── Weather
│
└── weather
    ├── bin
    │   ├── platform.sh
    │   ├── properties.sh
    │   └── weatherProperties.sh
    ├── img
    │   ├── flightmode-on.png
    │   ├── service-unavailable.png
    │   ├── weather-outdated.png
    │   └── wlan-unavailable.png
    ├── launcher.sh
    ├── weather.conf
    └── weather.sh
```
