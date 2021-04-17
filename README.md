# Carputer
A raspberry pi interface for my ford escape

NOTE: I am in the process of a total re-write of the code. Therfore most of the code is not what I am currently developing. I am hopeing to uplad the current code and remove this code in the near future. 

Purpouse:
To give me navigation, OBDII Codes and hopfully errors, Audio system.

I am doing this project as my vehicle doesn't have a GPS system. So I decided to do my own and decided to add other functinality. I take this vehicle off into the backwoods often GPS functinaity can be handy. I will also be adding features to controll other extra electronics I have added to my vehicle, such as work lights, amber warning lights, solar pannels, and the Auxillery battery. 

The files that come with this are: start.sh, vlc.py, main.py as well as some supporting documentation of this project.

start.sh - a shell script that starts the various parts of this project - the media player, the gps map software, and the main program. 

vlc.py - this is just to start vlc
            - could probably just put this in the start.sh file
            - or posibly just startup on launch. 

main.py - this is the main file that gets the data and displays it with a crapy gui -- but at least it is working :) -- It also contains the switches for my 2 work lights via buttons on the gui. 
