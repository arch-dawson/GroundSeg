# Dependencies

## Openpyxl

Openpyxl is super useful, and I never had any trouble installing it. It's used to read the master telemetry definition. 

There's a really common warning about losing information, but it's not anything to be worried about.  It only happens when exporting from Excel or Google Sheets, since they add some extra information to each cell that openpyxl doesn't encapsulate.  

## mySQL (PyMySQL)

PyMySQL is the Python module used to interface with mySQL.  It's pretty easy to install with pip. 

mySQL itself is ridiculously fussy though, and the syntax is really weird until you get used to it. 

## UFTP

Can install from http://uftp-multicast.sourceforge.net/

For future users-- if you're running into an issue installing uftp with the headers for openssl:
run 'sudo apt-get install libssl-dev' to get those headers.  
<3 Past Dawson

## Netem 
Working command: "sudo tc qdisc add dev wlan0 root netem delay 100ms" 
View internet connections: ifconfig
Remove netem: sudo tc qdisc del dev wlan0 root
