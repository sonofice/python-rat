import platform, json
from resources.misc import get_size
from socket import socket, AF_INET, SOCK_STREAM
from os import listdir, getlogin, path
from psutil import boot_time, cpu_count, cpu_freq, cpu_percent, virtual_memory, swap_memory
from datetime import datetime


port = 64780
host_IP = "127.0.0.1"  # need to be loopback


def sysinfo():
    info = {}
    #print("="*40, "System Information", "="*40)
    uname = platform.uname()
    info.update({f"System": uname.system})
    info.update({f"Node Name": uname.node})
    info.update({f"Release": uname.release})
    info.update({f"Version": uname.version})
    info.update({f"Machine": uname.machine})
    info.update({f"Processor": uname.processor})

    # Boot Time
    #print("="*40, "Boot Time", "="*40)
    boot_time_timestamp = boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    time = bt.year, bt.month, bt.day, bt.hour, bt.minute, bt.second
    info.update({f"Boot Time": time})

    # let's print CPU information
    #info.update({"="*40, "CPU Info", "="*40)
    # number of cores
    info.update({f"Physical cores": cpu_count(logical=False)})
    info.update({f"Total cores": cpu_count(logical=True)})
    # CPU frequencies
    cpufreq = cpu_freq()
    max_freq = f"{cpufreq.max:.2f}Mhz"
    info.update({f"Maximum frequency": max_freq})
    cpu_perc= f"{cpu_percent()}%"
    info.update({f"Current CPU Usage": cpu_perc})

    # Memory Information
    #print("="*40, "Memory Information", "="*40)
    # get the memory details
    svmem = virtual_memory()
    total_mem = f"{get_size(svmem.total)}"
    available_mem = f"{get_size(svmem.available)}"
    mem_percentage = f"{svmem.percent}%"
    used_mem = f"{get_size(svmem.used)}"
    info.update({f"Total mem": total_mem})
    info.update({f"Available mem": available_mem})
    info.update({f"Used mem": used_mem})
    info.update({f"Percentage mem": mem_percentage})
    #print("="*20, "SWAP", "="*20)
    # get the swap memory details (if exists)
    swap = swap_memory()
    total_swap = f"{get_size(swap.total)}"
    free_swap = f"{get_size(swap.free)}"
    used_swap = f"{get_size(swap.used)}"
    swap_percentage = f"{swap.percent}%"
    info.update({f"Total swap": total_swap})
    info.update({f"Free swap": free_swap})
    info.update({f"Used swap": used_swap})
    info.update({f"Percentage swap": swap_percentage})
    print(info)
    info = json.dumps(info)
    return info


with socket(AF_INET, SOCK_STREAM) as s:
    s.bind((host_IP, port))
    s.listen()
    print("started listening")
    conn, addr = s.accept()

    with conn:
        while True:

            s.listen()
            print("listening")
            data = conn.recv(2048)
            print(data)
            cmnd = data.decode()
            print(cmnd)

            if cmnd.lower() == "exit":
                print("exiting")
                break
            elif cmnd.lower() == "pwd":
                result = path.dirname(path.realpath(__file__))
            elif cmnd.lower() == "user":
                result = getlogin()
            elif cmnd.lower() == "listdir":
                result = listdir()
            elif cmnd.lower() == "sysinfo":
                result = sysinfo()
            else:
                result = "passing"

            conn.sendall(bytes(result, encoding="utf-8"))
