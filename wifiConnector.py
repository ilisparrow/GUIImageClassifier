import sys

f = open("interfaces", "w")

f.write('source-directory /etc/network/interfaces.d\n')
f.write("auto wlan0\n")
f.write("iface wlan0 inet dhcp\n")
f.write("       wpa-ssid ")
f.write(sys.argv[1])
f.write("\n")
f.write("       wpa-psk ")
f.write(sys.argv[2])
f.write("\n")
f.close()
