# pong
_Professional_ ping in python

# Usage
Run script. It will challenge you for your input. Host, repeatcount, timeout and preffered method op output. 

- python3 pong.py
- python3 pong.py textfile        -> for analysis of previous run

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
    
Do you want to send the output to console or file? (console/file): file
Host address (ipv4/fqdn): ppiitt.nl
Enter timeout (in milliseconds) or press enter for 2000: 250
Number of pings (or press enter for 4): 6
Pinging: 100%|██████████████████████████████████████████| 6/6 [00:06<00:00,  1.03s/ping]
Do you want to analyze a previously generated file? (yes/no): yes

Available ping output files:
1. 10.0.0.10_15_20241209-205841.txt
2. ppiitt.nl_6_20241209-215257.txt
3. 1.2.3.4_4_20241209-214627.txt
4. ppiitt.nl_8_20241209-215059.txt
5. 10.0.0.1_3600_20241209-205917.txt
6. google.de_2_20241209-214817.txt

Choose a file (number) or press Enter to cancel: 2
Enter threshold value in milliseconds: 28

Analysis of /home/tommie/.pongs/ppiitt.nl_6_20241209-215257.txt:
    Total pings: 6
    Pings above 28.0ms: 3 (50.00%)
    Minimum RTT = 26.83ms, Maximum RTT = 30.59ms, Average RTT = 28.20ms, 95th Percentile = 31.39ms
