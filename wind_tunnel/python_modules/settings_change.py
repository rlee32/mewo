#!/usr/bin/python

def set_end_time(new_end_time, input_path, output_path):
  # The paths should be the input and output controlDicts.
  output_file = open(output_path, 'w')
  with open(input_path, 'r') as input_file:
    for line in input_file:
      if ("endTime" in line) and ("stopAt" not in line):
        time_value = line.split()[1]
        new_line = line.replace(time_value, str(new_end_time)+";")
        output_file.write(new_line)
      else:
        output_file.write(line)
  return