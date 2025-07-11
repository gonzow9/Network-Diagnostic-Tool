# net_diag_tool.py
# A self-initiated project to learn core networking concepts and Python automation.
# Author: Samuel Witt

import socket
import subprocess
import platform
import argparse
import sys
from datetime import datetime

# To make output more readable
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'

def print_banner():
    """Prints a cool banner for the tool"""
    banner = f"""{Colors.BLUE}
    _   __     __  ___________   __________  ____  __
   / | / /__  / /_/  _/ ____/ | / / ____/ / / / / / /
  /  |/ / _ \/ __// // /   /  |/ / /   / /_/ / / / /
 / /|  /  __/ /__/ // /___/ /|  / /___/ __  / /_/ /
/_/ |_/\___/\__/___/\____/_/ |_/\____/_/ /_/\____/
        Network Diagnostic Tool by Samuel Witt
    {Colors.ENDC}"""
    print(banner)

def resolve_host(hostname):
    """
    Resolves a hostname to an IP address.
    Returns the IP address on success, or None on failure.
    """
    try:
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except socket.gaierror:
        # This error means DNS lookup failed
        return None

def ping_host(host):
    """
    Pings a host to check for reachability.
    Uses the system's built-in ping command for cross-platform compatibility.
    """
    print(f"\n{Colors.YELLOW}[*] Pinging {host}...{Colors.ENDC}")
    
    # Determine the correct ping command based on the operating system
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', host]
    
    try:
        # Run the command and capture the output
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)
        print(f"{Colors.GREEN}[+] Host is reachable.{Colors.ENDC}")
        print(output)
    except subprocess.CalledProcessError:
        # This error means the ping command failed (e.g. host unreachable)
        print(f"{Colors.RED}[-] Host is unreachable.{Colors.ENDC}")
    except FileNotFoundError:
        # This error means the ping command wasn't found on the system
        print(f"{Colors.RED}[-] Ping command not found. Please ensure it's in your system's PATH.{Colors.ENDC}")

def scan_ports(host, ports):
    """
    Scans a list of TCP ports on a given host.
    """
    ip_address = resolve_host(host)
    if not ip_address:
        print(f"{Colors.RED}[-] Cannot resolve hostname '{host}'. Aborting port scan.{Colors.ENDC}")
        return

    print(f"\n{Colors.YELLOW}[*] Starting TCP port scan on {host} ({ip_address})...{Colors.ENDC}")
    start_time = datetime.now()

    open_ports = []
    
    # Ports to scan are provided as comma separated string, so split them
    port_list = [int(p) for p in ports.split(',')]

    for port in port_list:
        # AF_INET specifies IPv4, SOCK_STREAM specifies TCP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set a timeout to avoid waiting too long for unresponsive ports.
        socket.setdefaulttimeout(1)
        
        # The core of the port scanner
        # connect_ex returns 0 if the connection is successful (port is open)
        result = sock.connect_ex((ip_address, port))
        if result == 0:
            print(f"{Colors.GREEN}[+] Port {port}: Open{Colors.ENDC}")
            open_ports.append(port)
        else:
            print(f"[-] Port {port}: Closed")
        sock.close()

    end_time = datetime.now()
    total_time = end_time - start_time
    print(f"\n{Colors.YELLOW}[*] Port scan completed in: {total_time}{Colors.ENDC}")
    if open_ports:
        print(f"{Colors.GREEN}Summary: Open ports found: {', '.join(map(str, open_ports))}{Colors.ENDC}")
    else:
        print(f"{Colors.RED}Summary: No open ports found in the specified list.{Colors.ENDC}")


def traceroute(host):
    """
    Performs a traceroute to show the network path to a host.
    """
    ip_address = resolve_host(host)
    if not ip_address:
        print(f"{Colors.RED}[-] Cannot resolve hostname '{host}'. Aborting traceroute.{Colors.ENDC}")
        return

    print(f"\n{Colors.YELLOW}[*] Performing traceroute to {host} ({ip_address})...{Colors.ENDC}")
    
    # Determine the command based on the OS
    command = 'tracert' if platform.system().lower() == 'windows' else 'traceroute'
    
    try:
        # Run the command and stream the output to the console in real-time
        process = subprocess.Popen([command, host], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        for line in process.stdout:
            sys.stdout.write(line)
        process.wait()
    except FileNotFoundError:
        print(f"{Colors.RED}[-] '{command}' command not found. Please ensure it is installed and in your system's PATH.{Colors.ENDC}")


def main():
    """Main function to parse arguments and call the right tool"""
    print_banner()

    # argparse to provides neat command-line interface.
    # automatically generates help messages
    parser = argparse.ArgumentParser(
        description="A simple network diagnostic tool.",
        epilog="Built as a learning project for network engineering fundamentals."
    )
    parser.add_argument("host", help="The target host or IP address to diagnose.")
    parser.add_argument("-p", "--ping", action="store_true", help="Perform a simple ping test.")
    parser.add_argument("-s", "--scan", type=str, help="Perform a TCP port scan. Provide a comma separated list of ports (e.g., '80,443,8080').")
    parser.add_argument("-t", "--traceroute", action="store_true", help="Perform a traceroute to the host.")
    parser.add_argument("-a", "--all", action="store_true", help="Run all diagnostic checks (ping, traceroute, and scan common ports).")

    # if no arguments, print the help message
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    
    target_host = args.host

    # DNS Lookup always performed first
    print(f"{Colors.YELLOW}[*] Resolving hostname '{target_host}'...{Colors.ENDC}")
    ip = resolve_host(target_host)
    if ip:
        print(f"{Colors.GREEN}[+] '{target_host}' resolved to IP address: {ip}{Colors.ENDC}")
    else:
        print(f"{Colors.RED}[-] Could not resolve '{target_host}'. Some functions may fail.{Colors.ENDC}")
        # don't exit here as the user might have provided an IP address directly.

    # Execute functions based on arguments
    if args.all:
        ping_host(target_host)
        # For the --all flag, scan a default list of common web ports
        common_ports = "21,22,80,443,3306,8000,8080"
        scan_ports(target_host, common_ports)
        traceroute(target_host)
    else:
        if args.ping:
            ping_host(target_host)
        if args.scan:
            scan_ports(target_host, args.scan)
        if args.traceroute:
            traceroute(target_host)

if __name__ == "__main__":
    main()

