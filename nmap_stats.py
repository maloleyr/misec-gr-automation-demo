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
    list_host_ports = [] # Placeholder for our discovered ports that match what we are looking for.
    for host in xml_root.findall("host"):
        list_ports = []
        if verbose:
            print(f"Host: {host}")
        ipv4 = "" # Set a blank ipv4
        for ip in host.findall("address"):
            if verbose:
                print(f"ip: {ip}")
                print(ip.get("addr"))
            if ip.get("addrtype") == "ipv4":
                ipv4 = ip.get("addr")
                # Go through all identified ports and see if they match what we are looking for.
                for ports in host.findall("ports"):
                    if verbose:
                        print(ports)
                    for port in ports:
                        portid = port.get("portid")
                        if verbose:
                            print(f"Port: {portid}")
                        if port:
                            list_ports.append(portid)
        list_hosts.append(ipv4)
        list_host_ports.append([ipv4, list_ports])

    if verbose:
        print(f"list_hosts:\n{list_hosts}")
    return report_name, list_hosts, list_host_ports

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
        report_name, list_hosts, list_host_ports = parse_nmap_file(report, verbose)
        print("=====================================================================")
        print(f"Report Name: {report_name}\t\tTotal Hosts (open ports): {len(list_hosts)}")
        print(f"Hosts:")
        for host in list_hosts:
            print(f"- {host}")
            for port in list_host_ports:
                if port[0] == host:
                    for p in port[1]:
                        print(f"\t{p}")
        print("=====================================================================\n\n")
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", type=str, required=True, help="A directory of NMAP XML files to parse.")
    parser.add_argument("-v", "--verbose", help="Turn on verbosity.", action="store_true")
    args = parser.parse_args()
    main(args.directory, args.verbose)
