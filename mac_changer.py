#!usr/bin/env python3

# import the necessary packages
import subprocess
import argparse
import re


# construct the argument parse and parse the arguments
def get_arguments():

    ap = argparse.ArgumentParser()

    ap.add_argument("-i", "--interface", required=True,
                    help="interface of Network")
    ap.add_argument("-m", "--mac_address", required=True,
                    help="mac Address")

    return vars(ap.parse_args())


# function to change mac address
def mac_changer(interface, new_mac_address):

    print("==> Changing MAC Address for " + interface + " to " + new_mac_address)

    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac_address])
    subprocess.call(["ifconfig", interface, "up"])


# function to get current MAC Address
def current_mac(interface):

    # Getting Data of ifconfig command
    ifconfig_data = subprocess.check_output(["ifconfig", interface])

    # Extracting ether or MAC Address
    ether_value = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_data)

    if ether_value:
        return ether_value.group(0)
    else:
        print("==> [X] Could not read MAC Address")


args = get_arguments()

# Getting Current MAC Address
current_mac_address = current_mac(args["interface"])
print("==> Current MAC Address = " + str(current_mac_address))

# If device MAC is not readable, return from further steps
if current_mac_address == None:
    print("==> [X] Exiting.")
elif current_mac_address == args["mac_address"]:
    print("==> [X] MAC address matches, no need to change")
else:
    mac_changer(args["interface"], args["mac_address"])

    # Getting Modified MAC Address
    print("==> Fetching Modified MAC Address")
    modified_mac_address = current_mac(args["interface"])

    if modified_mac_address == None:
        print("==> [X] Exiting.")
    else:
        if modified_mac_address == args["mac_address"]:
            print("==> MAC address was changed to " + modified_mac_address)
        else:
            print("==> [X] MAC address did not get changed.")

