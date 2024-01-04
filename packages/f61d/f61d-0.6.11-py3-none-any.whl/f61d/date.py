#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re, argparse, time
from datetime import datetime, timedelta
# import ast.literal_eval as eval

def parse_time_str(time_str):

    if time_str.lower() == 'now':
        return datetime.now()
    try:
        return datetime.strptime(time_str, '%Y-%m-%d_%H:%M:%S')
    except ValueError:
        try:
            return datetime.strptime(time_str, '%Y-%m-%d')
        except ValueError:
            return datetime.strptime(time_str, '%Y%m%d')

def parse_duration_str(duration_str):
    
    try:
        d = int(duration_str)
        desc = duration_str + 'Day'
        if d not in [-1, 0, 1]:
            desc += 's'
        return timedelta(days=d),desc
    except:
        pass
    
    parts = re.findall(r'([\d\.]+)([a-zA-Z]+)', duration_str.lower())
    # print(duration_str.lower(),parts)
    days = 0
    hours = 0
    minutes = 0
    seconds = 0
    desc = []

    for n, unit in parts:
        num = eval(n)
        if unit in ['y','year','years']:
            days += num * 365
            desc.append(n + "Year")
        elif unit in ['m','month','mon','months']:
            days += num * 30
            desc.append(n + "Month")
        elif unit in ['w','week','weeks']:
            days += num * 7
            desc.append(n + "Week")
        elif unit in ['d','days','day']:
            days += num
            desc.append(n + "Day")
        elif unit in ['h','hrs','hour','hr','hours']:
            hours += num
            desc.append(n + "Hour")
        elif unit in ['min','minite','minites']:
            minutes += num
            desc.append(n + "Minite")
        elif unit in ['s','sec','second','seconds','secs']:
            seconds += num
            desc.append(n + "Seconds")
            
    descc = '-'.join(desc)
    if len(desc) == 1 and num > 1:
        descc += 's'
    
    return timedelta(
        days=days,
        hours=hours,
        minutes=minutes,
        seconds=seconds
    ),descc


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Time calculations")
    parser.add_argument('-bt', '--base-time', required=True, help="Base time in the format 'YYYY-MM-DD_HH:MM:SS', 'YYYY-MM-DD', or 'YYYYMMDD'")
    parser.add_argument('-b', '--before', help="Duration before base time (e.g., '1y2m3d4h5min5s' or '4mon3week')")
    parser.add_argument('-a', '--after', help="Duration after base time (e.g., '1y2m3d4h5min5s' or '4mon3week5s')")
    parser.add_argument('-tt', '--target-time', help="Target time in the format 'YYYY-MM-DD HH:MM:SS', 'YYYY-MM-DD', or 'YYYYMMDD'")

    args = parser.parse_args()
    
    base_time = parse_time_str(args.base_time)
    print('Base time:',base_time,'/',)
    
    if args.before:
        duration, desc = parse_duration_str(args.before)
        before_time = base_time - duration
        print(f"Before {desc}: {before_time}")
    
    if args.after:
        duration, desc = parse_duration_str(args.after)
        after_time = base_time + duration
        print(f"After {desc}: {after_time}")
    
    if args.target_time:
        target_time = parse_time_str(args.target_time)
        if target_time < base_time:
            delta = base_time - target_time
            print(f"Target time is {delta} before base time.")
        elif target_time > base_time:
            delta = target_time - base_time
            print(f"Target time is {delta} after base time.")
        else:
            print("Target time is the same as base time.")

