# pong
Professional ping in python

# Language
I will change all dutch prompts to english,... soon. ;)

# Requirements:
- python3
- tqdm
- ping3

Without ping3 the script would have to use buitlin SOCK connection to hosts and this defeats the purpose. TQDM is used for the progress bar which is very helpful with longer iterations

# Purpose
This script is meant to do ping. However, it can store the results in a file based on the hosts, repetitions and date & time. Afterwards you can analyse the backlog with this script to see how many pings have failed te meet a certain benchmark. For instance. Show percentage of pings above 20ms is possible. This means you can ping a location for hours on end and won't have to do the scroll of scrolls... It will also show 95th percentile scores, however, I feel I should make this a 98th or higher mark.

Cheers,
Tommie
