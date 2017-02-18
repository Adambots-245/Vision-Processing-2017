TO INSTALL:
While connected to the internet, run the setup.py file. This should:
	1) Download and install MJPG Streamer
	2) Create a new directory /home/pi/CameraStream which contains all necessary files to run the stream
	3) Configure the Raspberry Pi to run the startMJPG.py script on startup
After installation is finished, copy the contents of the folder containing this READ_ME to the newly created directory.

TO USE:
On startup the Raspberry Pi should begin the stream, which can be accessed by going to http://yourip:port where 'yourip'
is the IP of the Raspberry Pi and 'port' is the number following the -p flag in the device0.sh or device1.sh files
(80 and 443 by defualt).
The disable.sh script will kill the startup script.
These scripts are for use with a USB Camera with a YVUV format. If the camera is already MJPG format, then the -y flag should
be removed from the device0.sh and device1.sh scripts. 
Framerate, resolution, and quality can be changed by adding -f<framerate>, -r<resolution>, or -q<quality> respectively
after the -y flag. Framerate is in FPS, resolution is of the format widthxheight in pixels, quality is the JPG compression
quality as a percentage.
To prevent the stream from running on startup, run $ sudo cronjob -e then remove the line that begins with @reboot.
Adding more streams should be relatively easy to implement, just look at how device0 and device1 are done.
The device0.sh and device1.sh files can be run directly to start either stream.

WHAT IT DOES:
By default the script will conitnuously check if a stream is running. if it is not running, it attempts to start a stream. if this fails, it attempts to rerun the script twice more.
If the stream still fails then the Raspberry Pi will reboot and attempt 3 more times to start the script.
After 3 reboots the camera is deemed inoperable. Log statements are written to the camera_log.txt file with timestamps.
Due to the nature of the code for writing logs, crashes will not be themselves recorded, but rather the successful reopening
of the stream or the failure thereof will be recorded. 
