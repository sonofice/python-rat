import platform, json
from datetime import datetime
from psutil import boot_time, cpu_count, cpu_freq, cpu_percent, virtual_memory, swap_memory

def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

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