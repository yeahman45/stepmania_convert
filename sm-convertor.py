#!/usr/bin/env python
# -*- coding: utf-8 -*-

# yeahman

import os, argparse, glob, tkinter, re

def split(word):
    return [char for char in word]

def rollback(song):
    for backup_file in glob.glob(song + '/*.ssc.backup'):
        if os.path.isfile(backup_file):
            ssc_file = backup_file.replace('.backup', '')
            if os.path.exists(ssc_file):
                os.remove(ssc_file)
            os.rename(backup_file, ssc_file)

def convertSong(song):
    print('Convert Song : ' + song)
    
    # find backup and rollback
    rollback(song)
    
    # convert    
    for ssc_file in glob.glob(song + '/*.ssc'):
        previous_state = 0
        if os.path.isfile(ssc_file):
            new_file = ssc_file + '.tmp'
            with open(new_file, 'w+')  as newFile:
                newFile.close()
            with open(new_file, 'a') as newFile:
                with open(ssc_file, 'r+') as file:
                    while True:
                        line = file.readline()
                        if not line:
                            break                        
                        if line.find('pump-') > -1:
                            line = line.replace('pump-', 'dance-')
                        elif not re.search("^(\\d){5}$", line) == None:
                            arr = split(line)
                            new_arr = arr
                            # take care of middle button
                            if arr[2] != '0':
                                if previous_state == 0:
                                    new_arr[4] = arr[2]
                                if previous_state == 1:
                                    new_arr[3] = arr[2]
                                if previous_state == 3:
                                    new_arr[1] = arr[2]
                                if previous_state == 4:
                                    new_arr[0] = arr[2]

                            if arr[0] != '0':
                                previous_state = 0
                            if arr[1] != '0':
                                previous_state = 1
                            if arr[3] != '0':
                                previous_state = 3
                            if arr[4] != '0':
                                previous_state = 4                            
                            line = new_arr[0] + new_arr[1] + new_arr[4] + new_arr[3]+ '\n'
                        newFile.write(line)
                    file.close()
                    os.rename(ssc_file, ssc_file + '.backup')
                newFile.close()
                os.rename(new_file, ssc_file)

def main():
    parser = argparse.ArgumentParser(description='Stepmania Convertor', prog='Stepmania Convertor')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    parser.add_argument("--folder", help="Folder (Group) containing subfolders of songs", required=True)

    args = parser.parse_args()
    folder = args.folder.rstrip('/').rstrip('\\')
    for subfolder in glob.glob(folder + '/*'):
        if os.path.isdir(subfolder):
            convertSong(subfolder)

if __name__ == "__main__":
    main()