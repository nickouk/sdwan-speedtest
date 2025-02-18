#!/usr/bin/env python3

# This script performs a speedtest

# This library hides sensitive input and replaces it with another character; default *
from pwinput import pwinput

# Cisco SDK for Catlayst SDWAN
from catalystwan.session import create_manager_session
from catalystwan.utils.alarm_status import Severity
from catalystwan.utils.personality import Personality
from catalystwan.exceptions import (
    DefaultPasswordError,
    ManagerHTTPError,
    ManagerReadyTimeout,
    ManagerRequestException,
    SessionNotCreatedError,
    TenantSubdomainNotFound,
)


# Standard libraries
from pprint import pprint
import urllib3
import ipaddress

username = input("Enter your username: ")
password = pwinput("Enter your password: ")

base_url = "https://vmanage-171203704.sdwan.cisco.com/"

# Disable insecure wanring due to self signed cert on SDWAN manager
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print(f"Connecting to vManage...\n")

# Create SDWAN Manager session
try:
    session = create_manager_session(url=base_url, username=username, password=password)
except ManagerHTTPError as error:
    # Error processing
    print(error.response.status_code)
    print(error.info.code)
    print(error.info.message)
    print(error.info.details)

# Get devices

print(f"Retrieving list of devices...\n")
devices = session.api.devices.get()

while True:
    while True:
        try:
            request_ip = input("Enter system IP address to run speedtest from or press [ENTER] to exit this tool: ")
            if request_ip == "":
                print("\nClosing the session")
                session.close()
                quit()
            request_ip = ipaddress.ip_address(request_ip)
            break
        except ValueError:
            continue

    request_ip = str(request_ip)

    n2r2 = devices.find(hostname="SH-N2-1-0002-NN36XF-R2")
    target = devices.find(local_system_ip=request_ip)

    print(f"\nPerforming speedtest from {target.hostname} to {n2r2.hostname}...\n")
    speedtest = session.api.speedtest.speedtest(target, n2r2, 60)

    print(speedtest)
    print("\n\n")
