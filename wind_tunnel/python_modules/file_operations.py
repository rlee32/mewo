#!/usr/bin/python

import os

def change_file_name(file_path, suffix):
  # Simply adds a suffix to an existing file.
  if os.path.isfile(file_path):
    os.system("mv "+file_path+" "+file_path+suffix)
  else:
    print "Couldn\'t find "+file_path
  return


def get_highest_folder(path, prefix):
  # Assumes that the folders in path are part of a series with an integer ID 
  # as the suffix.
  highest = 0
  folders = [x for x in os.listdir(path) if os.path.isdir(path+"/"+x)]
  print folders
  for folder in folders:
    folder_id = int(folder.replace(prefix, ""))
    if folder_id > highest:
      highest = folder_id
  return highest

def get_time_folders(path):
  time_folders = [ x for x in os.listdir(path) \
    if os.path.isdir(path+"/"+x) \
    and (("." in x) or (x.isdigit())) \
    and x != "0"]
  return time_folders

def leave_last_time(path):
  if os.path.isdir(path+"/processor0"):
    os.system("recontructPar -latestTime -case "+path)
    os.system("rm -r processor*")
  time_folders = get_time_folders(path)
  times = [ float(x) for x in time_folders ]
  times = [ int(x) if x.is_integer() else x for x in num_files ]
  times.sort()
  time_folders = [ str(x) for x in times ]
  time_folders_string = ' '.join(time_folders[0:-1])
  os.system("rm -r "+time_folders_string)
  return
