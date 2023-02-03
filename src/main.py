#! /usr/bin/env python

import platform
import os
import psutil
import math

si_prefix=['B', 'KB', 'MB', 'GB', 'TB', 'PB']
base=1024
digit_after_point=2

# gpu info
gpu_unix_command = "lspci | grep VGA"
cpu_unix_command = "cat /proc/cpuinfo | grep name"

disk_info = psutil.disk_usage('/')

result = os.popen(gpu_unix_command).readlines()
cpu_info = os.popen(cpu_unix_command).read().split('\n')

gpus = ""

for num,i in enumerate(result):
        gpus += f"GPU {num}:" + str(i.split(":")[2])
        gpus += "        "

os_name = platform.node()
kernel = platform.release()

total=psutil.virtual_memory().total
total_class=min(int(math.log(total, base)), len(si_prefix) - 1)

free=psutil.virtual_memory().free
free_class=min(int(math.log(free, base)), len(si_prefix) - 1)

used=psutil.virtual_memory().used
used_class=min(int(math.log(used, base)), len(si_prefix) - 1)

memory = {
        'total':round(total / pow(base, total_class), digit_after_point),
        'free':round(free / pow(base, free_class), digit_after_point),
        'used':round(used / pow(base, used_class), digit_after_point),
}

fetch = f"""        OS: {os_name}
        Kernel: {kernel}
        DE: {os.environ.get("DESKTOP_SESSION")}
        CPU: {cpu_info[0].split(':')[1]}
        {gpus}Disk: {round(disk_info.used/(1028**3))} {si_prefix[used_class]} / {round(disk_info.total/(1028*1028*1028))} {si_prefix[total_class]}
        Memory: {memory['used']} {si_prefix[used_class]} / {memory['total']} {si_prefix[total_class]}"""

print(fetch)

