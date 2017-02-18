from subprocess import check_output, CalledProcessError, call, Popen
from time import sleep, time, strftime, gmtime
success = False
already_success = False
def check_stream(device):
    global success
    global already_success
    for i in range(0,3):
        try:
            log = '\nTest'
            curr_time = strftime('%H:%M:%S', gmtime())
            check_stream_cmd = 'pgrep -f mjpg'.split()
            check_output(check_stream_cmd)
            log = '\nCamera stream successful. Time {}'.format(curr_time)
            success = True
        except CalledProcessError:
            log = '\nCamera stream failed. Attempt {0}. Time {1}'.format(i+1, curr_time)
            success = False
        finally:
            if not already_success:
                with open('/home/pi/CameraStream/logs/camera_log.txt', 'a') as logfile:
                    logfile.write(log)
            if success:
                with open('/home/pi/CameraStream/reboot.txt', 'w') as reboot:
                    reboot.write('0')
                already_success = True
		return
            else:
                already_success = False
                start_stream(device)

    reboot = None
    with open('/home/pi/CameraStream/logs/camera_log.txt','w') as logfile:
	with open('/home/pi/CameraStream/reboot.txt','r+') as reboot:
	    reboot_num = reboot.readline(1)
            if reboot_num < 3:
                reboot.write(reboot_num + 1)
                logfile.write('\nCamera stream failed 3rd time, reboot {0}. Time {1}').format(reboot_num, curr_time)
                reboot = true
            else:
                reboot.write('0')
                logfile.write('\nCamera inoperable. Time {}').format(curr_time)
                reboot = false

    if reboot:
        reboot_cmd = 'sudo shutdown -r now'.split()
	call(reboot_cmd)


def start_stream(device):
    stream_start_cmd = 'sh device{}.sh'.format(device)
    Popen(stream_start_cmd.split())


def kill_stream(device):
    stream_kill_cmd = 'sudo pkill -f video{}'.format(device).split()
    call(stream_kill_cmd)


if __name__ == '__main__':
    while(True):
        sleep(1)
        check_stream(0)

