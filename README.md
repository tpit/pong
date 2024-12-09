# pong
Professional ping in python

# Usage
Run script. It will challenge you for your input. Host, repeatcount, timeout and preffered method op output. 

Files are stored in ~/.pongs in text. 
Filename format is: host_repeatcount_date-time.txt

# Requirements:
- python3
- tqdm
- ping3

Without ping3 the script would have to use buitlin SOCK connection to hosts and this defeats the purpose. TQDM is used for the progress bar which is very helpful with longer iterations

# Purpose
This script is meant to do ping. However, it can store the results in a file based on the hosts, repetitions and date & time. Afterwards you can analyse the backlog with this script to see how many pings have failed te meet a certain benchmark. For instance. Show percentage of pings above 20ms is possible. This means you can ping a location for hours on end and won't have to do the scroll of scrolls... It will also show 95th percentile scores, however, I feel I should make this a 98th or higher mark.

Cheers,
Tommie

# Example output
tommie@dikke:~/.pongs$ pong.py 

    ___   _______  __   __  _______ 
    |   | |       ||  |_|  ||       |
    |   | |       ||       ||    _  |
    |   | |       ||       ||   |_| |
    |   | |      _||       ||    ___|
    |   | |     |_ | ||_|| ||   |    
    |___| |_______||_|   |_||___|    
                            v1.nerd
    # files are stored in ~/.pongs
    
Do you want to send the output to console or file? (console/file): **file**
Host address (ipv4/fqdn): **ppiitt.nl**
Enter timeout (in milliseconds) or press enter for 2000: **150**
Number of pings (or press enter for 4): **8**
Pinging: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 8/8 [00:08<00:00,  1.03s/ping]
Do you want to analyze a previously generated file? (yes/no): **yes**

Available ping output files:
1. 10.0.0.10_15_20241209-205841.txt
2. 1.2.3.4_4_20241209-214627.txt
3. ppiitt.nl_8_20241209-215059.txt
4. 10.0.0.1_3600_20241209-205917.txt
5. google.de_2_20241209-214817.txt

Choose a file (number) or press Enter to cancel: **3**
Enter threshold value in milliseconds: **29**

Analysis of /home/tommie/.pongs/ppiitt.nl_8_20241209-215059.txt:
    Total pings: 8
    Pings above 29.0ms: 1 (12.50%)
    Minimum RTT = 26.94ms, Maximum RTT = 29.01ms, Average RTT = 28.03ms, 95th Percentile = 29.32ms
