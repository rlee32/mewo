#!/bin/bash

gnuplot -persist > /dev/null 2>&1 << EOF
  set title "Forces vs. Time"
  set xlabel "Time / Iteration"
  set ylabel "Force (N) or Moment (N*m)"

  plot  "postProcessing/wing/0/forces.txt" using 1:2 title 'Lift' with linespoints,\
      "postProcessing/wing/0/forces.txt" using 1:3 title 'Drag' with linespoints,\
      "postProcessing/wing/0/forces.txt" using 1:4 title 'Moment' with linespoints
EOF
