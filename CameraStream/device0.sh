sudo /usr/local/bin/mjpg_streamer -i "/usr/local/lib/input_uvc.so -d /dev/video0 -y -f 5" -o "/usr/local/lib/output_http.so -w /usr/local/www -p 80"
