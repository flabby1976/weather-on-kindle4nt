weather-on-kindle4nt
=====================

## Features

- The original function as an ebook reader remains
- Doesn't require any crontab usage. Runs for weeks/months on battery!
- Generates the weather file on the kindle itself. No need for server!
- Caches the last successfully generated weather file until it expires at 24:00
  (So you can take away your 'weather station' in the pub and show it all your friends.)
- The temporary files are written in the '/tmp' directory which is a temporary filesystem(32M), living in the memory

__Note__  
You need to install [kite](https://github.com/ufuchs/kite-kindle4nt) to launch the program.  

_Before_ that you have to jailbreak the Kindle and to install the [USBNetwork Hacks](http://www.mobileread.com/forums/showthread.php?t=88004).  
[Jeniffer](http://www.shatteredhaven.com/2012/11/1337365-ssh-on-kindle-4-usbnetwork-hack.html) has written a very good tutorial, esp. for the Windows guys.

You have to install python on the kindle - also at (https://www.mobileread.com/forums/showthread.php?t=88004).
and then two modules -

python -m ensurepip
/mnt/us/python/bin/pip install icalendar
/mnt/us/python/bin/pip install tzdata

