#!/usr/bin/python3

import csv
import os
import pytz

from datetime import datetime, timezone
from pathlib import Path
from time import strftime

startpath = Path("/Volumes/Quantum2/Vantage_Watch_Quantum2/")


def get_stats(*args):
    '''
    get the last accessed date and file size for the given path
    '''

    # print("ARGS: " + str(args))
    path = Path(args[0])
    # print("PATH: " + str(path))
    last_access = path.stat().st_atime
    timezone = pytz.timezone('US/Eastern')
    accs_date = datetime.fromtimestamp(last_access, timezone)

    filesize_byte = path.stat().st_size
    filesize_gigabyte = filesize_byte/1000000000
    print("SIZE: " + str(filesize_gigabyte))

    return accs_date, filesize_gigabyte


def write_path_to_csv(*args):
    '''
    write the path, last access date, and file size to a csv
    '''

    accs_date, filesize_gigabyte = get_stats(*args)

    datetime_str = args[1]

    if filesize_gigabyte < 0.01:
        filesize_str = str(filesize_gigabyte)
    else:
        filesize_str = str(round(filesize_gigabyte,2))

    print(accs_date)
    print(datetime_str)
    print(filesize_str)

    filename = "paths_w_access_date_" + datetime_str + ".csv"

    with open(filename, 'a', newline='') as csvfile:
        fieldnames = ["File_Path", "Last_Accessed", "File_Size_[Gig]"]
        writer = csv.writer(csvfile, delimiter=',', quotechar="'")
        writer.writerow((args[0], accs_date, filesize_str))

    # with open(filename, 'a', newline='') as csvfile:
    #     fieldnames = ["File_Path", "Last_Accessed", "File_Size_[Gig]"]
    #     reader = csv.reader(csvfile, delimiter=' ')
    #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #     writer.writeheader()
    #     # csvwriter = csv.writer(csvfile, delimiter=',', quotechar="'")
    #     writer.writerow({"File_Path": args[0], "Last_Accessed":accs_date,
    #         "File_Size_[Gig]":filesize_str})


def build_dir_map(startpath):
    '''
    traverse a root director and build a list of directories and files
    '''

    datetime_now = datetime.now()
    datetime_str = datetime_now.strftime("%Y%m%d")
    filename = "dir_map_" + datetime_str + '.txt'
    file = open(filename, 'a')

    for root, dirs, files in os.walk(startpath):
        dir_path = root + "/"
        write_path_to_csv(dir_path, datetime_str)

        level = root.replace(str(startpath), '').count(os.sep)
        indent = ' ' * 4 * (level)
        map_path = f"{indent}{os.path.basename(root)}/\n"
        file.write(map_path)
        subindent = ' ' * 4 * (level + 1)

        for f in files:
            if f.startswith("."):
                pass
            else:
                fpath = f"{subindent}{f}\n"
                file.write(fpath)
                print(fpath)
                file_path = dir_path + f
                write_path_to_csv(file_path, datetime_str)


build_dir_map(startpath)
