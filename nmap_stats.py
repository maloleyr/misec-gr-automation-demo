#!/usr/bin/env python3
# nmap_stats.py
# Given a directory of NMAP XML files summarize some statistics.

import argparse
import xml.etree.ElementTree as ET
import os
import glob

def parse_nmap_file(report, verbose):
    """Function to parse the NMAP report."""

    if verbose:
        print(f"Parsing NMAP XML File: {report}.")
    xml_data = ET.parse(report)
    xml_root = xml_data.getroot()
    #print(xml_root.attrib)
    #print(report)
    #print(os.path.splitext(os.path.basename(report))[0])
    report_name = os.path.splitext(os.path.basename(report))[0]
    if verbose:
        print(f"Report Name: {report_name}")
    list_hosts = [] # A place to hold the hosts that we discover.
    for host in xml_root.findall("host"):
        if verbose:
            print(f"Host: {host}")
        ipv4 = "" # Set a blank ipv4
        for ip in host.findall("address"):
            if verbose:
                print(f"ip: {ip}")
                print(ip.get("addr"))
            if ip.get("addrtype") == "ipv4":
                ipv4 = ip.get("addr")
        list_hosts.append(ipv4)
    if verbose:
        print(f"list_hosts:\n{list_hosts}")
    return report_name, list_hosts

def main(directory, verbose):
    """Main Program"""
    if verbose:
        print(f"Verbose is: {verbose}.")
        print(f"Looking for NMAP XML files in directory {directory}.")
    
    # Get our NMAP XML files.
    list_nmap_files = glob.glob(os.path.join(directory, "*.xml"))

    # Warn if there are no files to parse.
    if len(list_nmap_files) == 0:
        print(f"Warning: No NMAP XML files discovered in {directory}.")
        return

    for report in list_nmap_files:
        report_name, list_hosts = parse_nmap_file(report, verbose)
        print("=====================================================================")
        print(f"Report Name: {report_name}\t\tTotal Hosts: {len(list_hosts)}")
        print(f"Hosts:")
        for host in list_hosts:
            print(f"- {host}")
        print("=====================================================================\n\n")
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", type=str, required=True, help="A directory of NMAP XML files to parse.")
    parser.add_argument("-v", "--verbose", help="Turn on verbosity.", action="store_true")
    args = parser.parse_args()
    main(args.directory, args.verbose)
