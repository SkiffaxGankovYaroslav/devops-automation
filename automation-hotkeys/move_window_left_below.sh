#!/bin/bash
width=1834
height=1053
additional_small_window_size_width=10
winID=$(xdotool getwindowfocus)
wmctrl -i -r "$winID" -b remove,maximized_vert,maximized_horz #working
sleep 0.001
wmctrl -i -r "$winID" -e 0,0,$(( $height/2 )),$(( $width/2-$additional_small_window_size_width )),$(( $height/2 ))
# sleep 1/100
# xdotool windowmove "$winID" 0 0
# #xdotool windowsize "$winID" $(( $width )) $(( $height-$height/5 ))
# #xdotool windowminimize "$winID"
# xdotool windowsize "$winID" $width $(( $height-$height*100/80 ))