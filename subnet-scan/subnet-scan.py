#!/usr/bin/env python3
# subnet-scan.py

import argparse
import ipaddress
import subprocess
import os

def validate_subnet(subnet, verbose):
    if verbose:
        print(f"Validating that {subnet} is real.")
    try:
        ipaddress.ip_network(subnet) # Check to see if this is a valid network.
        return True
    except Exception as e:
        print(f"Error: {e}. Please ensure you are entering a valid subnet.")
        return False


def main(verbose, subnet, file):
    """The main program."""
    if subnet:
        if validate_subnet(subnet, verbose):
            
            # Get the network and netmask from the given subnet.
            network, netmask = subnet.split('/')
            if verbose:
                print(network)
                print(netmask)
            report = network + ".xml"
            report_html = report + ".html"
    if file:
        report = file + ".xml"
        report_html = file + ".html"
    
    # If there is an existing file delete it.
    if file or subnet:
        if os.path.isfile(report):
            os.remove(report)

    # Run our NMAP process and report.
    if subnet: # Run this when given a subnet.
        subprocess.call(["nmap", "-A", "-v", "--exclude-ports", "T:9100", "--script", "smb-os-discovery,banner,vuln", "-oX", report, subnet])
    if file:
        subprocess.call(["nmap", "-A", "-v", "--exclude-ports", "T:9100", "--script", "smb-os-discovery,banner,vuln", "-oX", report, "-iL", file])
    if verbose:
        if subnet:
            print(f"An XML report for {subnet} has been created: {report}")
        if file:
            print(f"An XML report for {file} has been created: {report}")

    # Try and convert our XML report to HTML. Requires xsltproc to be installed. 
    if file or subnet:
        try:
            if os.path.isfile(report_html):
                os.remove(report_html)
            subprocess.call(["xsltproc", report, "-o", report_html])
            if verbose:
                if subnet:
                    print(f"An HTML report for {subnet} has been created: {report_html}")
                if file:
                    print(f"An HTML report for {file} has been created: {report_html}")
        except Exception as e:
            print(f"[!] Warning: You likely do not have \"xsltproc\" installed on your system. {e} ")
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Given a specific subnet or a file with a list of IP Addresses I'll run NMAP and save the results as an XML and an HTML report.")
    parser.add_argument("-s", "--subnet", type=str, required=False, help="The subnet to scan in CIDR format (e.g. 10.0.0.0/24).")
    parser.add_argument("-f", "--file", type=str, required=False, help="An input file with IP Addresses or hosts on individual new lines.")
    parser.add_argument("-v", "--verbose", help="Turn on verbosity.", action="store_true")
    args = parser.parse_args()

    # If we are given both a subnet and a file then exit.
    if args.subnet and args.file:
        print(f"Error: Please provide only a single subnet OR a single file for process.")
        exit(1)

    # Execute main()
    main(args.verbose, args.subnet, args.file)
