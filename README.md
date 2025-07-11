# Python Network Diagnostic Toolkit

A command-line network diagnostic tool built in Python. This project was created as a self-initiated learning exercise to deepen my understanding of fundamental networking concepts and Python automation.

## Overview

This tool provides a simple, unified interface for common network troubleshooting tasks. It's designed to be cross-platform compatible (Windows, macOS, Linux) and uses only Python's standard libraries, requiring no external dependencies for core functionality.

## Features

- **DNS Resolution**: Automatically resolves any provided hostname to its IPv4 address.
- **Ping Host**: Checks for host reachability using the system's native ping command.
- **TCP Port Scanning**: Scans a user-defined list of TCP ports to identify open services. This demonstrates a practical understanding of TCP sockets and connections.
- **Traceroute**: Displays the network path (hops) to a target host by leveraging the system's traceroute or tracert command.
- **User-Friendly CLI**: Built with argparse for a clean, professional command-line interface with clear help messages.

## Learning Journey & Purpose

As an Electrical and Computer Science student with a strong background in the physical and systems layer, I built this project to bridge my knowledge into the world of higher-level networking. The key objectives were:

- **Practical Application of Theory**: To move beyond textbook definitions and write code that interacts directly with network protocols and services like DNS and TCP.
- **Automation & Scripting**: To develop practical skills in Python, a critical language for modern network automation and infrastructure management.
- **Understanding System Tools**: To learn how to integrate and automate existing, powerful system commands (ping, traceroute) within a custom application.
- **Software Development Best Practices**: To practice structuring a project, writing clean and commented code, and managing it with Git/GitHub.

This project has been an invaluable step in my journey toward becoming a network engineer.

## How to Use

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/network-toolkit.git
    cd network-toolkit
    ```

2. Run the tool with the `-h` flag to see all available options:

    ```bash
    python3 net_diag_tool.py -h
    ```

## Examples

- Run all checks on a host (ping, traceroute, and scan common ports):

    ```bash
    python3 net_diag_tool.py tiktok.com --all
    ```

- Ping a host:

    ```bash
    python3 net_diag_tool.py google.com --ping
    ```

- Scan specific ports on a host:

    ```bash
    python3 net_diag_tool.py 1.1.1.1 --scan "80,443,53"
    ```

- Perform a traceroute:

    ```bash
    python3 net_diag_tool.py unsw.edu.au --traceroute
    ```
