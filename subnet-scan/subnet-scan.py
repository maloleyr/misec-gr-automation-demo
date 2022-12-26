#!/usr/bin/env python3
# A simple wrapper to run NMAP scans.
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


def main(verbose, subnet):
    """The main program."""
    if validate_subnet(subnet, verbose):
        
        # Get the network and netmask from the given subnet.
        network, netmask = subnet.split('/')
        if verbose:
            print(network)
            print(netmask)
        report = network + ".xml"
        report_html = report + ".html"
        # If there is an existing file delete it.
        if os.path.isfile(report):
            os.remove(report)

        # Run our NMAP process and report.
        #subprocess.call(["nmap", "-sT", "-F", "-T4", "--exclude-ports", "T:9100", "--script", "smb-os-discovery,banner", "-oX", report, subnet])
        subprocess.call(["nmap", "-A", "-v", "--exclude-ports", "T:9100", "--script", "smb-os-discovery,banner,vuln", "-oX", report, subnet])
        if verbose:
                print(f"An XML report for {subnet} has been created: {report}")

        # Try and convert our report to HTML. Requires xsltproc to be installed. 
        try:
            if os.path.isfile(report_html):
                os.remove(report_html)
            subprocess.call(["xsltproc", report, "-o", report_html])
            if verbose:
                print(f"An HTML report for {subnet} has been created: {report_html}")
        except Exception as e:
            print(f"Error: {e}.")
    else:
        return

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Given a specific subnet it'll run NMAP and save the results as an XML and an HTML report.")
    parser.add_argument("-s", "--subnet", type=str, required=True, help="The subnet to scan in CIDR format (e.g. 192.168.1.0/24).")
    parser.add_argument("-v", "--verbose", help="Turn on verbosity.", action="store_true")
    args = parser.parse_args()

    # Execute main()
    main(args.verbose, args.subnet)
    