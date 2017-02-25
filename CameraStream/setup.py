from subprocess import call, check_output
import os
def create_sh(name, cmds, path=''):
    if path != '':
        os.chdir(path)
    file_cmd = 'touch {}.txt'.format(name)
    call(file_cmd.split())
    with open('{}.txt'.format(name),'w') as install_file:
        install_file.write(cmds)
    rename_cmd = 'mv {0}.txt {0}.sh'.format(name)
    call(rename_cmd.split())

def create_run_delete(cmds):
    create_sh('temp_installer', cmds)
    run_installer_cmd = 'sh temp_installer.sh'
    call(run_installer_cmd.split())
    del_installer_cmd = 'rm -f temp_installer.sh'
    call(del_installer_cmd.split())

    
def install_MJPG():
    MJPG_cmds = ('#!/bin/bash'
                 '\ncd /home/pi'
                 '\nsudo apt-get install libjpeg8-dev imagemagick libv4l-dev'
                 '\nsudo ln -s /usr/include/linux/videodev2.h /usr/include/linux/videodev.h'
                 '\nwget http://sourceforge.net/code-snapshots/svn/m/mj/mjpg-streamer/code/mjpg-streamer-code-182.zip'
                 '\nmkdir MJPGStreamer'
                 '\nmv mjpg-streamer-code-182.zip MJPGStreamer'
                 '\ncd MJPGStreamer'
                 '\nunzip mjpg-streamer-code-182.zip'
                 '\ncd mjpg-streamer-code-182/mjpg-streamer'
                 '\nmake mjpg_streamer input_file.so input_uvc.so output_http.so'
                 '\nsudo cp mjpg_streamer /usr/local/bin'
                 '\nsudo cp output_http.so input_file.so input_uvc.so /usr/local/lib'
                 '\nsudo cp -R www /usr/local/www'
                 '\ncd ../../'
                 '\nrm -rf mjpg-streamer-182.zip')
    create_run_delete(MJPG_cmds)


def create_files():
    create_path = '/home/pi/Vision-Processing-2017/CameraStream/'
    create_file_cmds = ('#!/bin/bash'
                        '\ncd /home/pi'
                        '\nmkdir CameraStream'
                        '\ncd CameraStream'
                        '\nmkdir logs'
                        '\ncd logs'
                        '\necho "CAMERA LOG" >> camera_log.txt'
                        '\ncd ..'
                        '\necho "00" >> reboot0.txt'
                        '\necho "00" >> reboot1.txt'
                        '\necho "0" >> reboot_time.txt')
    create_run_delete(create_file_cmds)
    device0_cmd = 'sudo /usr/local/bin/mjpg_streamer -i "/usr/local/lib/input_uvc.so -d /dev/video0 -y" -o "/usr/local/lib/output_http.so -w /usr/local/www -p 80"'
    create_sh('device0', device0_cmd, create_path)
    device1_cmd = 'sudo /usr/local/bin/mjpg_streamer -i "/usr/local/lib/input_uvc.so -d /dev/video1 -y" -o "/usr/local/lib/output_http.so -w /usr/local/www -p 443"'
    create_sh('device1', device1_cmd, create_path)
    launcher_cmds = ('#!/bin/bash'
                     '\ncd /'
                     '\ncd home/pi/Vision-Processing-2017/CameraStream/'
                     '\nsudo python startMJPG.py'
                     '\ncd /')
    create_sh('launcher', launcher_cmds)
    disable_cmds = ('#!/bin/bash'
                    '\nsudo pkill -f startMJPG'
                    '\nsudo pkill -f mjpg')
    create_sh('disable', disable_cmds)
    permissions_cmd = ('#!/bin/bash'
                       '\nfor f in /home/pi/Vision-Processing-2017/CameraStream/*.sh'
                       '\ndo'
                       '\n    sudo chmod 755 "$f"'
                       '\ndone')
    create_run_delete(permissions_cmd)


def create_reboot():
    job = '@reboot sh /home/pi/Vision-Processing-2017/CameraStream/launcher.sh >/home/pi/CameraStream/logs/cronlog 2>&1'
    cronjob_cmd = '(sudo crontab -l ; echo "{}")| sudo crontab -'.format(job)
    create_run_delete(cronjob_cmd)


if __name__ == '__main__':
    install_MJPG()
    create_files()
    create_reboot()

