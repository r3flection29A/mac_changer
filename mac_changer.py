#! /usr/bin/env python3

import subprocess
import optparse
import re
import sys


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change it's MAC Address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC Address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("Specify an interface. -h/--help for more information")
    elif not options.new_mac:
        parser.error("Specify a MAC Address to change. -h/--help for more information")
    return options


def change_mac(interface, new_mac):
    print("[+] Changing MAC Address for {} to {}...".format(interface, new_mac))
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_mac_addr(interface):
    result = subprocess.check_output(["ifconfig", interface])
    mac_addr_search = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w', str(result))

    if mac_addr_search:
        return mac_addr_search.group(0)
    else:
        print("Not readable MAC Address... :(")


def main():
    options = get_arguments()
    try:
        change_mac(options.interface, options.new_mac)
    except subprocess.CalledProcessError:
        print("ERROR! Interface {} not found!".format_map(options.interface))
        sys.exit()
    current_mac = get_mac_addr(options.interface)
    print("Current MAC Address: {}".format(current_mac))
    if current_mac == options.new_mac:
        print("[+] Successfully changed MAC Address to {}".format(current_mac))
    else:
        print("[-] MAC Address did not get changed... :(")
        sys.exit()


main()
