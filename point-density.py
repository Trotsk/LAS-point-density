"""Computes point density for raw flightlines

Will generate csv file for each LAS file showing point ID, density, and spacing
restricting scan angles between -15 and 15 degrees.

Requires pip install tqdm
Requires LAStools downloaded into default data structure (C:\LAStools\bin)
"""

import re
from glob import glob
import subprocess
import os
from tqdm import tqdm
import csv


dir = input('What is the full path of your LAS files? \n > ')
try:
    os.chdir(dir)
except:
    raise ValueError('Invalid directory')

def extract(text):
    """filters stdout to match keywords"""
    clean_lines = [line.lstrip() for line in text.splitlines()]
    return [line for line in clean_lines if re.match("|".join(['file source ID:', 'point density:', 'spacing:']), line)]

def main():
    """ Invokes lasinfo, parses output for each LAS file,
    appends to csv file for each successive loop """
    filename = glob("*.las")  # search for LAS files in directory
    pbar = tqdm(total=len(filename), unit="file")  # instantiate progress bar

    for i in filename:
        # redirects to stdout as tqdm uses stderr
        proc = subprocess.Popen(['C:/LAStools/bin/lasinfo.exe', i, '-keep_scan_angle', '-15', '15', '-cd', '-nv', '-stdout'],
                                stdout=subprocess.PIPE)
        f = extract(proc.communicate()[0].decode('utf-8').strip())
        with open('point-density.csv', 'a', newline='\n') as output:
            wr = csv.writer(output)
            wr.writerow(f)
        pbar.update(1)  # increment progress bar
    pbar.close()  # close progress bar

main()