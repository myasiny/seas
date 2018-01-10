import wmi
import psutil
def ProcessKiller(process_name):
    c = wmi.WMI()
    processes = {}
    for process in c.Win32_Process():
        processes[process.ProcessId] = process.Name
    for i, j in processes.items():
        if j == process_name:
            p = psutil.Process(i)
            p.terminate()
