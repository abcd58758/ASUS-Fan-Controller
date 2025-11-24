import subprocess
import os

if os.path.isfile("/sys/devices/platform/asus-nb-wmi/hwmon/hwmon5/temp1_input"):
    fan_path = '/sys/devices/platform/asus-nb-wmi/hwmon/hwmon5/'
elif os.path.isfile("/sys/devices/platform/asus-nb-wmi/hwmon/hwmon4/temp1_input"):
    fan_path = '/sys/devices/platform/asus-nb-wmi/hwmon/hwmon4/'

def read(path):
    result = subprocess.run(["cat", path], capture_output=True, text=True)
    output = result.stdout.strip()
    return output

def write(path, output):
    cmd = "echo " + output + " | " + "tee " + path
    os.system(cmd)

def temp():
    return int(read(fan_path + "temp1_input")) / 1000


def fan():
    return read(fan_path + "fan1_input")
def wfan(num):
    write(fan_path + "pwm1", num)


def pwm():
    return int(read(fan_path + "pwm1_enable"))
def wpwm(num):
    write(fan_path + "pwm1_enable", num)


def name():
    return read(fan_path + "fan1_label")

def service_status():
    result = subprocess.run(
        ['systemctl', 'is-active', 'fan_service'],
        capture_output=True,
        text=True
    )
    state_line =result.stdout.strip()
    if not os.path.isfile("/etc/systemd/system/fan_service.service"):
        return '找不到文件'
    if 'inactive' in state_line:
        return '停止运行'
    if 'activating' in state_line:
        return '启动中...'
    if 'active' in state_line:
        return '正在运行'
    return '错误！' + state_line
