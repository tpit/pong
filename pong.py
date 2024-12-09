#!/usr/bin/env python3
"""
Description: [ping for professionals]
Author: [Tommie Pit]
Date: 2024-01-09
Version: 1.0
"""

# Standard library imports
import os
import sys

import socket
import time
import statistics
from datetime import datetime
import glob  # Add this to your imports at the top
from tqdm import tqdm  # Add this to your imports
from ping3 import ping, verbose_ping

def display_banner():
    banner = r"""
    ___   _______  __   __  _______ 
    |   | |       ||  |_|  ||       |
    |   | |       ||       ||    _  |
    |   | |       ||       ||   |_| |
    |   | |      _||       ||    ___|
    |   | |     |_ | ||_|| ||   |    
    |___| |_______||_|   |_||___|    
                            v1.nerd
    # files are stored in ~/.pongs
    """
    print(banner)

display_banner()  # Display the banner before any user input

def ask_user():
    # Constants
    HOST = input("Host address (ipv4/fqdn): ")
    try:
        timeout_input = input("Enter timeout (in milliseconds) or press enter for 2000: ")
        TIMEOUT = float(timeout_input)/1000 if timeout_input else 2.0  # Convert ms to seconds
    except ValueError:
        print("Invalid timeout value. Using default value of 2000 milliseconds.")
        TIMEOUT = 2.0

    try:
        count_input = input("Number of pings (or press enter for 4): ")
        PING_COUNT = int(count_input) if count_input else 4
    except ValueError:
        print("Invalid number. Using default value of 4 pings.")
        PING_COUNT = 4

    return HOST, TIMEOUT, PING_COUNT

def get_output_choice():
    choice = input("Do you want to send the output to console or file? (console/file): ").strip().lower()
    if choice not in ['console', 'file']:
        print("Invalid choice. Defaulting to console.")
        return 'console'
    return choice

def generate_filename(host, count):
    # Get the home directory
    home_dir = os.path.expanduser("~")
    # Define the pongs directory path
    pongs_dir = os.path.join(home_dir, ".pongs")
    # Create the directory if it doesn't exist
    os.makedirs(pongs_dir, exist_ok=True)
    # Generate the filename with the full path
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return os.path.join(pongs_dir, f"{host}_{count}_{timestamp}.txt")

def ping_host(host, timeout, count=4, output='console'):
    """
    Ping the host multiple times using ICMP and return RTT statistics.
    """
    rtts = []
    filename = generate_filename(host, count) if output == 'file' else None
    
    for i in tqdm(range(count), desc="Pinging", unit="ping"):
        try:
            rtt = ping(host, timeout=timeout)
            if rtt is None:
                output_line = f"Ping {i+1}: {host} - Request timed out"
            else:
                rtt *= 1000  # Convert to milliseconds
                rtts.append((time.strftime("%Y-%m-%d %H:%M:%S"), rtt))
                output_line = f"Ping {i+1}: {host} - Time= {rtt:.2f} ms at {rtts[-1][0]}"
            
            if output == 'console':
                print(output_line)
            else:
                with open(filename, "a") as f:
                    f.write(output_line + "\n")
            time.sleep(1)  # Wait between pings
        except Exception as e:
            print(f"An error occurred: {e}")
            return []
    
    return rtts

def analyze_file(filename, threshold):
    """
    Analyze the RTT values from a file and print a summary.
    """
    try:
        with open(filename, "r") as f:
            lines = f.readlines()
        
        rtt_values = []
        for line in lines:
            parts = line.split("Time= ")
            if len(parts) > 1:
                rtt_str = parts[1].split("ms")[0]
                try:
                    rtt = float(rtt_str)
                    rtt_values.append(rtt)
                except ValueError:
                    continue
        
        if not rtt_values:
            print("No valid RTT values found in the file.")
            return
        
        avg = statistics.mean(rtt_values)
        min_rtt = min(rtt_values)
        max_rtt = max(rtt_values)
        percentile_95 = statistics.quantiles(rtt_values, n=100)[94]  # 95th percentile
        above_threshold = len([rtt for rtt in rtt_values if rtt > threshold])
        percent_above_threshold = (above_threshold / len(rtt_values)) * 100
        
        print(f"\nAnalysis of {filename}:")
        print(f"    Total pings: {len(rtt_values)}")
        print(f"    Pings above {threshold}ms: {above_threshold} ({percent_above_threshold:.2f}%)")
        print(f"    Minimum RTT = {min_rtt:.2f}ms, Maximum RTT = {max_rtt:.2f}ms, Average RTT = {avg:.2f}ms, 95th Percentile = {percentile_95:.2f}ms")
    
    except FileNotFoundError:
        print(f"File {filename} not found.")
    except Exception as e:
        print(f"An error occurred while analyzing the file: {e}")

def list_ping_files():
    """
    List all ping output files in the ~/.pongs directory and let user select one.
    """
    # Get the home directory
    home_dir = os.path.expanduser("~")
    # Define the pongs directory path
    pongs_dir = os.path.join(home_dir, ".pongs")
    
    # Get all txt files in the pongs directory
    files = glob.glob(os.path.join(pongs_dir, "*_*_*.txt"))
    
    if not files:
        print("No ping output files found in the ~/.pongs directory.")
        return None
    
    print("\nAvailable ping output files:")
    for i, file in enumerate(files, 1):
        print(f"{i}. {os.path.basename(file)}")
    
    while True:
        try:
            choice = input("\nChoose a file (number) or press Enter to cancel: ").strip()
            if not choice:
                return None
            
            file_index = int(choice) - 1
            if 0 <= file_index < len(files):
                return files[file_index]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

def main():
    # Add file argument handling at the start of main()
    if len(sys.argv) > 1 and sys.argv[1].endswith('.txt'):
        # If file argument provided, analyze it immediately
        threshold = float(input("Enter threshold value in milliseconds: ").strip())
        analyze_file(sys.argv[1], threshold)
        return
    
    output_choice = get_output_choice()
    HOST, TIMEOUT, PING_COUNT = ask_user()  # Capture the returned values
    if output_choice == 'file':
        filename = generate_filename(HOST, PING_COUNT)
        rtts = ping_host(HOST, TIMEOUT, PING_COUNT, output_choice)
    else:
        rtts = ping_host(HOST, TIMEOUT, PING_COUNT, output_choice)
    
    if rtts and len(rtts) > 0:
        rtt_values = [rtt[1] for rtt in rtts]
        avg = statistics.mean(rtt_values)
        min_rtt = min(rtt_values)
        max_rtt = max(rtt_values)
        percentile_95 = statistics.quantiles(rtt_values, n=100)[94]
        summary = (
            f"\nPing statistics for {HOST}:\n"
            f"    Packets: Sent = {PING_COUNT}, Received = {len(rtts)}, Lost = {PING_COUNT-len(rtts)} ({(PING_COUNT-len(rtts))/PING_COUNT*100:.0f}% loss)\n"
            f"Approximate round trip times in milliseconds:\n"
            f"    Minimum = {min_rtt:.2f}ms, Maximum = {max_rtt:.2f}ms, Average = {avg:.2f}ms, 95th Percentile = {percentile_95:.2f}ms\n"
        )
        if output_choice == 'console':
            print(summary)
        else:
            with open(filename, "a") as f:
                f.write(summary)
    
    
    # Ask user if they want to analyze a file
    analyze_choice = input("Do you want to analyze a previously generated file? (yes/no): ").strip().lower()
    if analyze_choice == 'yes':
        selected_file = list_ping_files()
        if selected_file:
            threshold = float(input("Enter threshold value in milliseconds: ").strip())
            analyze_file(selected_file, threshold)

def setup():
    """Perform any necessary setup."""
    pass


if __name__ == "__main__":
    # This block only runs if the script is executed directly
    # (not imported as a module)
    setup()
    main()
