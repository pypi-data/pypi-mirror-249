"""Temperature system check application"""
import os
import psutil
import sys
from datetime import datetime

# temporary way of limiting screen noise after KeyInterrupt by user
sys.tracebacklimit = 0

# class-based colors
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    if hasattr(psutil, "sensors_temperatures"):
        temperatures = psutil.sensors_temperatures()
    else:
        temperatures = {}
     
    if hasattr(psutil, "sensors_fans"):
        fans = psutil.sensors_fans()
    else:
        fans = {}
    
    battery = psutil.sensors_battery()
    
    clear_terminal()
    
    print(f'{bcolors.OKBLUE}{bcolors.BOLD}CPU Temperature:{bcolors.ENDC}')
    coretemp_slice = (temperatures['coretemp'])[1:8]
    for entry in coretemp_slice:
        print("%-15s %s °C " % (
            entry.label, entry.current))    
    print(f'{bcolors.OKBLUE}{bcolors.BOLD}Fan Speed:{bcolors.ENDC}')
    for name, entries in fans.items():
        for entry in entries:
            print(name, "%-10s %s RPM" % (
                entry.label, entry.current))
    print(f'{bcolors.OKBLUE}{bcolors.BOLD}Battery:{bcolors.ENDC}        %s%%' % (battery.percent))        
            
            
    dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")        
    print(f'\n{bcolors.WARNING}Current time:{bcolors.ENDC}', dt_string  )


while True:
    main()
    
        
