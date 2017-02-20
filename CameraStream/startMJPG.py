from subprocess import check_output, CalledProcessError, call, Popen
from time import sleep, time, strftime, gmtime
success = [False, False]
already_success = [False, False]
def check_stream(device):
    global success
    global already_success
    
    with open('/home/pi/CameraStream/reboot{}.txt'.format(device),'r+') as reboot_file:
        with open('/home/pi/CameraStream/reboot_time.txt','r') as reboot_time_file:
            reboot_time_file.seek(0)
            reboot_time = int(reboot_time_file.readline())
            if time() - reboot_time > 200:
                    reboot_file.seek(0)
                    reboot_file.write('00')
                        
    inoperable = False
    with open('/home/pi/CameraStream/reboot{}.txt'.format(device),'r') as reboot_file:
        reboot_file.seek(1)
        if(int(reboot_file.read(1)) == 1):
            inoperable = True
    if not inoperable:
        
        for i in range(0,4):
            if i == 0 and not already_success[device]:
                start_stream(device)
            else:
                try:
                    log = '\nTest'
                    curr_time = strftime('%H:%M:%S', gmtime())
                    check_stream_cmd = 'pgrep -f device{}'.format(device).split()
                    sleep(1)
                    check_output(check_stream_cmd)
                    log = 'Time: {1} Camera {0}: Stream successful.'.format(device, curr_time)
                    success[device] = True
                except CalledProcessError:
                    log = 'Time: {2} Camera {0}: Stream failed. Attempt {1}'.format(device, i, curr_time)
                    success[device] = False
                finally:
                    if not already_success[device]:
                        with open('/home/pi/CameraStream/logs/camera_log.txt', 'a') as logfile:
                            logfile.write(log + '\n')
                    if success[device]:
                        with open('/home/pi/CameraStream/reboot{}.txt'.format(device), 'w') as reboot_file:
                            reboot_file.seek(0)
                            reboot_file.write('00')
                        already_success[device] = True
                        return
                    else:
                        already_success[device] = False
                        start_stream(device)
                        sleep(1)

        reboot = None
        reboot_time = 0
        with open('/home/pi/CameraStream/reboot_time.txt','r') as reboot_time_file:
            reboot_time_file.seek(0)
            reboot_time = int(reboot_time_file.readline())
        with open('/home/pi/CameraStream/logs/camera_log.txt','a') as logfile:
            with open('/home/pi/CameraStream/reboot{}.txt'.format(device),'r+') as reboot_file:
                with open('/home/pi/CameraStream/reboot_time.txt','r') as reboot_time_file:
                    if time() - reboot_time > 40:
                        reboot_file.seek(0)
                        reboot_file.write('00')
                reboot_file.seek(0)
                reboot_num = int(reboot_file.readline(1))
                if reboot_num < 3:
                    reboot_file.seek(0)
                    reboot_file.write(str(reboot_num + 1))
                    logfile.write('Time: {2} Camera {0}: Streaming failed 3 times, reboot {1}.\n'.format(device, reboot_num + 1, curr_time))
                    reboot = True
                else:
                    reboot_file.seek(1)
                    reboot_file.write('1')
                    logfile.write('Time: {1} Camera {0}: Camera inoperable.\n'.format(device, curr_time))
                    reboot = False

        if reboot:
            with open('/home/pi/CameraStream/reboot_time.txt','w') as reboot_time_file:
                reboot_time_file.write(str(int(time())))
            reboot_cmd = 'sudo shutdown -r now'.split()
            call(reboot_cmd)


def start_stream(device):
    stream_start_cmd = 'sh device{}.sh'.format(device)
    Popen(stream_start_cmd.split())


def kill_stream(device):
    stream_kill_cmd = 'sudo pkill -f video{}'.format(device).split()
    call(stream_kill_cmd)


if __name__ == '__main__':
    sleep(5)
    while(True):
        check_stream(0)

